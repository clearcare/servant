import sys
sys.path.append('../../')

import time
from pprint import pprint as pp

from simple_service.service import SimpleService

service = SimpleService()

client = service.get_client()

#print client.ping()
#print client.echo(name='brianz')
#print client.echo(name='brianz', age=41, is_awesome=True)
#print client.get_weather(city='denver', state='CO')

n = time.time() - (3600 * 4)

resp = client.get_historical_weather(
            city_id=2885679,
            start_time=n,
            make_real_request=False)
pp(resp)

#resp = client.get_theater_listing(theater_id=1234)
