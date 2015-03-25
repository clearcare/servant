import pytest


def test_calculate_action(test_client):
    """double_result is calculated using an internal client to make another service call"""
    response = test_client.calculate(
            amount1=5.5,
            amount2=10.1,
            operator='*',
    )
    assert not response.is_error()
    assert response.result == 55.55
    assert response.double_result == 2*55.55


def test_calculate_action_with_sub_error(test_client):
    """Internal service call throws an error"""
    response = test_client.calculate(
            amount1=1,
            amount2=9,
            operator='+',
            error_type='SUBERROR',
    )
    assert not response.is_error()
    assert response.result == 10
    assert response.double_result == None


def test_calculate_action_with_main_error(test_client):
    response = test_client.calculate(
            amount1=10,
            amount2=0,
            operator='/',
    )
    assert response.is_error()


def test_calculate_action_with_main_error_and_sub_error(test_client):
    # make a main request with a warning
    # make internal call with error
    response = test_client.calculate(
            amount1=7.1,
            amount2=2.1,
            operator='-',
            error_type='WARN',
            suberror=True,
    )
    print response.text
    #assert response.is_error()



