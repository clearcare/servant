from .base import BaseTransport

import requests


class HttpTransport(BaseTransport):

    def __init__(self):
        self.__url = 'http://localhost:8000'

    def __repr__(self):
        return 'HttpTransport at %s' % (self.__url, )

    def configure(self, host='localhost', port=8000, scheme='http', **kwargs):
        self.__url = '%s://%s:%s' % (scheme, host, port)
        self.__service_name = kwargs.get('service_name', 'servant')
        self.__service_version = kwargs.get('service_version', '1')

    def is_connected(self):
        return True

    def send(self, data):
        headers = {
                'host': self.__service_name,
                'content-type': 'application/json',
        }
        response = requests.post(self.__url, data=data, headers=headers)
        return response.text
