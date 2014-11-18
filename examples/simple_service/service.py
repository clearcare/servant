from servant.service import Service

from servant.service.actions import (
        Action,
        stdactions,
)
import servant.fields

import requests


class WeatherSearchAction(Action):

    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

    city = servant.fields.StringField(
            max_length=64,
    )

    def run(self, **kwargs):
        return {u'clouds': {u'all': 1}, u'name': u'Denver', u'coord': {u'lat': 39.74, u'lon': -104.98}, u'sys': {u'country': u'US', u'sunset': 1416354111, u'message': 0.0207, u'type': 1, u'id': 538, u'sunrise': 1416318520}, u'weather': [{u'main': u'Clear', u'id': 800, u'icon': u'01n', u'description': u'sky is clear'}], u'cod': 200, u'base': u'cmc stations', u'dt': 1416288900, u'main': {u'pressure': 1021, u'humidity': 63, u'temp_max': 273.15, u'temp': 269.26, u'temp_min': 266.15}, u'id': 5419384, u'wind': {u'speed': 5.7, u'deg': 300}}
        response = requests.get(
                WeatherSearchAction.WEATHER_URL,
                params={'q': '%s,us' % self.city}
        )
        return response.json()


class SimpleService(Service):

    name = 'simple_service'
    version = 1

    action_map = {
            'echo': stdactions.EchoAction,
            'ping': stdactions.PingAction,
            'get_weather': WeatherSearchAction,
    }
