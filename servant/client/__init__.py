from ..transport import get_client_transport_class_by_name
from ..utils import generate_cid

from ..serializers import JsonSerializer
from .response import Response


class Client(object):

    def __init__(self, service_name, service_version=1, **kwargs):
        self.service_name = service_name
        self.service_version = service_version
        self.service_meta = kwargs

        self.__transport = None
        self.__serializer = None

    def __getattr__(self, name):
        return self.send(name)

    def is_configured(self):
        return self.__transport is not None

    def configure(self, broker_type='local', **kwargs):
        if self.__transport is None:
            self.__transport = self.get_transport(broker_type)
            self.__transport.configure(**kwargs)
            self.__transport.connect()

    def configure_from_service_instance(self, service_instance):
        """Special hook to create a transport directly from an instantiated
        service.  Used mostly for testing.

        """
        if self.__transport is None:
            self.__transport = self.get_transport('local')
            self.__transport.service = service_instance

    def send(self, action_name):
        # by default, configure for local calls
        if not self.is_configured():
            self.configure(broker_type='local',
                    service_name=self.service_name,
                    service_version=self.service_version,
                    service_meta=self.service_meta)

        def make_call(**kwargs):
            payload = self.prepare_request(action_name=action_name, **kwargs)
            request = self.serialize_request(payload)
            service_response = self.__transport.send(request)
            response = self.prepare_response(service_response)
            return response

        return make_call

    def prepare_request(self, action_name, **kwargs):
        request = {
                'service_name': self.service_name,
                'service_version': self.service_version,
                'correlation_id': generate_cid()
        }
        return {
                'actions': [
                    {
                        'action_name': action_name,
                        'arguments': kwargs,
                    }
                ],
                'request': request,
        }

    def get_serializer(self):
        if not self.__serializer:
            self.__serializer = JsonSerializer()
        return self.__serializer

    def serialize_request(self, payload):
        serializer = self.get_serializer()
        return serializer.serialize(payload)

    def get_transport(self, broker_type, **kwargs):
        return get_client_transport_class_by_name(broker_type)

    def set_transport(self, name):
        pass

    def prepare_response(self, service_response):
        response = self.deserialize_response(service_response)
        return Response.fromDict(response)

    def deserialize_response(self, response):
        serializer = self.get_serializer()
        return serializer.deserialize(response)

    def handle_exception(self):
        pass

    def set_timeout(self):
        pass

    def describe(self):
        pass



class InternalClient(object):

    def __init__(self, service, do_begin_response=False):
        """Parameters:

        * do_begin_response: causes the service errors to be reset.
                This can be useful if your actions are independent and you
                only care about the latest action's errors.
        
        Note: `do_begin_response` only solves the problem of resetting
        the response errors between requests.
        The InternalClient needs more thought for complicated used cases
        where we pipeline multiple commands from the original client.
        If you find yourself reaching into the internals of this object
        (or the service or response objects), please consider improving
        the InternalClient interface.
        """
        self.__service = service
        self.do_begin_response = do_begin_response

    def __getattr__(self, name):
        return self.send(name)

    def send(self, name):
        action_class = self.__service._get_action_class_by_name(name)
        if not action_class:
            return

        def make_call(**kwargs):
            action = {'action_name': name, 'arguments': kwargs}
            if self.do_begin_response:
                self.__service.begin_response()  # reset errors
            action_results = self.__service.run_single_action(action_class, action)
            service_response = {}
            self.__service.finalize_response(service_response, [action_results])
            response = Response(service_response)
            return response

        return make_call

