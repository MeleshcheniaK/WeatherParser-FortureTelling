import json

import requests
from decouple import config

import globals

gender_calc = {"м": "0.7", "ж": "0.6"}


def calculate_alco(data):
    if len(data.text.split()) != 5:
        return "Неправильный ввод"
    gender, weight, height, degree, ml = data.text.split()
    params = {"action": "drink_count", "nonce": "2bc79bc186",
              "data": "gender=" + str(gender_calc[gender]) + "&weight=" + str(weight) + "&height=" + str(
                  height) + "&drink1=" + str(degree) + "&amount1=" + str(
                  ml) + "&drink2=0&amount2=0&drink3=0&amount3=0&gstr=3", "dataType": "json"}

    response = requests.post(globals.HREF, data=params,
                             headers={'Host': 'alcofan.com', 'User-Agent': config('User-Agent')})
    result = f'В выдыхаемом воздухе -- {json.loads(response.text)[1]} мг/л\n' \
             f'Указанная концентрация соответствует {json.loads(response.text)[2]}\n' \
             f'Время выведения из организма {json.loads(response.text)[3]}'

    return result
