class BaseTransport(object):

    def connect(self):
        pass

    def is_connected(self):
        return False

    def configure(self, **kwargs):
        pass

    def send(self, data):
        raise NotImplementedError('Subclasses must override this method')
