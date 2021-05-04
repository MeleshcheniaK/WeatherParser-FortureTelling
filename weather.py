import globals
import requests

from datetime import datetime


def current_forecast(city_name):
    res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                       params={'q': city_name, 'units': 'metric', 'lang': 'ru', 'APPID': globals.APPID})
    data = res.json()
    if data['cod'] == '404':
        current_weather = 'Такого города не существует'
    else:
        current_weather = f"{data['weather'][0]['description'].capitalize()}\n" \
                          f"Текущая температура: {round(data['main']['temp'])}, ощущается как {round(data['main']['feels_like'])}\n" \
                          f"Колебание от {data['main']['temp_min']} до {data['main']['temp_max']}\n" \
                          f"Рассвет - {datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')[11:16]}," \
                          f" закат - {datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')[11:16]}"

    return current_weather


def future_forecast(city_name):
    res = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                       params={'q': city_name, 'units': 'metric', 'lang': 'ru', 'APPID': globals.APPID})
    data = res.json()

    forecast = 'Сегодня:\n'
    if data['cod'] == '404':
        forecast = 'Такого города не существует'
    else:
        for i in data['list']:
            if (i['dt_txt'])[11:16] == '00:00':
                forecast += f"{(i['dt_txt'])[0:10]}:\n"
            forecast += f"\t{(i['dt_txt'])[11:16]} {'{0:+3.0f}'.format(i['main']['temp'])} {i['weather'][0]['description']}\n"

    return forecast
