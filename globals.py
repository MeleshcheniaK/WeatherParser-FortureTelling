from decouple import config

# Appid для сайта с прогнозом погоды
APPID = config('APPID')

# Начальное состояние конечного автомата
CITY_ENTER = 0

# Token для TelegramBot
TOKEN = config('TOKEN')

# Ссылка на сайт с предсказаниями
URL = 'https://8-gund.com/ru/'

# Ссылка на сайт с прогнозом погоды
WEATHER_SITE = 'http://api.openweathermap.org/data/2.5/'

# Ссылка на сайт с калькулятором
HREF = 'https://alcofan.com/wp-admin/admin-ajax.php'

# Ссылка на сайт с картинками
PICTURES = 'https://castlots.org/img/kamasutra/'

# Код ошибки
NOT_FOUND = '404'

# Начало нового дня
START_TIME = '00:00'

# Паттерн для получения данных json строки
START_PATTERN = 11
END_PATTERN = 16
DATE_SIZE = 10

# Формат получения даты
DATA_FORMAT = '%Y-%m-%d %H:%M:%S'

# Размер данных для калькулятора
INFO_SIZE = 5

# Код ошибки доступа
SECURITY_ERROR_TEXT = "Ошибка проверки безопасности!"
