import http.client
import json
from collections import namedtuple

# REFACTOR THIS TO JUST LOAD CITY COORDINATES!!!

CityCoord = namedtuple('CityCoord', 'lon lat')
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

#add types!
# maybe have one connection and pass it in?
def get_city_coord(city):
    connection = http.client.HTTPConnection('api.openweathermap.org', 80, timeout=10)
    # handle connection failure? raise an exception!
    path = '/geo/1.0/direct?q={city_name}&limit=5&appid={API_key}'.format(city_name = city, API_key=API_KEY)
    connection.request('GET', path)
    response = connection.getresponse()
#    print("Status: {} and reason: {} and body {}".format(response.status, response.reason, response.read()))
    response_dict = json.loads(response.read())
#    print("lon: {}, lat: {}".format(response_dict[0]['lon'], response_dict[0]['lat']))
    connection.close()
    return CityCoord(response_dict[0]['lon'], response_dict[0]['lat'])

# we only keep humidity, temp, feels_liks
def get_forecast(city_coord):
    connection = http.client.HTTPSConnection('api.openweathermap.org', 443, timeout=10)
    path = '/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_key}'.format(
        lat=city_coord.lat, lon=city_coord.lon, API_key=API_KEY)
    print(path)
    connection.request('GET', path)
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    response_dict = json.loads(response.read())
    connection.close()
    return response_dict

for city in CITIES:
    city_coord = get_city_coord(city)
    print(city_coord)
    print(get_forecast(city_coord))