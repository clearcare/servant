from calculator_service.service import CalculatorService
from calculator_service.service import CalculatorServiceV2

service = CalculatorServiceV2()
application = service.get_wsgi_application
