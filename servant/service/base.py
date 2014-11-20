import requests
import json


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

#    def get_client(self):
#        if not self.__client:
#            transport = self.get_transport()
#            self.__client = Client(transport,
#                    action_map=self.__class__.action_map)
#
#        return  self.__client


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
            import pdb; pdb.set_trace()
            # this should transform the data into the necessary format, and
            # decorate it with addition info about the service
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

    def send(self, **kwargs):
        pass


import json
import sys
import SimpleHTTPServer
import SocketServer
import urlparse



class EchoHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))

        print('Path -> ' + self.path)

        for key, value in post_data.iteritems():
            print('%s: %s' % (key, value))

        resp = json.dumps(post_data)
        self.wfile.write(resp)


class ServiceHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/json')
        self.end_headers()

        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))



class Server(Service):

    def __init__(self, host='localhost', port=8888):
        super(Server, self).__init__()
        self.host = host
        self.port = port

#    def send(self, data, actionclass):
#        return actionclass._do_run(**data)
#

    def serve_forever(self):
        httpd = SocketServer.TCPServer(
                (self.host, self.port),
                EchoHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()

    def get_transport(self):
        return HttpTransport(self)

