import os
import time

from selenium import webdriver

import globals

# Подключение веб-браузера
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(f'{os.path.dirname(os.path.abspath(__file__))}/ChromeDriver/chromedriver',
                          chrome_options=options)


# Получение ответа от шара
def get_orb_answer():
    driver.get(globals.URL)
    time.sleep(1)
    element = driver.find_element_by_class_name('ball-text')
    element.click()
    time.sleep(1)
    element = driver.find_element_by_class_name('ball-text').text
    return element
