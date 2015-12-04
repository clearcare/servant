import servant.client

client = servant.client.Client('calculator_service', version=1)
# Uncomment this line and change the connection settings in order to hit an HTTP version of the
# service
client.configure('http', host='192.168.88.100', port=8888)

def _handle_error(response):
    print response.errors, response.field_errors


def do_add():
    response = client.add(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_subtract():
    response = client.subtract(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_divide():
    response = client.divide(numerator=100, denominator=6)
    # Here are some examples of requests which throw errors
    #response = client.divide(numerator=100, denominator=0)
    #response = client.divide(numerator=100, denominator='abc')

    if response.is_error():
        _handle_error(response)
    else:
        print '%s / %s = %s' % (response.numerator, response.denominator, response.quotient)


do_divide()
