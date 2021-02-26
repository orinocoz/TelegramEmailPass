import telebot
from telebot import types
import os
import time
import subprocess
from config import bot_token, base_catalog

# TODO: сделать регулярное выражение на входе чтобы принимала программа только почту
# TODO: организовать логирование
# TODO: расширить функцианал фото можно подцепить из URL в соц сетях модифицировав её на основе почты цели


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_contact = types.InlineKeyboardButton(text='Связаться с нами', callback_data='about')
    item_disclam = types.InlineKeyboardButton(text='README', callback_data='readme')

    markup_inline.add(item_contact, item_disclam)

    try:
        img = open('logo.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, 'Вся информация взята из открытых источников '
                                          '\n И только в ознакомительных целях', reply_markup=markup_inline)
    except Exception as err:
        bot.send_message(message.chat.id, 'Попробуйте еще раз')
        print(err)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'about':
        bot.send_message(call.message.chat.id, 'По всем вопросам: @b0t_for_you')
    elif call.data == 'readme':
        bot.send_message(call.message.chat.id,
                         'Я умею искать слитые в сеть пароли и почту. \n Введи почту для поиска.')


@bot.message_handler(content_types=['text'])
def main_func(message):
    """Функция принимает текст от пользователя и ищет в базе"""

    with open('log.txt', 'a', encoding='utf-8', errors='ignore') as file_log:
        file_log.writelines(message.text + '\n')
        file_log.close()

    lists = []
    os.chdir(base_catalog)

    try:
        cmd_console = subprocess.run(['./query.sh', message.text], stdout=subprocess.PIPE)
        out_interpreter = cmd_console.stdout.decode('utf-8', errors='ignore')

        if message.text in out_interpreter:
            for i in out_interpreter.split():
                lists.append(''.join(i)[:-3] + '***')
            about_up = 'Найдено совпадений: ' + str(len(lists)) + '\n\n'
            about_down = '\n\nПолучить больше инфы без звездочек бесплатно, напиши мне: @b0t_for_you '
            bot.send_message(message.chat.id, about_up + '\n'.join(lists[0:5]) + about_down)
            time.sleep(5)
        else:
            bot.send_message(message.chat.id, 'Нет совпадений в базе')
            time.sleep(5)

    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, 'Что то пошло не так 1')
        print('ApiException')
        time.sleep(5)
    except Exception as err:
        bot.send_message(message.chat.id, 'Что то пошло не так 2')
        print(err)
        time.sleep(5)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
