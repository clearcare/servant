from service import SimpleService

server = SimpleService()
application = server.get_wsgi_application
