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
        self.city = 'denver'
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
