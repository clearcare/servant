from servant.service.base import Service

from .actions import AddAction, SubtractAction, DivideAction
from .actions import MultiplyAction, BackwardSubtractAction


class CalculatorService(Service):

    name = 'calculator_service'
    version = 1

    action_map = {
            'add': AddAction,
            'subtract': SubtractAction,
            'divide': DivideAction,
    }


class CalculatorServiceV2(CalculatorService):
    version = 2
    action_map = {
            'multiply': MultiplyAction,
            'subtract': BackwardSubtractAction,
    }
