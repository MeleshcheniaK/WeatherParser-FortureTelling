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
        item1 = types.InlineKeyboardButton('На сегодня', callback_data='today')
        item2 = types.InlineKeyboardButton('На 5 дней', callback_data='5days')

        markup.add(item1, item2)
    else:
        item1 = types.KeyboardButton('Узнать погоду')
        if str(message.chat.id) in users.dict:
            item2 = types.KeyboardButton('Отписаться')
        else:
            item2 = types.KeyboardButton('Подписаться')
        item3 = types.KeyboardButton('Калькулятор')

        markup.add(item1, item2, item3)

    return markup


# Вывод подсчётов
def print_alco(message):
    bot.send_message(message.chat.id, calculator.calculate_alco(message))


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
def processing(message):
    bot.send_message(message.chat.id, 'Если хотите узнать ответ, задайте вопрос,\n'
                                      'если хотите посчитать сколько выпить, напишите Калькулятор,\n'
                                      'если хотите подписаться, напишите Подписаться,\n'
                                      'если хотите отписаться, напишите Отписаться,\n'
                                      'если хотите узнать погоду, напишите Узнать погоду.')

# Тайная функция)
@bot.message_handler(commands=['secret'])
def random_pos(message):
    data = requests.get("https://castlots.org/img/kamasutra/" + str(random.randint(0, 100)) + ".jpg")
    bot.send_photo(message.chat.id, data.content)


# Действия при любом другом сообщении
@bot.message_handler(content_types=['text'])
def processing(message):
    if globals.STATE == 1:
        # При вводе названия города для режима "На сегодня"
        bot.send_message(message.chat.id, weather.current_forecast(message.text))
        globals.STATE = 0
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id, "Я снова готов к работе)", parse_mode='html', reply_markup=markup)
    elif globals.STATE == 2:
        # При вводе названия города для режима "На 5 дней"
        bot.send_message(message.chat.id, weather.future_forecast(message.text))
        globals.STATE = 0
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id, "Я снова готов к работе)", parse_mode='html', reply_markup=markup)
    elif message.text == 'Калькулятор':
        # Вызов калькулятора опьянения
        bot.send_message(message.chat.id, "Введите пол(м/ж), вес, рост, градус и мл(цифрами и через пробелы)")
        bot.register_next_step_handler(message, print_alco)
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
                         'Теперь выберите режим'.format(),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'На сегодня':
        # При выборе функции "На сегодня"
        bot.send_message(message.chat.id,
                         'Введите название города'.format())
        globals.STATE = 1
    elif message.text == 'На 5 дней':
        # При выборе функции "На 5 дней"
        bot.send_message(message.chat.id,
                         'Введите название города'.format())
        globals.STATE = 2
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
