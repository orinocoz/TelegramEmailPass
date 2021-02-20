import telebot
from telebot import types

BOT_TOKEN = '1678862072:AAHxLwixFSQcFDjBbHKmzXGttKQkGJXEJVs'
bot = telebot.TeleBot(BOT_TOKEN)


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
def main_func(message):  # простая функция в случае выполнения условия прини()мающая аргументом сообщение пользователя
    lists = []
    with open('VK_100M.txt', 'r', encoding='utf-8', errors='ignore') as file:
        for i in file:
            if message.text in i:
                lists.append(i)
            else:
                continue
        else:
            if not lists:
                bot.send_message(message.chat.id, 'Нет совпадений в базе')
            else:
                for line in lists:
                    bot.send_message(message.chat.id, line)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
