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

class SayFullNameAction(Action):
    first_name = servant.fields.StringField(
            required=True,
    )
    last_name = servant.fields.StringField(
            required=True,
    )
    full_name = servant.fields.StringField(
            in_response=True,
    )

    def run(self, **kwargs):
        self.full_name = '%s %s' % (self.first_name.title(), self.last_name.title())



class TestService(Service):
    name = 'test_service'
    version = 1

    action_map = {
            'say_name': SayNameAction,
    }

class TestServiceV2(TestService):
    version = 2
    action_map = {
            'say_full_name': SayFullNameAction,
    }


def pytest_configure(config):
    """Called at the start of the entire test run

    For our puposes, setup and configure the payment service so that the
    db session is bootstrapped and ready to go.

    """
    pass


@pytest.fixture(scope='session')
def test_client():
    client = Client('test_service', version=1)
    client.configure_from_service_instance(TestService())
    return client


@pytest.fixture(scope='session')
def test_client_v2():
    client = Client('test_service', version=2)
    client.configure_from_service_instance(TestServiceV2())
    return client
