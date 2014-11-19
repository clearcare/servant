import requests
import json

class Transport(object):

    def send(self, data, actionclass):
        return actionclass._do_run(**data)


class HttpTransport(Transport):

    def send(self, data, actionclass):
        url = 'http://localhost:8888'
        response = requests.post(url, data=data)
        return response.json()


class Service(object):

    def __init__(self):
        if not hasattr(self, 'name'):
            raise Exception('Services must contain a name attribute')

        if not hasattr(self, 'version'):
            raise Exception('Services must contain a version attriute')

        self.__client = None

    def describe(self):
        return u'%s, version %d' % (
                self.__class__.name,
                self.__class__.version)

    def get_transport(self):
        return Transport()

    def get_client(self):
        if not self.__client:
            transport = self.get_transport()
            self.__client = Client(transport,
                    action_map=self.__class__.action_map)

        return  self.__client



class HttpService(Service):
    def get_transport(self):
        return HttpTransport()


class Client(object):

    def __init__(self, transport, action_map):
        self.__transport = transport
        self.__attach_action_map(action_map)

    def __attach_action_map(self, action_map):
        for name, actionclass in action_map.iteritems():
            setattr(self, name, self.__make_entry(actionclass))

    def __make_entry(self, actionclass):
        def call_service(**kwargs):
            # 1. prepare request
            request = self.prepare_request(**kwargs)

            # 2. send request
            service_response = self.__transport.send(request, actionclass)

            # 3. prepare response
            response = self.prepare_response(service_response)

            return response

        return call_service

    def prepare_request(self, **kwargs):
        return kwargs

    def prepare_response(self, service_response):
        return service_response


class Server(object):

    def __init__(self, transport):
        self.__transport = transport









#    def __getattr__(self, name):
#        actionclass = self.__class__.action_map.get(name)
#        if not actionclass:
#            raise AttributeError("'%s' object has no attribute '%s'" % (
#                    self.__class__.__name__, name))
#
#        _do_run_method = getattr(actionclass, '_do_run')
#        if not _do_run_method or (
#                _do_run_method and not callable(_do_run_method)):
#            raise AttributeError("'%s' object has no attribute '%s'" % (
#                    self.__class__.__name__, name))
#
#        import pdb; pdb.set_trace()
#            #jaction_instance = actionclass()
#        return actionclass._do_run


