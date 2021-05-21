import os
import time

from selenium import webdriver

import globals

# Подключение веб-браузера
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(f'{os.path.dirname(os.path.abspath(__file__))}/ChromeDriver/chromedriver',
                          chrome_options=options)


def get_orb_answer():
    """
    Получение ответа от шара
    :return:
    """
    driver.get(globals.URL)
    time.sleep(1)
    # Поиск элемента
    orb_element_on_website = driver.find_element_by_class_name('ball-text')
    # Клик по нему
    orb_element_on_website.click()
    time.sleep(1)
    # Получение обновленного элемента
    orb_element_on_website = driver.find_element_by_class_name('ball-text').text

    return orb_element_on_website
