import json
from random import choice

import requests
from geopy import Nominatim

CONFIG = json.load(open('./packages/weather/package_config.json'))
ANSWERS = json.load(open(CONFIG['python_datas']['answers']))['weather']

def get_weather(entities):
    location_name = None

    for item in entities:
        if item['name'] == 'location':
            location_name = item['value']
            break

    if not location_name:
        return choice(ANSWERS['location_not_provided'])

    locator = Nominatim(user_agent='myGeocoder')
    location = locator.geocode(location_name)

    api_id = CONFIG['python_datas']['api_id']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_id}'

    result = json.loads(requests.get(url).text)

    current_condition = result['weather'][0]['description']

    response_string = choice(ANSWERS['weather_received'])
    response_string = response_string.replace('@city', location_name)
    response_string = response_string.replace('@weather', current_condition)

    return response_string