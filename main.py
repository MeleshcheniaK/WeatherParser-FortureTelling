import codecs
import fortune
import globals
import shelve
import telebot
import weather

from telebot import types


# Ссылка на бота
bot = telebot.TeleBot(globals.TOKEN)

# База данных пользователей
users = shelve.open('users')

# Замена кнопок
def updating_main_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Узнать погоду':
        item1 = types.InlineKeyboardButton('На сегодня', callback_data='today')
        item2 = types.InlineKeyboardButton('На 5 дней', callback_data='5days')
    else:
        item1 = types.KeyboardButton('Узнать погоду')
        if str(message.chat.id) in users.dict:
            item2 = types.KeyboardButton('Отписаться')
        else:
            item2 = types.KeyboardButton('Подписаться')

    markup.add(item1, item2)

    return markup

# Действия при /start
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = updating_main_markup(message)

    bot.send_message(message.chat.id,
                     'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы рассказывать вам о погоде и не только).'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

# Действия при любом другом сообщении
@bot.message_handler(content_types=['text'])
def processing(message):
    if globals.CITY_ENTER == 1:
        # При вводе названия города для режима "На сегодня"
        bot.send_message(message.chat.id, weather.current_forecast(message.text))
        globals.CITY_ENTER = 0
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id, "Я снова готов к работе)", parse_mode='html', reply_markup=markup)
    elif globals.CITY_ENTER == 2:
        # При вводе названия города для режима "На 5 дней"
        bot.send_message(message.chat.id, weather.future_forecast(message.text))
        globals.CITY_ENTER = 0
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id, "Я снова готов к работе)", parse_mode='html', reply_markup=markup)
    elif message.text == 'Подписаться':
        # При выборе функции "Подписаться"
        users.dict[str(message.chat.id)] = ''
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Теперь вы подписаны, {0.first_name})'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'Отписаться':
        # При выборе функции "Отписаться"
        del users[str(message.chat.id)]
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Возвращайтесь поскорей, {0.first_name})'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'Узнать погоду':
        # При выборе функции "Узнать погоду"
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Теперь выберите режим'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'На сегодня':
        # При выборе функции "На сегодня"
        bot.send_message(message.chat.id,
                         'Введите название города'.format(message.from_user))
        globals.CITY_ENTER = 1
    elif message.text == 'На 5 дней':
        # При выборе функции "На 5 дней"
        bot.send_message(message.chat.id,
                         'Введите название города'.format(message.from_user))
        globals.CITY_ENTER = 2
    elif message.text[-1] == '?':
        # При вводе вопросе
        answer = fortune.get_answer()
        if str(message.chat.id) in users:
            user_info = codecs.decode(users.dict[str(message.chat.id)], 'UTF-8')
            user_info += f"{message.text}\n{answer}\n"
            print(user_info)
            users.dict[str(message.chat.id)] = user_info
        bot.send_message(message.chat.id, answer)
    else:
        # При вводе случайного сообщения
        bot.send_message(message.chat.id, 'Я предпочту сохранить молчание')

    # Обновление базы данных
    users.sync()

# Запуск бота
bot.polling(none_stop=True)
