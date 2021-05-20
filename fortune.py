import globals
import time
from selenium import webdriver

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

# Подключение к сайту
def parse():
    html = get_html(globals.URL)
    if html.status_code == 200:
        get_answer(html.text)
    else:
        print('Error')
