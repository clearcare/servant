import requests

class HttpTransport(object):

    def __init__(self):
        self.__url = 'http://localhost:8000'

    def __repr__(self):
        return 'HttpTransport at %s' % (self.__url, )

    def configure(self, host='localhost', port=8000, scheme='http'):
        self.__url = '%s://%s:%s' % (scheme, host, port)

    def connect(self):
        pass

    def is_connected(self):
        return True

    def send(self, data):
        headers = {'content-type': 'application/json'}
        response = requests.post(self.__url, data=data, headers=headers)
        return response.json()

    def handle_errors(self, response):
        pass

    def is_error(self, response):
        pass


_TRANSPORT_MAPPING = {
        'http': HttpTransport(),
}

def get_client_transport_class_by_name(name):
    return _TRANSPORT_MAPPING[name.lower()]

def get_server_transport_class_by_name(name):
    return _TRANSPORT_MAPPING[name.lower()]
