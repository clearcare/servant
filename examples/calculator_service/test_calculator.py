import servant.client

calc_client = servant.client.Client('calculator_service', version=1)
simple_client = servant.client.Client('simple_service', version=1)
calc_client2 = servant.client.Client('calculator_service', version=2)

# Uncomment this line and change the connection settings in order to hit an HTTP version of the
# service
# client.configure('http', host='192.168.88.100', port=8888)

def _handle_error(response):
    print response.errors, response.field_errors


def do_add(client):
    response = client.add(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_subtract(client):
    response = client.subtract(number1=10, number2=15)

    if response.is_error():
        _handle_error(response)
    else:
        print response.result


def do_divide(client):
    response = client.divide(numerator=100, denominator=6)
    # Here are some examples of requests which throw errors
    #response = client.divide(numerator=100, denominator=0)
    #response = client.divide(numerator=100, denominator='abc')

    if response.is_error():
        _handle_error(response)
    else:
        print '%s / %s = %s' % (response.numerator, response.denominator, response.quotient)

def do_multiply(client):
    response = client.multiply(number1=12, number2=12)

    if response.is_error():
        print response.errors
    else:
        print response.result


calc_client.configure('http', host='192.168.88.100', port=8888)
calc_client2.configure('http', host='192.168.88.100', port=8888)

do_divide(calc_client)

#response = simple_client.get_theater_listing(theater_id=123)
#if not response.is_error():
#    for movie in response.movies:
#        print movie
#else:
#    print response.text
#

do_add(calc_client2)
#calc_client2.service_name = 'fooely'
#do_multiply(calc_client2)
