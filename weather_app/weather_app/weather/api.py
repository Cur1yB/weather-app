import requests
from datetime import datetime


def get_weather(city):
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city["latitude"]}&longitude={city["longitude"]}&hourly=temperature_2m,weathercode')
    if response.status_code == 200:
        data = response.json()
        forecast = []
        hourly_data = data.get('hourly', {})
        times = hourly_data.get('time', [])
        temperatures = hourly_data.get('temperature_2m', [])
        weathercodes = hourly_data.get('weathercode', [])
        
        for time, temp, code in zip(times, temperatures, weathercodes):
            weather_description = get_weather_description(code)
            time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M')
            forecast.append({
                'time': time_obj,
                'temperature': temp,
                'description': weather_description
            })
        return forecast
    return None

def get_weather_description(code):
    weather_descriptions = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        56: 'Light freezing drizzle',
        57: 'Dense freezing drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        66: 'Light freezing rain',
        67: 'Heavy freezing rain',
        71: 'Slight snow fall',
        73: 'Moderate snow fall',
        75: 'Heavy snow fall',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail',
    }
    return weather_descriptions.get(code, 'Unknown')


def get_coordinates(city_name):
    headers = {
        'User-Agent': 'weather_app/1.0 (your.email@example.com)' 
    }
    params = {
        'q': city_name,
        'format': 'json',
        'addressdetails': 1,
    }
    response = requests.get('https://nominatim.openstreetmap.org/search', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            first_result = data[0]
            return {"latitude": float(first_result['lat']), "longitude": float(first_result['lon'])}
    return None