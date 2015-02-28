import time
import requests

from ..config import Config
from ..constants import *
from ..exceptions import (
        ActionError,
        ActionFieldError,
        ServantException,
)
from ..serializers import JsonSerializer
from ..utils import generate_cid
from ..logger import create_logger


class Service(object):

    def __init__(self, do_configure=True):
        if not hasattr(self, 'name'):
            raise Exception('Services must contain a name attribute')

        if not hasattr(self, 'version'):
            raise Exception('Services must contain a version attriute')

        if not hasattr(self, 'action_map'):
            raise Exception('Services must contain an action_map attribute')

        self.__client = None
        self.__serializer = None

        self.config = Config()
        self.is_configured = False
        if do_configure:
            self.configure()

    @property
    def logger(self):
        return self.get_logger()

    @logger.setter
    def logger(self, logger):
        self._logger = logger

    def get_logger(self):
        """Return a Logger instance.

        Services are encouraged and expected to override this to return a Logger object which makes
        sense for a given service.  The default logger doesn't do much of anything other than
        calling ``logging.basicConfig``.

        """
        self._logger = getattr(self, '_logger', None)
        if self._logger:
            return self._logger

        self._logger = create_logger(self.__class__.__name__)
        return self._logger

    def configure(self):
        """Configuration hook for services to utilize as needed."""
        pass

    def describe(self):
        return u'%s, version %d' % (
                self.__class__.name,
                self.__class__.version)

    def before_request(*args, **kwargs):
        """Registers a function to run before each request."""
        pass

    def preprocess_request(self):
        """Do any request-wide setup"""
        pass

    def postprocess_response(self, response):
        """Do any request-wide teardown"""
        pass

    def handle_request(self, payload):
        """Entry point for actually running a service action.

        This method is called when running any of the application backends (eg,
        wsgi/http, local). It's important to note that any exception will be
        digest here so that the backend can reply with a suitable response to
        the client.

        :param payload: A serialized request object from a client, typically a
                        json encoded string
        :type payload: string
        :rtype:

        """
        self.__start_time = time.time()

        # TODO - start_request signal

        # hook for any type of setup
        self.preprocess_request()

        # response dictionary
        response = self.begin_response()

        action_results = []

        # this could be wrapped in process_response()
        try:
            deserialized_request_payload = self.deserialize_request(payload)
            actions = self.prepare_request(deserialized_request_payload)
            action_results = self.run_actions(actions)
        except ServantException, err:
            self.handle_service_error(err)
        except Exception, err:
            self.handle_unexpected_error(err)

        self.finalize_response(response, action_results)

        serialized_response = self.serialize_response(response)

        self.postprocess_response(response)

        # TODO - end_request signal

        return serialized_response

    def run_actions(self, actions):
        """Loop through and execute a list of actions in a request.

        :param actions: list of actions to exectute
        :type actions: list of action dicts
        :rtype: list of action results

        """
        action_results = []
        for i, action in enumerate(actions):
            action_class = self._get_action_class(action, i)
            if not action_class:
                action_result = {}
            else:
                action_result = self.run_single_action(action_class, action)

            action_results.append(action_result)

        return action_results

    def run_single_action(self, action_class, action):
        """Parses out a single request action along with kwargs and runs the
        requested action.

        Along with ``handle_request``, this is another important method which
        is responsible for actually executing an individual action. Most of the
        errors here should be of the type ``ActionFieldError``, which is raised
        from the client when a field in the model doesn't validate. Note that
        a field may be invalid upon invocation (user passes in invalid data) or
        after the fact.

        :param action_class: An action class, in other words, a single service
                             endpoint which will fulfill the request.
        :type action_class: class object which subclasses ``Action`` and has a
                            ``run`` method.
        :param action: An action dict which describes the action's input
        :type action: dict
        :rtype: response dict

        """
        args = action.get('arguments', {})
        field_errors = None
        action_results = None
        action_errors = None
        action_instance = None

        try:
            action_instance = action_class.get_instance(**args)
            action_instance.pre_run(service=self)
            action_results = action_instance.execute_run(service=self)
            action_errors = action_instance.get_errors() or None
            # copy the action errors into the main errors
            if action_errors:
                for err in action_errors:
                    self.add_service_error(
                            err['error'],
                            error_type=err['error_type'],
                            hint=err['hint'],
                    )
        except ActionError, err:
            error = self.handle_client_error(err)
            # set the action errors to be this one error
            action_errors = [error]
        except ActionFieldError, err:
            field_errors = self.handle_field_error(err)
            action_errors = [{
                'error': 'field_errors',
                'error_type': CLIENT_ERROR,
                'hint': 'One or more fields did not validate. ' \
                        'See field_errors attribute for details',
            }]

        if action_instance:
            action_instance.post_run()

        return {
                'action_name': action['action_name'],
                'errors': action_errors,
                'results': action_results,
                'field_errors': field_errors,
        }

    def get_wsgi_application(self, environ, start_response):
        """Pre-baked hook for running wsgi applications via http transport."""
        # TODO - This could eventually be moved out into a separate service object.

        # Note, space is required after status to conform to wsgi spec.
        status = '200 '
        headers = [
                ('Content-Type', 'application/json'),
        ]
        start_response(status, headers)

        content_length = int(environ['CONTENT_LENGTH'])
        payload = environ['wsgi.input'].read(content_length)
        response = self.handle_request(payload)
        return [response]

    def begin_response(self):
        self._service_errors = []
        return {}

    def finalize_response(self, response, action_results):
        """Add in the action results into the response and perform other
        necessary finalization.

        :param action_results: list of actions results
        :type action_results: list of action result dicts

        """
        response['actions'] = action_results
        response['response'] = {
                'response_time': '%0.5f' % (time.time() - self.__start_time, ),
                'correlation_id': self._cid,
                'errors': self._service_errors or None,
                'version': self.__class__.version,
                'name': self.__class__.name,
        }

    def deserialize_request(self, request_payload):
        """Deserialize a request object from a client.

        :param payload: A serialized request object from a client, typically a
                        json encoded string
        :type payload: string
        :rtype: dict

        """
        serializer = self.get_serializer()
        try:
           return serializer.deserialize(request_payload)
        except ServantException, err:
            self.handle_unexpected_error(err)

    def serialize_response(self, response):
        """Serialize the final response object as a last step before returning
        to the client.

        :param response: final response dictionary
        :type response: dict
        :rtype: serialized string

        """
        serializer = self.get_serializer()
        return serializer.serialize(response)

    def prepare_request(self, deserialized_request_payload):
        """Prepare the client's request for execution.

        :param deserialized_request_payload: Client's request
        :type deserialized_request_payload: dict
        :rtype: A list of actions to exectute

        """
        actions = self._get_actions_from_request(deserialized_request_payload)
        if not actions:
            return

        # self._validate_service_name(request)
        # get timeouts and other things
        self._cid = self._get_correlation_id(deserialized_request_payload)

        return actions

    def _get_action_class_by_name(self, action_name):
        action_class = self.__class__.action_map.get(action_name)
        if action_class:
            return action_class

        self.add_service_error('No action named "%s" found' % (action_name, ),
                CLIENT_ERROR)

    def _get_action_class(self, action, action_num):
        action_name = action.get('action_name')
        if not action_name:
            self.add_service_error('No action_name found in action %d' % (
                action, action_num), CLIENT_ERROR)
            return

        return self._get_action_class_by_name(action_name)

    def _get_actions_from_request(self, request):
        # request is the raw deserialized payload. It must be validated
        # assume we only have 1 action for now
        try:
            actions = request['actions']
        except KeyError, err:
            self.add_service_error('No actions found', CLIENT_ERROR)

        if not isinstance(actions, list):
            self.add_service_error('Actions must be a list', CLIENT_ERROR)

        if len(actions) < 1:
            self.add_service_error('Empty list of actions', CLIENT_ERROR)

        return actions

    def _get_correlation_id(self, request):
        try:
            return request['request']['correlation_id']
        except KeyError:
            return generate_cid()

    def handle_service_error(self, exc):
        """Add an error message to the list of request errors.

        This method should be invoked when there is an error that has a
        request-wide scope and is within the realm of the server.

        :param exc: An ``Exception`` object which should have subclassed
                    ``ServantException``

        """
        return self.add_service_error(exc, error_type=SERVER_ERROR)

    def handle_client_error(self, exc):
        """Add an error message to the list of request errors.

        This method should be invoked when there is an error that has a
        request-wide scope and is within the realm of the client, meaning the
        client has the ability to correct the problem.

        :param exc: An ``Exception`` object which should have subclassed
                    ``ServantException``
        """
        return self.add_service_error(exc, error_type=CLIENT_ERROR)

    def handle_unexpected_error(self, exc):
        """Handle an unexpected error.

        :param exc: An ``Exception`` object which should have subclassed
                    ``ServantException``

        """
        return self.add_service_error(exc, error_type=SERVER_ERROR,
                error_prelude='Unexpected service error')

    def handle_field_error(self, exc):
        """Any field-level exceptions should be caught and this method called
        in order to add client-readable errors.

        :param exc: An ``ActionFieldError`` object
        :rtype: dict mapping field names to a list of errors

        """
        errs = {}
        for errmsg in exc.messages:
            # Some exceptions have a messages attrs while other don't. Either
            # way, the results will be a dict.
            if hasattr(errmsg, 'messages'):
                errmsg = errmsg.messages

            for fieldname, err in errmsg.iteritems():
                field_errors = errs.get(fieldname, [])

                if isinstance(err, list):
                    err = ', '.join(err)

                field_errors.append({
                        'error': err,
                        'hint': err,
                })
                errs[fieldname] = field_errors

        return errs

    def add_service_error(self, exc, error_type, error_prelude='', hint=''):
        if hasattr(exc, 'messages') and isinstance(exc.messages, list):
            err = u', '.join(exc.messages)
        else:
            err = unicode(exc)

        if error_prelude:
            err = u'%s: %s' % (error_prelude, err)

        error = {
            'error': unicode(err),
            'hint': unicode(hint),
            'error_type': error_type,
        }
        self._service_errors.append(error)
        return error

    def get_serializer(self):
        if not self.__serializer:
            self.__serializer = JsonSerializer()
        return self.__serializer
