from ..transport import get_client_transport_class_by_name
from ..utils import generate_cid

from ..serializers import JsonSerializer


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

    def configure(self, broker_type, **kwargs):
        if self.__transport is None:
            self.__transport = self.get_transport(broker_type)
            self.__transport.configure(**kwargs)
            self.__transport.connect()

    def send(self, name):
        def make_call(**kwargs):
            payload = self.prepare_request(action_name=name, **kwargs)

            request = self.serialize_request(payload)

            # 2. send request
            service_response = self.__transport.send(request)

            # 3. prepare response
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
        return service_response

    def deserialize_response(self):
        pass

    def handle_exception(self):
        pass

    def set_timeout(self):
        pass

    def describe(self):
        pass

