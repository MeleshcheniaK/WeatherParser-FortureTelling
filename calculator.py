import json

import requests
from decouple import config

import globals

gender_coefficient = {'м': '0.7', 'ж': '0.6'}


def calculate_alco(data):
    info = data.text.split()
    if len(info) != globals.INFO_SIZE:
        return 'Неправильный ввод'
    gender, weight, height, degree, ml = info
    params = {'action': 'drink_count', 'nonce': '2bc79bc186',
              'data': f"gender={gender_coefficient[gender]}&weight={weight}&height={height}&drink1={degree}"
                      f"&amount1={ml}&drink2=0&amount2=0&drink3=0&amount3=0&gstr=3", 'dataType': 'json'}

    response = requests.post(globals.HREF, data=params,
                             headers={'Host': 'alcofan.com', 'User-Agent': config('User-Agent')})

    # Проверка на наличие ошибок
    if response.status_code == globals.SECURITY_ERROR:
        result = response.text
    else:
        result = f"В выдыхаемом воздухе -- {json.loads(response.text)[1]} мг/л\n" \
                 f"Указанная концентрация соответствует {json.loads(response.text)[2]}\n" \
                 f"Время выведения из организма {json.loads(response.text)[3]}"

    return result
