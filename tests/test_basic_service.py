import pytest


def test_test_client(test_client):
    response = test_client.say_name()
    assert not response.is_error()
    assert response.name == 'Test Service'
    assert response.age >= 0
    assert response.age <= 100

def test_test_client_values(test_client):
    response = test_client.say_name(name='bz', age=41)
    assert not response.is_error()
    assert response.name == 'bz'
    assert response.age == 41


def test_test_client_errors(test_client):
    response = test_client.say_name(age='abc')
    assert response.is_error()
    assert response.field_errors.age[0].error == 'Value is not int'
    assert not response.errors
