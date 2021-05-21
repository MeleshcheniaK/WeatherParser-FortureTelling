from datetime import datetime

import requests

import globals


# Получение прогноза 'На сегодня'
def current_forecast(city_name):
    res = requests.get(f"{globals.WEATHER_SITE}weather",
                       params={'q': city_name, 'units': 'metric', 'lang': 'ru', 'APPID': globals.APPID})
    data = res.json()
    if data['cod'] == globals.NOT_FOUND:
        current_weather = 'Такого города не существует'
    else:
        # Вывод части данных в качестве прогноза
        current_weather = f"{data['weather'][0]['description'].capitalize()}\n" \
                          f"Текущая температура: {round(data['main']['temp'])}, " \
                          f"ощущается как {round(data['main']['feels_like'])}\n" \
                          f"Колебание от {data['main']['temp_min']} до {data['main']['temp_max']}\n" \
                          f"Рассвет - " \
                          f"{datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')[11:16]}," \
                          f" закат - {datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')[11:16]}"

    return current_weather


# Получение прогноза 'На 5 дней'
def future_forecast(city_name):
    res = requests.get(f"{globals.WEATHER_SITE}forecast",
                       params={'q': city_name, 'units': 'metric', 'lang': 'ru', 'APPID': globals.APPID})
    data = res.json()

    forecast = 'Сегодня:\n'
    if data['cod'] == globals.NOT_FOUND:
        forecast = 'Такого города не существует'
    else:
        # Вывод части данных в качестве прогноза
        for single_hour_forecast in data['list']:
            if (single_hour_forecast['dt_txt'])[11:16] == '00:00':
                forecast += f"{(single_hour_forecast['dt_txt'])[0:10]}:\n"
            forecast += f"\t{(single_hour_forecast['dt_txt'])[11:16]}" \
                        f" {'{0:+3.0f}'.format(single_hour_forecast['main']['temp'])}" \
                        f" {single_hour_forecast['weather'][0]['description']}\n"

    return forecast
