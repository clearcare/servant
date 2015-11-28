from .base import BaseTransport

import requests


class HttpTransport(BaseTransport):

    def __init__(self):
        self.__url = 'http://localhost:8000'

    def __repr__(self):
        return 'HttpTransport at %s' % (self.__url, )

    def configure(self, host='localhost', port=8000, scheme='http'):
        self.__url = '%s://%s:%s' % (scheme, host, port)

    def is_connected(self):
        return True

    def send(self, data):
        headers = {'content-type': 'application/json'}
        response = requests.post(self.__url, data=data, headers=headers)
        return response.text
