from .response import Response, FutureResponse
from ..serializers import JsonSerializer
from ..transport import get_client_transport_class_by_name
from ..utils import generate_cid


class Batch(object):

    def __init__(self, client):
        self.__client = client
        self.__responses = {}

    def __getattr__(self, name):
        return self.deferred_send(name)

    def deferred_send(self, action_name):

        def make_call(**kwargs):
            cid = generate_cid()
            self.__client.add_action(action_name=action_name, cid=cid, **kwargs)
            future_response = FutureResponse()
            self.__responses[cid] = future_response
            return future_response

        return make_call

    def execute(self):
        response = self.__client.send()
        for cid, result in response.action_results():
            future_response = self.__responses[cid]
            future_response.init_from_result(result)


class Client(object):

    def __init__(self, service_name, service_version=1, **kwargs):
        self.service_name = service_name
        self.service_version = service_version
        self.service_meta = kwargs

        self.__transport = None
        self.__serializer = None
        self.__requests = None

    def __getattr__(self, name):
        return self.send_single_action(name)

    def is_configured(self):
        return self.__transport is not None

    def configure(self, broker_type='local', **kwargs):
        if self.__transport is None:
            self.__transport = self.get_transport(broker_type)
            self.__transport.configure(**kwargs)
            self.__transport.connect()

    def batch(self):
        return Batch(self)

    def send_single_action(self, action_name):
        def make_call(**kwargs):
            self.add_action(action_name=action_name, **kwargs)
            return self.send()

        return make_call

    def send(self):
        """Prepare the request and send it off to the service via the
        configured transport.

        """
        # by default, configure for local calls
        if not self.is_configured():
            self.configure(broker_type='local',
                    service_name=self.service_name,
                    service_version=self.service_version,
                    service_meta=self.service_meta)

        payload = self.prepare_request()
        request = self.serialize_request(payload)
        ### TODO - need to handle connection errors and timeouts here
        service_response = self.__transport.send(request)
        response = self.prepare_response(service_response)
        return response

    def add_action(self, action_name, cid=None, **kwargs):
        if self.__requests is None:
            self.__requests = []

        cid = cid or generate_cid()
        self.__requests.append({
                'action_name': action_name,
                'action_cid': cid,
                'arguments': kwargs,
        })

    def prepare_request(self):
        if not self.__requests:
            raise Exception('No actions to execute')
        request = {
                'service_name': self.service_name,
                'service_version': self.service_version,
        }
        return {'actions': self.__requests, 'request': request}

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
        return Response(response)

    def deserialize_response(self, response):
        serializer = self.get_serializer()
        return serializer.deserialize(response)

    def handle_exception(self):
        pass

    def set_timeout(self):
        pass

    def describe(self):
        pass

