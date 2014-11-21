import sys
import time

import servant.client

from pprint import pprint as pp

client = servant.client.Client('simple_service', version=1)

try:
    if sys.argv[1].lower() == 'http':
        client.configure('http', host='localhost', port=8888)
except Exception:
    pass

if not client.is_configured():
    client.configure('local')

print client.ping()
print client.echo(name='brianz')
print client.echo(name='brianz', age=41, is_awesome=True)
print client.get_weather(city='denver', state='CO')

n = time.time() - (3600 * 4)

resp = client.get_historical_weather(
            city_id=2885679,
            start_time=n,
            make_real_request=False)
pp(resp)

#resp = client.get_theater_listing(theater_id=1234)
