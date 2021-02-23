import telebot
from telebot import types
import os
import subprocess
from config import bot_token, base_catalog

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_contact = types.InlineKeyboardButton(text='Связаться с нами', callback_data='about')
    item_disclam = types.InlineKeyboardButton(text='README', callback_data='readme')

    markup_inline.add(item_contact, item_disclam)
    img = open('Sova.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, 'Вся информация взята из открытых источников \n И только в ознакомительных целях',
                     reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'about':
        bot.send_message(call.message.chat.id, 'Напишите нам сюда: test@test.com')
    elif call.data == 'readme':
        bot.send_message(call.message.chat.id,
                         'Я умею искать слитые в сеть пароли и почту. \n Введи почту, пароль или телефон.')


@bot.message_handler(content_types=['text'])
def main_func(message):
    """Функция принимает текст от пользователя и ищет в базе"""

    # TODO: сделать регулярное выражение на входе чтобы принимала программа только почту
    # TODO: сделать чтобы закрывали звездочки пароль
    # TODO: организовать логирование
    # TODO: фото можно подцепить из URL в соц сетях модифицировав её на основе почты

    os.chdir(base_catalog)
    try:
        cod_search = subprocess.run(['./query.sh', message.text], stdout=subprocess.PIPE)
        file_simple = cod_search.stdout.decode('utf-8')
        bot.send_message(message.chat.id, file_simple)
    except Exception as err:
        print(err)

    # with open('VK_100M.txt', 'r', encoding='utf-8', errors='ignore') as file:
    #     for i in file:
    #         if message.text in i:
    #             lists.append(i)
    #         else:
    #             continue
    #     else:
    #         if not lists:
    #             bot.send_message(message.chat.id, 'Нет совпадений в базе')
    #         else:
    #             for line in lists:
    #                 bot.send_message(message.chat.id, line)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
