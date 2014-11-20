class BaseClient(object):

    def __init__(self, service_name):
        self.service_name = service_name


class Client(BaseClient):

    def __getattr__(self, name):
        return self.send

    def get_transport(self):
        pass

    def set_transport(self, name):
        pass

    def send(self, **kwargs):
        print kwargs
        return
        request = self.prepare_request(**kwargs)

        # 2. send request
        service_response = self.__transport.send(request)

        # 3. prepare response
        response = self.prepare_response(service_response)

        return response

    def prepare_request(self, **kwargs):
        return kwargs

    def prepare_response(self, service_response):
        return service_response

