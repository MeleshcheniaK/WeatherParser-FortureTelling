import globals
import requests
import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(r'D:\Informatic\Python\Bot/chromedriver', chrome_options=options)


def get_html(url):
    r = requests.get(url)
    return r


def get_answer():
    driver.get(globals.URL)
    time.sleep(1)
    element = driver.find_element_by_class_name('ball-text')
    element.click()
    time.sleep(1)
    element = driver.find_element_by_class_name('ball-text').text
    return element


def parse():
    html = get_html(globals.URL)
    if html.status_code == 200:
        get_answer(html.text)
    else:
        print('Error')
