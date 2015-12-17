import servant.fields

from servant.exceptions import ActionError
from servant.exceptions import ServantException
from servant.service.actions import Action


class AddAction(Action):
    number1 = servant.fields.IntField(
            required=True,
    )
    number2 = servant.fields.IntField(
            required=True,
    )
    result = servant.fields.IntField(
            in_response=True,
    )

    def run(self, **kwargs):
        self.result = self.number1 + self.number2


class SubtractAction(AddAction):
    def run(self, **kwargs):
        self.result = self.number1 - self.number2


class BackwardSubtractAction(SubtractAction):
    def run(self, **kwargs):
        self.result = self.number2 - self.number1


class MultiplyAction(AddAction):
    def run(self, **kwargs):
        self.result = self.number1 * self.number2


class DivideAction(Action):
    numerator = servant.fields.DecimalField(
            required=True,
            in_response=True,
    )
    denominator = servant.fields.DecimalField(
            required=True,
            in_response=True,
    )
    quotient = servant.fields.DecimalField(
            in_response=True,
    )

    def run(self, **kwargs):
        if self.denominator == 0:
            raise ActionError('Cannot divide by zero')
        self.quotient = self.numerator / self.denominator

