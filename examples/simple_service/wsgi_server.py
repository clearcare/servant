from wsgiref.simple_server import make_server
from wsgiref.validate import validator

from wsgi_handler import application

validator_app = validator(application)

httpd = make_server('', 8888, validator_app)
print "Serving on port 8888..."
httpd.serve_forever()
