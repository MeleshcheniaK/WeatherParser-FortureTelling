import codecs
import random
import shelve

import requests
import telebot
from telebot import types

import calculator
import fortune
import globals
import weather

# Ссылка на бота
bot = telebot.TeleBot(globals.TOKEN)

# База данных пользователей
users = shelve.open('users')



def updating_main_markup(message):
    """
    Замена кнопок
    :param message: Сообщение с учётом которого проводится обновление
    :return:
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Если выбрана функция 'Узнать погоду'
    if message.text == 'Узнать погоду':
        button_1 = types.InlineKeyboardButton('На сегодня', callback_data='today')
        button_2 = types.InlineKeyboardButton('На 5 дней', callback_data='5days')

        markup.add(button_1, button_2)
    else:
        # Главное меню
        button_1 = types.KeyboardButton('Узнать погоду')
        button_2_text = 'Подписаться'

        if str(message.chat.id) in users.dict:
            button_2_text = 'Отписаться'

        button_2 = types.KeyboardButton(button_2_text)
        button_3 = types.KeyboardButton('Калькулятор')

        markup.add(button_1, button_2, button_3)

    return markup


def print_alco(message):
    """
    Вывод подсчётов
    :param message: Данные для подсчёта
    :return:
    """
    bot.send_message(message.chat.id, calculator.calculate_alco(message))


def print_today(message):
    """
    При вводе названия города для режима 'На сегодня'
    :param message: Название города
    :return:
    """
    bot.send_message(message.chat.id, weather.current_forecast(message.text))
    markup = updating_main_markup(message)
    bot.send_message(message.chat.id, 'Я снова готов к работе)', parse_mode='html', reply_markup=markup)


def print_forecast(message):
    """
    При вводе названия города для режима 'На 5 дней'
    :param message: Название города
    :return:
    """
    bot.send_message(message.chat.id, weather.future_forecast(message.text))
    markup = updating_main_markup(message)
    bot.send_message(message.chat.id, 'Я снова готов к работе)', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Действия при /start
    :param message: /start
    :return:
    """
    markup = updating_main_markup(message)

    bot.send_message(message.chat.id,
                     'Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, '
                     'бот созданный чтобы рассказывать вам о погоде и не только).'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    """
        Действия при /help
        :param message: /help
        :return:
    """
    bot.send_message(message.chat.id, 'Если хотите узнать ответ, задайте вопрос,\n'
                                      'если хотите посчитать сколько выпить, напишите Калькулятор,\n'
                                      'если хотите подписаться, напишите Подписаться,\n'
                                      'если хотите отписаться, напишите Отписаться,\n'
                                      'если хотите узнать погоду, напишите Узнать погоду.')


@bot.message_handler(commands=['secret'])
def random_pos(message):
    """
    Тайная функция)
    :param message: /secret
    :return:
    """
    data = requests.get(f"{globals.PICTURES}{random.randint(0, 100)}.jpg")
    bot.send_photo(message.chat.id, data.content)


@bot.message_handler(content_types=['text'])
def processing(message):
    """
    Действия при любом другом сообщении
    :param message: Сообщение для обработки
    :return:
    """
    if message.text == 'Калькулятор':
        # Вызов калькулятора опьянения
        bot.send_message(message.chat.id, 'Введите пол(м/ж), вес, рост, градус и мл(цифрами и через пробелы)')
        bot.register_next_step_handler(message, print_alco)
    elif message.text == 'Подписаться':
        # При выборе функции 'Подписаться' добавляем пользователя в базу данных
        users.dict[str(message.chat.id)] = ''
        markup = updating_main_markup(message)
        bot.send_message(message.chat.id,
                         'Теперь вы подписаны, {0.first_name})'.format(message.from_user),
                         parse_mode='html', reply_markup=markup)
    elif message.text == 'Отписаться':
        # При выборе функции 'Отписаться' удаляем пользователя из базы данных
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
        # При вводе вопроса
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
