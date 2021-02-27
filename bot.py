import telebot
from telebot import types
import os
import time
import subprocess
from config import bot_token, base_catalog

# TODO: организовать нормальное логирование
# TODO: расширить функцианал фото(!) можно подцепить из URL в соц сетях модифицировав её на основе почты цели


bot = telebot.TeleBot(bot_token)  # создаем бота передаем ему наш токен


@bot.message_handler(commands=['start', 'help'])  # декоратор с фильтром принимающим комманды бота
def send_welcome(message):
    """ Функция для работы с командами бота """
    markup_inline = types.InlineKeyboardMarkup()  # создаем клавиатуру в поле диалогов
    item_contact = types.InlineKeyboardButton(text='Связаться с нами', callback_data='about')  # создаем кнопки
    item_disclam = types.InlineKeyboardButton(text='README', callback_data='readme')

    markup_inline.add(item_contact, item_disclam)  # передаем кнопки нашей клавиатуре

    try:  # создаем конструкцию для проверки и отлова исключений
        img = open('logo.jpg', 'rb')  # открываем картинку в режиме чтение-побитово
        bot.send_photo(message.chat.id, img)  # отправляем фото и текст в чат
        bot.send_message(message.chat.id, 'Вся информация взята из открытых источников '
                                          '\n И только в ознакомительных целях', reply_markup=markup_inline)
    except Exception as err:  # ловим исключение если что то не получилось
        bot.send_message(message.chat.id, 'Попробуйте еще раз')
        print(err)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    """Функция обрабатывающая вызов при нажатии на кнопки """
    if call.data == 'about':  # если нажали кнопку с callback_data=about то отправляем в чат текст
        bot.send_message(call.message.chat.id, 'По всем вопросам: @b0t_for_you')
    elif call.data == 'readme':  # аналогично
        bot.send_message(call.message.chat.id,
                         'Я умею искать слитые в сеть пароли и почту. \n Введи почту для поиска.')


@bot.message_handler(content_types=['text'])
def main_func(message):  # принимает любой текст что напишет пользователь в поле чата
    """Функция принимает текст от пользователя и ищет в базе"""

    with open('log.txt', 'a', encoding='utf-8', errors='ignore') as file_log:  # открываем файл для логирования
        file_log.writelines(message.text + '\n')  # записываем что ввел пользователь в файл
        file_log.close()  # гарантированно закрываем файл(?)
    if '@' and '.' not in message.text:  # проверяем ввел ли юзер почту (лаконичное решение без regex)
        bot.send_message(message.chat.id, 'Введите корректный email адрес!')  # если нет просим еще раз ввести
        time.sleep(3)
    else:  # если юзер корректно ввел почту то
        lists = []  # создем пустой список
        os.chdir(base_catalog)  # перемещаемся в категорию где расположена наша база

        try:
            cmd_console = subprocess.run(['./query.sh', message.text], stdout=subprocess.PIPE)  # отдаем команду в
            # через питон в консоль запуская баш скрипт который ищет в базе и возвращает обратно результат поиска
            out_interpreter = cmd_console.stdout.decode('utf-8', errors='ignore')  # приводим результат в str()
            print(out_interpreter)  # скрытая печать для дебага
            if message.text in out_interpreter:  # проверяем есть ли почта от юзера в том, что нашли в базе
                for i in out_interpreter.split():  # если нашли приводим в list() и итерируем по элементам списка
                    lists.append(''.join(i)[:-3] + '***')  # добавляя в пустой список элементы заменяя 3 последних симв
                about_up = 'Найдено совпадений: ' + str(len(lists)) + '\n\n'  # информация о количестве совпадений
                about_down = '\n\nПолучить больше инфы без звездочек бесплатно, напиши мне: @b0t_for_you '
                bot.send_message(message.chat.id, about_up + '\n'.join(lists[0:3]) + about_down)  # выводим конечный
                # результат для пользователя если найдено много почт печатаем только первые 3 пердлагая заплатить
                time.sleep(5)
            else:
                bot.send_message(message.chat.id, 'Нет совпадений в базе')  # если не нашел в базе почту
                time.sleep(5)

        except telebot.apihelper.ApiException:  # отработка исключений
            bot.send_message(message.chat.id, 'Что то пошло не так 1')
            print('ApiException')
            time.sleep(5)
        except Exception as err:
            bot.send_message(message.chat.id, 'Что то пошло не так 2')
            print(err)
            time.sleep(5)


while True:  # говорим нашему боту работать постоянно дабы не отваливался как рекомендуют создатели библиотеки
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
