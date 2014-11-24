import time
import requests

from ..exceptions import (
        ActionFieldError,
        ServantException,
)
from ..serializers import JsonSerializer
from ..transport import get_server_transport_class_by_name
from ..utils import generate_cid

SERVER_ERROR = 'SERVER_ERROR'
CLIENT_ERROR = 'CLIENT_ERROR'


class Service(object):

    def __init__(self):
        if not hasattr(self, 'name'):
            raise Exception('Services must contain a name attribute')

        if not hasattr(self, 'version'):
            raise Exception('Services must contain a version attriute')

        if not hasattr(self, 'action_map'):
            raise Exception('Services must contain an action_map attribute')

        self.__client = None

        self.__serializer = None

    def describe(self):
        return u'%s, version %d' % (
                self.__class__.name,
                self.__class__.version)

    def get_transport(self, broker_type):
        return get_server_transport_class_by_name(name)

    def get_wsgi_application(self, environ, start_response):
        status = '200 '
        headers = [
                ('Content-Type', 'application/json'),
        ]
        start_response(status, headers)

        content_length = int(environ['CONTENT_LENGTH'])
        payload = environ['wsgi.input'].read(content_length)
        response = self.handle_request(payload)
        return [response]

    def handle_request(self, payload):
        self.__start_time = time.time()
        self.begin_response()
        action_results = []

        try:
            deserialized_payload = self.deserialize_request(payload)
            actions = self.prepare_request(deserialized_payload)
            action_results = self.run_actions(actions)
        except ServantException, err:
            self.handle_error(err)
        except Exception, err:
            self.handle_error(err)

        self.finalize_response(action_results)
        return self.serialize_response(self._response)

    def begin_response(self):
        self._response = {}
        self._service_errors = []

    def finalize_response(self, action_results):
        self._response['actions'] = action_results
        self._response['response'] = {
                'response_time': '%0.5f' % (time.time() - self.__start_time, ),
                'correlation_id': self._cid,
                'errors': self._service_errors or None,
        }

    def deserialize_request(self, payload):
        serializer = self.get_serializer()
        try:
           return serializer.deserialize(payload)
        except ServantException, err:
            self.add_service_error(err, SERVER_ERROR)

    def serialize_response(self, response):
        serializer = self.get_serializer()
        return serializer.serialize(response)

    def prepare_request(self, request):
        # request is the deserialized payload
        actions = self._get_actions_from_request(request)
        if not actions:
            return

        # self._validate_service_name(request)
        # get timeouts and other things
        self._cid = self._get_correlation_id(request)

        return actions

    def run_actions(self, actions):
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
        args = action.get('arguments', {})
        field_errors = None
        results = None
        try:
            results = action_class._do_run(**args)
        except ActionFieldError, err:
            field_errors = self.handle_field_error(err)

        return {
                'action_name': action['action_name'],
                'errors': None,
                'results': results,
                'field_errors': field_errors,
        }

    def _get_action_class(self, action, action_num):
        action_name = action.get('action_name')
        if not action_name:
            self.add_service_error('No action_name found in action %d' % (
                action, action_num), CLIENT_ERROR)
            return

        action_class = self.__class__.action_map.get(action_name)
        if not action_class:
            self.add_service_error('No action named "%s" found' % (action, ),
                    CLIENT_ERROR)
            return

        return action_class

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

    def add_service_error(self, exc, error_type):
        self._service_errors.append({
            'error': unicode(exc),
            'hint': unicode(exc),
            'error_type': error_type,
        })

    def handle_field_error(self, exc, error_type=None):
        errs = {}
        for errmsg in exc.messages:
            # Some exceptions have a messages attrs while other don't. Either
            # way, the results will be a dict.
            if hasattr(errmsg, 'messages'):
                errmsg = errmsg.messages

            for fieldname, err in errmsg.iteritems():
                field_errors = errs.get(fieldname, [])
                field_errors.append({
                        'error': err,
                        'hint': err,
                })
                errs[fieldname] = field_errors

        return errs

    def handle_error(self, exc):
        pass
#        "response": {
#            "has_errors": true,
#            "response_time": "1.2325",
#            "result": "PARTIAL_SUCCESS",
#            "service_name": "cc.payment_processing",
#            "correlation_id": "0e197907-6e8c-11e4-9e77-3c15c2cc31d0"
#        }

    def get_serializer(self):
        if not self.__serializer:
            self.__serializer = JsonSerializer()
        return self.__serializer
