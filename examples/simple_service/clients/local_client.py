import sys
sys.path.append('../../')

from simple_service.service import SimpleService

service = SimpleService()

client = service.get_client()

#print client.ping()
#print client.echo(name='brianz')
#print client.echo(name='brianz', age=41, is_awesome=True)
print client.get_weather(city='denver')
