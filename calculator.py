import json

import requests
from decouple import config

import globals

gender_coefficient = {'м': '0.7', 'ж': '0.6'}


def calculate_alco(data):
    """
    Подсчет количества проммилей
    :param data: Параметры (пол, вес, высота, градус, мл)
    :return:
    """
    info = data.text.split()
    if len(info) != globals.INFO_SIZE:
        return 'Неправильный ввод'
    gender, weight, height, degree, ml = info
    if gender not in gender_coefficient:
        return 'Неправильный пол'
    if int(weight) < 40 or int(weight) > 150:
        return 'Неправильный вес'
    if int(height) < 120 or int(height) > 200:
        return 'Неправильный рост'
    if int(degree) < 0 or int(degree) > 100:
        return 'Неправильный градус'

    params = {'action': 'drink_count', 'nonce': config('nonce'),
              'data': f"gender={gender_coefficient[gender]}&weight={weight}&height={height}&drink1={degree}"
                      f"&amount1={ml}&drink2=0&amount2=0&drink3=0&amount3=0&gstr=3", 'dataType': 'json'}

    response = requests.post(globals.HREF, data=params,
                             headers={'Host': 'alcofan.com', 'User-Agent': config('User-Agent')})

    # Проверка на наличие ошибок
    if response.text == globals.SECURITY_ERROR_TEXT or response.status_code != 200:
        result = response.text
    else:
        result = f"В выдыхаемом воздухе -- {json.loads(response.text)[1]} мг/л\n" \
                 f"Указанная концентрация соответствует {json.loads(response.text)[2]}\n" \
                 f"Время выведения из организма {json.loads(response.text)[3]}"

    return result
