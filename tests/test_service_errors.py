import pytest

import servant.fields

from servant.constants import *
from servant.client import Client
from servant.exceptions import (
        ActionError,
        ActionFieldError,
        ServantException,
)
from servant.service.actions import Action
from servant.service.base import Service


class AttributeErrorAction(Action):
    def run(self):
        raise AttributeError('Unhandled exception')

class UnexpectedExceptionAction(Action):
    def run(self):
        raise Exception('Unhandled exception')

class ServantExceptionAction(Action):
    def run(self):
        raise ServantException('Purposefully raised servant exception')

class BaseErrorAction(Action):
    name = servant.fields.StringField(in_response=True, max_length=2)

class AddErrorAction(BaseErrorAction):
    def run(self):
        error = 'add error'
        self.add_error(error, 'WARNING')
        self.name = 'bz'

class AddClientErrorAction(BaseErrorAction):
    def run(self):
        error = 'add client error'
        self.add_client_error(error)
        self.name = 'bz'

class AddServerErrorAction(BaseErrorAction):
    def run(self):
        error = 'add server error'
        self.add_server_error(error, 'WARNING')
        self.name = 'bz'

class RaiseActionErrorAction(BaseErrorAction):
    def run(self):
        raise ActionError('action error')

class RaiseActionFieldErrorAction(BaseErrorAction):
    def run(self):
        raise ActionFieldError('action field error')


class AService(Service):
    name = 'a_service'
    version = 1
    action_map = {
            'attribute_error_exception': AttributeErrorAction,
            'unexpected_exception': UnexpectedExceptionAction,
            'servant_exception': ServantExceptionAction,
            'add_error': AddErrorAction,
            'add_client_error': AddClientErrorAction,
            'add_server_error': AddServerErrorAction,
            'raise_action_error': RaiseActionErrorAction,
            'raise_action_field_error': RaiseActionFieldErrorAction,
    }


@pytest.fixture
def client():
    client = Client('a_service', version=1)
    client.configure_from_service_instance(AService())
    return client


# start tests

def test_attribute_error_exception(client):
    resp = client.attribute_error_exception()
    assert resp.is_error()
    assert len(resp.errors) == 1
    assert resp.errors[0] == 'Unexpected service error: Unhandled exception'
    assert not resp.action_errors
    assert not resp.field_errors

def test_unexpected_exception(client):
    resp = client.attribute_error_exception()
    assert resp.is_error()
    assert len(resp.errors) == 1
    assert resp.errors[0] == 'Unexpected service error: Unhandled exception'
    assert not resp.action_errors
    assert not resp.field_errors

def test_servant_exception(client):
    resp = client.servant_exception()
    assert resp.is_error()
    assert len(resp.errors) == 1
    assert resp.errors[0] == 'Purposefully raised servant exception'
    assert not resp.action_errors
    assert not resp.field_errors

def test_add_error(client):
    """An error which is added by the action should be copied into the list of request errors."""
    resp = client.add_error()
    assert resp.is_error()
    assert resp.name == 'bz'
    assert len(resp.errors) == 1
    err = resp.errors[0]
    assert err == 'add error'

    assert resp.action_errors
    assert len(resp.action_errors) == 1
    action_error = resp.action_errors[0]
    assert action_error.error == 'add error'
    assert action_error.error_type == 'WARNING'
    assert action_error.hint == ''

    assert not resp.field_errors

def test_add_client_error(client):
    resp = client.add_client_error()
    assert resp.is_error()
    assert resp.name == 'bz'
    assert len(resp.errors) == 1
    err = resp.errors[0]
    assert err == 'add client error'

    assert resp.action_errors
    assert len(resp.action_errors) == 1
    action_error = resp.action_errors[0]
    assert action_error.error == 'add client error'
    assert action_error.error_type == CLIENT_ERROR
    assert action_error.hint == ''

    assert not resp.field_errors


def test_add_server_error(client):
    resp = client.add_server_error()
    assert resp.is_error()
    assert resp.name == 'bz'
    assert len(resp.errors) == 1
    err = resp.errors[0]
    assert err == 'add server error'

    assert resp.action_errors
    assert len(resp.action_errors) == 1
    action_error = resp.action_errors[0]
    assert action_error.error == 'add server error'
    assert action_error.error_type == SERVER_ERROR
    assert action_error.hint == 'WARNING'

    assert not resp.field_errors


def test_raise_action_error(client):
    """Raising an action error stops execution flow."""
    resp = client.raise_action_error()
    assert resp.is_error()
    # raising an exception means
    assert not hasattr(resp, 'name')

    assert len(resp.errors) == 1
    err = resp.errors[0]
    assert err == 'action error'

    assert resp.action_errors
    assert len(resp.action_errors) == 1
    action_error = resp.action_errors[0]
    assert action_error.error == 'action error'
    assert action_error.error_type == CLIENT_ERROR
    assert action_error.hint == ''

    assert not resp.field_errors


def test_raise_action_field_error(client):
    resp = client.raise_action_field_error(name='abcde')
    assert resp.is_error()
    assert not hasattr(resp, 'name')

    assert not resp.errors

    assert resp.action_errors
    assert len(resp.action_errors) == 1
    action_error = resp.action_errors[0]
    assert action_error.error == 'field_errors'
    assert action_error.error_type == CLIENT_ERROR
    hint = 'One or more fields did not validate. See field_errors attribute for details'
    assert action_error.hint == hint

    assert resp.field_errors
    assert len(resp.field_errors) == 1
    assert 'name' in resp.field_errors
    field_error = resp.field_errors['name']
    assert len(field_error) == 1
    field_error = field_error[0]
    assert field_error.error == 'String value is too long.'
    assert field_error.hint == 'String value is too long.'
