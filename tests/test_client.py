import pytest

from servant.client import Client

# the calculator service lives in the examples/ directory and is installed automatically when
# running tests via tox
@pytest.fixture
def clientv1():
    return Client('calculator_service', version=1)

@pytest.fixture
def clientv2():
    return Client('calculator_service', version=2)


def test_calculator_v1(clientv1):
    response = clientv1.subtract(number1=11, number2=2)
    assert not response.is_error()
    assert response.result == 9

def test_calculator_v1_no_multiply(clientv1):
    response = clientv1.multiply(number1=10, number2=20)
    assert response.is_error()
    assert response.errors == [u'No action named "multiply" found']


def test_calculator_v2_add(clientv2):
    response = clientv2.add(number1=10, number2=22)
    assert not response.is_error()
    assert response.result == 32

def test_calculator_v2_divide(clientv2):
    response = clientv2.divide(numerator=10, denominator=2)
    assert not response.is_error()
    assert response.quotient == 5

def test_calculator_v2_multiply(clientv2):
    response = clientv2.multiply(number1=10, number2=20)
    assert not response.is_error()
    assert response.result == 200

def test_calculator_v2_subtract_has_been_overriden(clientv2):
    response = clientv2.subtract(number1=11, number2=2)
    assert not response.is_error()
    assert response.result == -9


def test_client_version():
    client = Client('foo', version=1)
    assert client.service_version == 1

def test_client_service_version():
    # test that service_version raises a deprecation warning
    pytest.deprecated_call(Client, 'foo', service_version=1)

def test_invalid_version():
    client = Client('calculator_service', version=3)
    with pytest.raises(Exception) as execinfo:
        client.add(number1=10, number2=22)

    assert 'Could not find appropriate Service class' in str(execinfo.value)
