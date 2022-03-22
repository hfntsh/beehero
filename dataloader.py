import http.client
import json
from datetime import datetime
from collections import namedtuple
from city import City
from forecast import Forecast
from base import Base, Session, engine


CityCoord = namedtuple('CityCoord', 'lon lat')
RawForecast = namedtuple('Forecast', 'temperature humidity feels_like')

CITY_API_KEY = '8133004a923c6f2812a3c9b28d099e08'

WEATHER_API_KEY = 'e2e4d1f7b56340179b6232406221903'

CITIES = ['Jerusalem', 'Haifa', 'Tel-Aviv', 'Eilat', 'Tiberias']

def get_city_coord(city):
    connection = http.client.HTTPConnection('api.openweathermap.org', 80, timeout=10)
    # handle connection failure? raise an exception!
    path = '/geo/1.0/direct?q={city_name}&limit=5&appid={API_key}'.format(city_name = city, API_key=CITY_API_KEY)
    connection.request('GET', path)
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    # need to fail loudly if request failed
    response_dict = json.loads(response.read())
#    print("lon: {}, lat: {}".format(response_dict[0]['lon'], response_dict[0]['lat']))
    connection.close()
    return CityCoord(response_dict[0]['lon'], response_dict[0]['lat'])

def get_forecast(city):
    connection = http.client.HTTPConnection('api.weatherapi.com', 80, timeout=10)
    path = '/v1/forecast.json?key={API_key}&q={city_name}&days=4&aqi=no&alerts=no'.format(
        city_name=city, API_key=WEATHER_API_KEY)
    print(path)
    connection.request('GET', path)
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    response_dict = json.loads(response.read())
    output_dict = {}
    for day in response_dict['forecast']['forecastday']:
        for hour in day['hour']:
            # use datetime? YES
            output_dict[hour['time']] = RawForecast(hour['temp_c'], hour['humidity'], hour['feelslike_c'])
    connection.close()
    return output_dict


Base.metadata.create_all(engine)

session = Session()

for index, city_name in enumerate(CITIES):
    city_coord = get_city_coord(city_name)
    print(city_coord)
    city = City(city_name, city_coord.lon, city_coord.lat)
    city.id = index
    session.add(city)
    forecasts = get_forecast(city_name)
    for date_string, forecast in forecasts.items():
        # There's a subtle issue here - we're gonna store the datetime in the timezone which we queried from.
        # probably good enough.
        date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        forecast = Forecast(date_object, forecast.humidity, forecast.temperature, forecast.feels_like)
        forecast.city_id = city.id
        session.add(forecast)

session.commit()
session.close()
