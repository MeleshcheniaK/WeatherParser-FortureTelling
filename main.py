import codecs
import fortune
import globals
import shelve
import random
import shelve

import requests
import telebot
import weather

from telebot import types
import calculator

# Ссылка на бота
bot = telebot.TeleBot(globals.TOKEN)

# База данных пользователей
users = shelve.open('users')


# Замена кнопок
def updating_main_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Узнать погоду':
        button_1 = types.InlineKeyboardButton('На сегодня', callback_data='today')
        button_2 = types.InlineKeyboardButton('На 5 дней', callback_data='5days')

        markup.add(button_1, button_2)
    else:
        button_1 = types.KeyboardButton('Узнать погоду')
        button_2 = types.KeyboardButton('Подписаться')

        if str(message.chat.id) in users.dict:
            button_2 = types.KeyboardButton('Отписаться')

        button_3 = types.KeyboardButton('Калькулятор')

        markup.add(button_1, button_2, button_3)

    return markup


# Вывод подсчётов
def print_alco(message):
    bot.send_message(message.chat.id, calculator.calculate_alco(message))


# При вводе названия города для режима 'На сегодня'
def print_today(message):
    bot.send_message(message.chat.id, weather.current_forecast(message.text))
    markup = updating_main_markup(message)
    bot.send_message(message.chat.id, 'Я снова готов к работе)', parse_mode='html', reply_markup=markup)


# При вводе названия города для режима 'На 5 дней'
def print_forecast(message):
    bot.send_message(message.chat.id, weather.future_forecast(message.text))
    markup = updating_main_markup(message)
    bot.send_message(message.chat.id, 'Я снова готов к работе)', parse_mode='html', reply_markup=markup)


# Действия при /start
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = updating_main_markup(message)

    bot.send_message(message.chat.id,
                     'Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, '
                     'бот созданный чтобы рассказывать вам о погоде и не только).'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Если хотите узнать ответ, задайте вопрос,\n'
                                      'если хотите посчитать сколько выпить, напишите Калькулятор,\n'
                                      'если хотите подписаться, напишите Подписаться,\n'
                                      'если хотите отписаться, напишите Отписаться,\n'
                                      'если хотите узнать погоду, напишите Узнать погоду.')


# Тайная функция)
@bot.message_handler(commands=['secret'])
def random_pos(message):
    data = requests.get(f"{globals.PICTURES}{random.randint(0, 100)}.jpg")
    bot.send_photo(message.chat.id, data.content)


# Действия при любом другом сообщении
@bot.message_handler(content_types=['text'])
def processing(message):
    if message.text == 'Калькулятор':
        # Вызов калькулятора опьянения
        bot.send_message(message.chat.id, 'Введите пол(м/ж), вес, рост, градус и мл(цифрами и через пробелы)')
        bot.register_next_step_handler(message, print_alco)
    elif message.text == 'Подписаться':
        # При выборе функции 'Подписаться'
        users.dict[str(message.chat.id)] = ''
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Теперь вы подписаны, {0.first_name})'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'Отписаться':
        # При выборе функции 'Отписаться'
        del users[str(message.chat.id)]
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Возвращайтесь поскорей, {0.first_name})'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'Узнать погоду':
        # При выборе функции 'Узнать погоду'
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Теперь выберите режим'.format(),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'На сегодня':
        # При выборе функции 'На сегодня'
        bot.send_message(message.chat.id,
                         'Введите название города')
        bot.register_next_step_handler(message, print_today)

    elif message.text == 'На 5 дней':
        # При выборе функции 'На 5 дней'
        bot.send_message(message.chat.id,
                         'Введите название города'.format())
        bot.register_next_step_handler(message, print_forecast)
    elif message.text[-1] == '?':
        # При вводе вопросе
        answer = fortune.get_orb_answer()
        if str(message.chat.id) in users:
            user_info = codecs.decode(users.dict[str(message.chat.id)], 'UTF-8')
            user_info += f'{message.text}\n{answer}\n'
            users.dict[str(message.chat.id)] = user_info
        bot.send_message(message.chat.id, answer)
    else:
        # При вводе случайного сообщения
        bot.send_message(message.chat.id, 'Я предпочту сохранить молчание')

    # Обновление базы данных
    users.sync()


# Запуск бота
bot.polling(none_stop=True)
