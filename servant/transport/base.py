class TransportBase(object):

    def connect(self, **kwargs):
        pass

    def get_connection(self, **kwargs):
        pass

    def disconnect(self):
        pass

    def is_connected(self):
        return False

    def send(self, data, actionclass):
        raise NotImplementedError('Subclasses must override this method')



class ServerTransport(TransportBase):
    def __init__(self, server):
        self._server = server

class HttpServerTransport(ServerTransport):

    def get_connection(self):
        return 'http://%s:%s' % (self._server.host, self._server.port)

    def send(self, data, actionclass):
        url = self.get_connection()
        response = requests.post(url, data=data)
        return response.json()



class ClientTransport(TransportBase):
    pass

class LocalClientTransport(ClientTransport):

    def send(self, data, actionclass):
        return actionclass._do_run(**data)


