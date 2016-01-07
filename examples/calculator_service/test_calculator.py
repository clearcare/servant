import servant.client


def get_client(version=1):
    client = servant.client.Client('calculator_service', version=version)
    # Uncomment this line and change the connection settings in order to hit an HTTP version of the
    # service
    client.configure('http', host='192.168.88.100', port=8888)
    return client


def _handle_error(response):
    print response.errors, response.field_errors


def do_add():
    client = get_client()
    response = client.add(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_subtract():
    client = get_client()
    response = client.subtract(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_divide():
    client = get_client()
    response = client.divide(numerator=100, denominator=6)
    # Here are some examples of requests which throw errors
    #response = client.divide(numerator=100, denominator=0)
    #response = client.divide(numerator=100, denominator='abc')

    if response.is_error():
        _handle_error(response)
    else:
        print '%s / %s = %s' % (response.numerator, response.denominator, response.quotient)

def do_multiply():
    """Multiply only exists in version 2 of the service"""
    client = get_client(version=2)
    response = client.multiply(number1=12, number2=12)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


do_divide()
do_multiply()
