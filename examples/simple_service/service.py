import time
import requests

from datetime import datetime

import servant.fields

from servant.service.base import Service
from servant.service.actions import (
        Action,
        stdactions,
)

from schematics.exceptions import ValidationError

def now():
    return time.time()


class WeatherSearchAction(Action):

    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
    city = servant.fields.StringField(
            max_length=64,
    )

    def run(self, **kwargs):
        response = requests.get(
                WeatherSearchAction.WEATHER_URL,
                params={'q': '%s,us' % self.city}
        )
        return response.json()


_fake_response = {u'calctime': 0.8057,
 u'city_id': 2885679,
 u'cnt': 2,
 u'cod': u'200',
 u'list': [{u'clouds': {u'all': 90},
            u'dt': 1416331494,
            u'main': {u'humidity': 75,
                      u'pressure': 1009,
                      u'temp': 279.92,
                      u'temp_max': 281.15,
                      u'temp_min': 278.85},
            u'weather': [{u'description': u'light rain',
                          u'icon': u'10n',
                          u'id': 500,
                          u'main': u'Rain'}],
            u'wind': {u'deg': 0, u'speed': 1}},
           {u'clouds': {u'all': 75},
            u'dt': 1416340783,
            u'main': {u'humidity': 93,
                      u'pressure': 1011,
                      u'temp': 279.63,
                      u'temp_max': 282.15,
                      u'temp_min': 278.15},
            u'weather': [{u'description': u'broken clouds',
                          u'icon': u'04n',
                          u'id': 803,
                          u'main': u'Clouds'}],
            u'wind': {u'deg': 180.009, u'speed': 1.11}}],
 u'message': u''}


class HistoricalWeatherSearchAction(Action):

    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/history/city'

    # input only fields
    city_id = servant.fields.IntField(
            required=True,
    )
    make_real_request = servant.fields.BooleanField(
            default=False,
    )

    # input and output fields
    start_time = servant.fields.IntField(
            required=True,
            in_response=True,
    )
    end_time = servant.fields.IntField(
            default=now,
            in_response=True,
    )

    # output only fields
    city_name = servant.fields.StringField(
            in_response=True,
            max_length=40,
    )
    #calctime = servant.fields.DecimalField(
    calctime = servant.fields.FloatField(
            serialized_name='response_time',
            in_response=True,
    )

    def validate_start_time(self, data, value):
        if data['start_time'] >= data['end_time']:
            raise ValidationError(u'start_time must be before end_time')
        return value

    def run(self, **kwargs):
        """Main entry point to entire service."""
        if self.make_real_request:
            resp = self._make_request()
        else:
            resp = _fake_response
        self.city_name = self.get_city_name_by_id(self.city_id)
        self.calctime = resp['calctime']

    def get_city_name_by_id(self, city_id):
        db = {2885679: 'Denver'}
        return db.get(city_id, 'Unknown City')

    def _make_request(self):
        response = requests.get(
                HistoricalWeatherSearchAction.WEATHER_URL,
                params={
                    'id': self.city_id, 'type': 'hour',
                    'start': self.start_time, 'end': self.end_time
                }
        )
        return response.json()


class MovieField(Action):
    name = servant.fields.StringField()
    director = servant.fields.StringField()
    release_date = servant.fields.DateTimeField()


class TheaterListingAction(Action):

    theater_id = servant.fields.IntField(
            required=True,
    )
    theater_name = servant.fields.StringField(
            in_response=True,
    )
    movies = servant.fields.ListField(
            servant.fields.ModelField(MovieField),
            in_response=True,
    )

    def get_movies_from_db(self, theater_id):
        return [
                MovieField(
                    {'name': 'Intersteller',
                    'director': 'Christopher Nolan',
                    'release_date': datetime(2014, 11, 1)}
                ),
                MovieField(
                    {'name': 'Dumb and Dumber To',
                    'director': 'Peter Farrelly, Bobby Farrelly',
                    'release_date': datetime(2014, 11, 5)},
                ),
        ]

    def run(self, **kwargs):
        self.movies = self.get_movies_from_db(self.theater_id)
        return {
                'theater_name': u'Cinemark Fort Collins 16',
                'movies': self.movies,

        }



class SimpleService(Service):

    name = 'simple_service'
    version = 1

    action_map = {
            'echo': stdactions.EchoAction,
            'ping': stdactions.PingAction,
            'get_weather': WeatherSearchAction,
            'get_historical_weather': HistoricalWeatherSearchAction,
            'get_theater_listing': TheaterListingAction,
    }


if __name__ == '__main__':
    server = HttpService()
    server.serve_forever()
