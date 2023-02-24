
import json
from urllib.request import urlopen

import errors_myweather


ENDPOINT_URL = 'https://api.openweathermap.org/data/2.5/weather?{params}'
api_key = '8dc0df3cbbb6a97697a2c746dfeed73f'


def req_url(**kwargs):
    """Make resuling url for GET req to the ENDPOINT."""
    params = '&'.join([f'{k}={v}' for k, v in kwargs.items()])
    return ENDPOINT_URL.format(params=params)


def get_curtemp(response):
    """Get current temperature from parsed JSON."""
    current = response['main']
    current_temp = float(round((current['temp'] - 273.15), 2))
    return current_temp


def get_feels_like_temp(response):
    """Get current temperature from parsed JSON."""
    current = response['main']
    feels_like_temp = float(round((current['feels_like'] - 273.15), 2))
    return feels_like_temp


def make_request(url):
    response = urlopen(url)
    data = response.read()
    data = data.decode('utf-8')
    res = json.loads(data)
    return res


def request_curtemp(lon, lat):
    url = req_url(lon=lon, lat=lat, appid='8dc0df3cbbb6a97697a2c746dfeed73f')
    resp = make_request(url)
    temp = get_curtemp(resp)
    return temp


def request_feels_like_temp(lon, lat):
    url = req_url(lon=lon, lat=lat, appid='8dc0df3cbbb6a97697a2c746dfeed73f')
    resp = make_request(url)
    feels_like_temp = get_feels_like_temp(resp)
    return feels_like_temp


GEO_URL = ('https://openweathermap.org/data/2.5/find?q={city}&'
           'appid=439d4b804bc8187953eb36d2a8c26a02&units=metric')


def get_coords(city):
    url = GEO_URL.format(city=city)
    data = make_request(url)
    data = data['list']
    try:
        city = data[0]['name']
        lat = data[0]['coord']['lat']
        lon = data[0]['coord']['lon']
    except IndexError:
        raise errors_myweather.CityNotFoundError()
    return (city, lon, lat)


USAGE = 'USAGE: {prog} CITY\nGet current temperature.'


class City():
    def __init__(self, city):
        self.city = city

    def main(self):
        city = self.city
        city, lon, lat = get_coords(city)
        temp = request_curtemp(lon, lat)
        _deg = '\u00b0'
        print(f'Currently temperature in {city} is {temp} {_deg}C')

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, val):
        if val.isalpha():
            self._city = val
        else:
            raise errors_myweather.CityNameError()


class Weather(City):

    def feels_like(self):
        city = self.city
        city, lon, lat = get_coords(city)
        temp = request_curtemp(lon, lat)
        feels_like_temp = request_feels_like_temp(lon, lat)
        _deg = '\u00b0'
        print(f'Currently temperature in {city} is {temp} {_deg}C'
              f' and feels like temperature is {feels_like_temp} {_deg}C.')
