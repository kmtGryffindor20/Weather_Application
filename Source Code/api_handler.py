import requests  # The module for handling HTTP requests for an API

# The API Endpoint for the Weather Forecast Data
WEATHER_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

# The API Endpoint for the Geocoding Data
CITY_CODE_SEARCH_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"

# The API Endpoint for the Current Weather Data
CURRENT_WEATHER_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

# API Key for the openweathermap.org API
API_KEY = '455a6fc0215111908e30a79040e22dcf'

# A Session object for request pooling, helps in performance and prevents frequent request cancelling by the API host
session = requests.Session()


def get_3hour_weather_data(lat, lon):
    """Returns the forecast weather data at an interval of 3 hours for the given ``lat`` and ``lon``."""

    # The Parameters for the API call
    parameters = {
        "appid": API_KEY,
        "cnt": 3,
        "lat": lat,
        "lon": lon,
        'units': 'metric'
    }

    # Response object for this API call
    response = session.get(url=WEATHER_API_ENDPOINT, params=parameters)
    response.raise_for_status()
    print(response.url)

    # Returns the json of the response
    return response.json()


def get_current_weather_data(lat, lon):
    """Returns the current weather data for the given ``lat`` and ``lon``"""

    # Parameters for this API call
    parameters = {
        "apikey": API_KEY,
        "lat": lat,
        "lon": lon,
        'units': 'metric'
    }

    # Response object for the current weather
    response = session.get(url=CURRENT_WEATHER_API_ENDPOINT, params=parameters)
    response.raise_for_status()
    print(response.url)

    # Returns the json data
    return response.json()


def get_current_city_code(city):
    """Return the Geocoded ``lat`` and ``lon`` for the given ``city`` as a tuple. Returns ``None`` if no geocoding is
    found"""

    # Response object for the Geocoding API
    response = session.get(url=CITY_CODE_SEARCH_ENDPOINT, params={"q": city, "appid": API_KEY})
    print(response.url)
    dat = response.json()

    # Returns the Latitude and Longitude if found else returns None
    try:
        return dat[0]['lat'], dat[0]['lon']
    except KeyError:
        return None, None
    except IndexError:
        return None, None
