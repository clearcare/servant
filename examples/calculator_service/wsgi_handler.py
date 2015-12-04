from calculator_service.service import CalculatorService

service = CalculatorService()
application = service.get_wsgi_application
