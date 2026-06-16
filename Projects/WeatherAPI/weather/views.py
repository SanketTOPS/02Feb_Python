import json
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.shortcuts import render

API_KEY = 'a27f25987ccfcb14814c14aa045bf860'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

WEATHER_ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Smoke': '💨',
    'Haze': '🌫️',
    'Fog': '🌫️',
    'Dust': '🌪️',
    'Sand': '🏜️',
    'Ash': '🌋',
    'Squall': '🌬️',
    'Tornado': '🌪️',
}


def fetch_weather(city: str) -> dict:
    query = urlencode({
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
    })
    url = f'{BASE_URL}?{query}'

    try:
        with urlopen(url, timeout=10) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except HTTPError as exc:
        return {'error': f'Weather API returned HTTP {exc.code}. Please try another city.'}
    except URLError as exc:
        return {'error': f'Unable to reach weather service: {exc.reason}'}
    except Exception as exc:
        return {'error': f'Unexpected error: {exc}'}


def home(request):
    city = request.GET.get('city', 'Rajkot').strip() or 'Rajkot'
    weather = fetch_weather(city)

    weather_icon = '🔎'
    if isinstance(weather, dict) and not weather.get('error'):
        main_condition = weather.get('weather', [{}])[0].get('main', '')
        weather_icon = WEATHER_ICONS.get(main_condition, '🌈')
    # Prepare simple, preformatted strings for the template to avoid complex inline filters
    temp = None
    feels = None
    description = ''
    condition_main = ''
    if isinstance(weather, dict) and not weather.get('error'):
        main = weather.get('main', {})
        temp = main.get('temp')
        feels = main.get('feels_like')
        w = weather.get('weather', [{}])[0]
        description = w.get('description', '')
        condition_main = w.get('main', '')

    temp_text = f"{temp:.1f}°C" if isinstance(temp, (int, float)) else 'N/A'
    feels_text = f"Feels like {feels:.1f}°C" if isinstance(feels, (int, float)) else 'Feels like N/A'
    description_text = description.capitalize() if description else 'Clear skies'

    context = {
        'city': city,
        'weather': weather,
        'weather_icon': weather_icon,
        'temp_text': temp_text,
        'feels_text': feels_text,
        'description_text': description_text,
        'condition_main': condition_main or 'Clear',
    }
    return render(request, 'weather/home.html', context)
