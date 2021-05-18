from decouple import config

# Appid для сайта с прогнозом погоды
APPID = config('APPID')

# Token для TelegramBot
TOKEN = '*'
# Начальное состояние конечного автомата
CITY_ENTER = 0
# Ссылка на сайт с пресказаниями
STATE = 0

# Ссылка на сайт с предсказаниями
URL = 'https://8-gund.com/ru/'

# Ссылка на сайт с прогнозом погоды
WEATHER_SITE = 'http://api.openweathermap.org/data/2.5/'

# Ссылка на сайт с калькулятором
HREF = "https://alcofan.com/wp-admin/admin-ajax.php"

# Код ошибки
ERROR_CODE = '404'

# Начало нового дня
START_TIME = '00:00'

# Паттерн для получения данных json строки
START_PATTERN = 11
END_PATTERN = 16
DATE_SIZE = 10

# Формат получения даты
DATA_FORMAT = '%Y-%m-%d %H:%M:%S'
