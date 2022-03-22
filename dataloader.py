"""
dataloader.py
This is a tool to load data from openweathermap.org and weatherapi.com into the database.
It doesn't do error handling on returned values and failed connections, since it is assumed to be run interactively
from shell by a user, so crashing back to the shell is acceptable.
"""


import http.client
import json
from datetime import datetime
from collections import namedtuple

from base import Base, Session, engine
from city import City
from forecast import Forecast


CityCoord = namedtuple('CityCoord', 'lon lat')
RawForecast = namedtuple('Forecast', 'temperature humidity feels_like')

# Ideally these would live in some secret manager.
CITY_API_KEY = '8133004a923c6f2812a3c9b28d099e08'
WEATHER_API_KEY = 'e2e4d1f7b56340179b6232406221903'

CITIES = ['Jerusalem', 'Haifa', 'Tel-Aviv', 'Eilat', 'Tiberias']

def get_city_coord(city: str):
    """
    get_city_coord
        Fetches city coordinates from openweathermap API
    :param city: string, city name, assumed to be a name recognized by openweathermap.
    :return: a CityCoord namedtuple containing longtitude and latitude.
    """
    # We might want to re-use the connection across calls, though it's probably not a big deal.
    connection = http.client.HTTPConnection('api.openweathermap.org', 80, timeout=10)
    path = '/geo/1.0/direct?q={city_name}&limit=1&appid={API_key}'.format(city_name = city, API_key=CITY_API_KEY)
    connection.request('GET', path)
    response = connection.getresponse()
    response_dict = json.loads(response.read())
    connection.close()
    return CityCoord(response_dict[0]['lon'], response_dict[0]['lat'])

def get_forecast(city: str):
    """
    get_forecast
        Fetches city forecast from weatherapi.com
    :param city: string, city name, assumed to be recognized by weatherapi.com
    :return: dict, mapping each forecast report time to a RawForecast namedtuple containing temperature, humidity and
    feelslike.
    """
    connection = http.client.HTTPConnection('api.weatherapi.com', 80, timeout=10)
    path = '/v1/forecast.json?key={API_key}&q={city_name}&days={num_days}&aqi=no&alerts=no'.format(
        API_key=WEATHER_API_KEY, city_name=city, num_days=3)
    connection.request('GET', path)
    response = connection.getresponse()
    response_dict = json.loads(response.read())
    output_dict = {}
    for day in response_dict['forecast']['forecastday']:
        for hour in day['hour']:
            output_dict[hour['time']] = RawForecast(hour['temp_c'], hour['humidity'], hour['feelslike_c'])
    connection.close()
    return output_dict


Base.metadata.create_all(engine)

session = Session()

for index, city_name in enumerate(CITIES):
    city_coord = get_city_coord(city_name)
    city = City(city_name, city_coord.lon, city_coord.lat)
    city.id = index
    session.add(city)
    forecasts = get_forecast(city_name)
    for date_string, forecast in forecasts.items():
        # There's a subtle issue here - we're storing the datetime in the timezone which we queried from.
        # probably good enough.
        date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        forecast = Forecast(
            date_object.date(), date_object.time(), forecast.humidity, forecast.temperature, forecast.feels_like)
        forecast.city_id = city.id
        session.add(forecast)

session.commit()
session.close()
