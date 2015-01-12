import pytest
import random

import servant.fields

from servant.client import Client
from servant.service.actions import Action
from servant.service.base import Service

# use a singleton client
__client = None


class DoSomethingAction(Action):
    name = servant.fields.StringField(
            default='Test Service',
            in_response=True,
            required=True,
    )
    age = servant.fields.IntField(in_response=True)

    def run(self):
        if not self.age:
            self.age = random.randint(0, 100)


class TestService(Service):
    name = 'test_service'
    version = 1

    action_map = {
            'say_name': DoSomethingAction,
    }


def pytest_configure(config):
    """Called at the start of the entire test run

    For our puposes, setup and configure the payment service so that the
    db session is bootstrapped and ready to go.

    """
    pass


@pytest.fixture
def test_client():
    global __client
    if __client is None:
        __client = Client('test_service', version=1)
        __client.configure_from_service_instance(TestService())
    return __client

