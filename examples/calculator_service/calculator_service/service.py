from servant.service.base import Service

import actions


class CalculatorService(Service):

    name = 'calculator_service'
    version = 1

    action_map = {
            'add': actions.AddAction,
            'subtract': actions.SubtractAction,
            'divide': actions.DivideAction,
    }


class CalculatorServiceV2(CalculatorService):
    version = 2
    action_map = {
            'multiply': actions.MultiplyAction,
            'subtract': actions.BackwardSubtractAction,
    }
