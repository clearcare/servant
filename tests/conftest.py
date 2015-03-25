import pytest
import random

import servant.fields

from servant.client import Client
from servant.service.actions import Action
from servant.service.base import Service


class SayNameAction(Action):
    name = servant.fields.StringField(
            default='Test Service',
            in_response=True,
            required=True,
    )
    age = servant.fields.IntField(in_response=True)

    def run(self):
        if not self.age:
            self.age = random.randint(0, 100)


class DoubleAction(Action):
    amount = servant.fields.DecimalField(
            required=True,
    )
    result = servant.fields.DecimalField(
            in_response=True,
    )
    create_error = servant.fields.BooleanField(
            default=False
    )

    def run(self, **kwargs):
        if self.create_error:
            raise ServantException('Purposeful error!')

        self.result = self.amount * 2


operators = ('+', '-', '*', '/')

class CalculatorAction(Action):
    amount1 = servant.fields.DecimalField(
            required=True,
    )
    amount2 = servant.fields.DecimalField(
            required=True,
    )
    operator = servant.fields.StringField(
            required=True,
            choices=operators,
    )
    result = servant.fields.DecimalField(
            in_response=True,
    )
    double_result = servant.fields.DecimalField(
            in_response=True,
    )
    error_type = servant.fields.StringField(
            choices=('EXCEPTION', 'WARN'),
    )
    suberror = servant.fields.BooleanField(
            default=False,
    )

    def calculate(self):
        if self.operator == '+':
            return self.amount1 + self.amount2
        elif self.operator == '-':
            return self.amount1 - self.amount2
        elif self.operator == '*':
            return self.amount1 * self.amount2
        elif self.operator == '/':
            return self.amount1 / self.amount2

    def run(self):
        create_error = False

        self.result = self.calculate()
        amount_to_double = self.result

        if self.error_type == 'WARN':
            self.add_error('this is a warning', 'WARNING')

        if self.suberror:
            amount_to_double = None
            create_error = True

        internal_client = self.get_internal_client(do_begin_response=True)
        response = internal_client.double(amount=amount_to_double, create_error=create_error)
        #import pdb; pdb.set_trace()
        if not response.is_error():
            self.double_result = response.result
        else:
            print 'suberrors'
            print response.text
            print


class TestService(Service):
    name = 'test_service'
    version = 1

    action_map = {
            'say_name': SayNameAction,
            'double': DoubleAction,
            'calculate': CalculatorAction,
    }


def pytest_configure(config):
    """Called at the start of the entire test run

    For our puposes, setup and configure the payment service so that the
    db session is bootstrapped and ready to go.

    """
    pass


@pytest.fixture(scope="module")
def test_client():
    client = Client('test_service', version=1)
    client.configure_from_service_instance(TestService())
    return client
