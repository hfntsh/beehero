import http.client
import json
from collections import namedtuple
from city import City
from forecast import Forecast
from base import Base, Session, engine


CityCoord = namedtuple('CityCoord', 'lon lat')
RawForecast = namedtuple('Forecast', 'temperature humidity feels_like')
# connect to API
# get data
# load to DB

# Ideally this would be managed by some secret management service
# or at least export from env variables - how to do that in docker?
# this is the appid param
#this is for the one from the assignment
#API_KEY = '8133004a923c6f2812a3c9b28d099e08'

#this is for weatherapi.com
API_KEY = 'e2e4d1f7b56340179b6232406221903'

# first obtain lon, lat

CITIES = ['Jerusalem', 'Haifa', 'Tel-Aviv', 'Eilat', 'Tiberias']

# we only keep humidity, temp, feels_liks
def get_forecast(city):
    connection = http.client.HTTPConnection('api.weatherapi.com', 80, timeout=10)
    path = '/v1/forecast.json?key={API_key}&q={city_name}&days=4&aqi=no&alerts=no'.format(
        city_name=city, API_key=API_KEY)
    print(path)
    connection.request('GET', path)
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    response_dict = json.loads(response.read())
    output_dict = {}
    for day in response_dict['forecast']['forecastday']:
        for hour in day['hour']:
            # use datetime? YES
            output_dict[hour['time_epoch']] = RawForecast(hour['temp_c'], hour['humidity'], hour['feelslike_c'])
    connection.close()
    return output_dict



Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

for city in CITIES:
    forecasts = get_forecast(city)
    print(city)
    print(forecasts)
    for datetime, forecast in forecasts.items():
        session.add(Forecast(, city_coord.lon, city_coord.lat))
session.commit()
session.close()
