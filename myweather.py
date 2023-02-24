
import json
from urllib.request import urlopen

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


GEO_URL = ('https://openweathermap.org/data/2.5/find?q={city}&'
           'appid=439d4b804bc8187953eb36d2a8c26a02&units=metric')


def get_coords(city):
    url = GEO_URL.format(city=city)
    data = make_request(url)
    data = data['list']
    # set to new, could differ as city is the first match
    # of search results
    city = data[0]['name']
    lat = data[0]['coord']['lat']
    lon = data[0]['coord']['lon']
    return (city, lon, lat)


USAGE = 'USAGE: {prog} CITY\nGet current temperature.'


def main(args):
    prog, *args = args
    if len(args) != 1:
        exit(USAGE.format(prog=prog))
    city = args[0]
    city, lon, lat = get_coords(city)
    temp = request_curtemp(lon, lat)
    _deg = '\u00b0'
    print(f'Currently temperature in {city} is {temp} {_deg}C')


if __name__ == '__main__':
    import sys
    main(sys.argv)


def __simpltest():
    indata = r'''{"coord":{"lon":30.52,"lat":50.45},"weather":[{"id":804,'
    '"main":"Clouds","description":"overcast clouds","icon":"04n"}],'
    '"base":"stations","main":{"temp":277.21,"feels_like":273.94,'
    '"temp_min":276.04,"temp_max":277.21,"pressure":1005,"humidity":72},'
    '"visibility":10000,"wind":{"speed":3.86,"deg":274,"gust":9.16},"clouds":{"all":100},"dt":1676821295,'
    '"sys":{"type":2,"id":2003742,"country":"UA","sunrise":1676782986,"sunset":1676820049},"timezone":7200,'
    '"id":696050,"name":"Pushcha-Vodytsya","cod":200}'''
    assert get_curtemp(json.loads(indata)) == 4.06
    params = dict(lat=50.45, lon=30.52, appid=api_key)
    r = req_url(**params)
    expected_url = 'https://api.openweathermap.org/data/2.5/weather?'
    'lat=50.45&lon=30.52&appid=8dc0df3cbbb6a97697a2c746dfeed73f'
    assert r == expected_url, 'Wrong url gen'
    make_request(r)
    main(...)
    print(get_coords('kyiv'))
