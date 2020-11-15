import os
import telebot
import datetime
import json
import traceback
import schedule
import time
import fics
from functools import wraps
from multiprocessing import *


me = os.getenv("ME")
token = os.getenv("TOKEN")
channel = os.getenv("CHANNEL")
#url = "https://api.telegram.org/bot" + token + "/"

bot = telebot.TeleBot(token)

def start_process():#Запуск Process
    p1 = Process(target=P_schedule.start_schedule, args=()).start()
 
    
class P_schedule(): # Class для работы с schedule
    def start_schedule(): #Запуск schedule
        ######Параметры для schedule######
        #schedule.every().day.at("11:02").do(P_schedule.send_message1)
        schedule.every(12).hours.do(P_schedule.send_message)
        ##################################
        
        while True: #Запуск цикла
            schedule.run_pending()
            time.sleep(1)
 
    ####Функции для выполнения заданий по времени  
    def send_message():
        something_updated = False
        for fic in fics.fics:
            if fic.is_updated():
                bot.send_message(chat_id=channel, text=f'Привет! Счастлива сообщить, что у фанфика {fic.name} появилось продолжение! Ты остановилась на главе {fic.stop}. Ссылка на фик: {fic.url}. Поздравляю!')
                something_updated = True
            elif fic.is_updated() == False and fic.check_parts() == 0:
                bot.send_message(chat_id=channel, text='Ошибочька. Или фанфик пуст, или проблемка с сервером.')

        if not something_updated:
            bot.send_message(chat_id=channel, text='Обновлений нет, милорд.')


@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'убирайтесь отсюда'  
  )

@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Написать Насте', url='telegram.me/raumdemenz'  
        )  
    )  
    bot.send_message(  
        message.chat.id,  
        'Настя, ты сделала этот бот для получения уведомлений. Ты же читаешь фанфики. \n' +
        'Тебе уже не помочь. \n' +
        'Команда для получения обнов на канал: /check.',  
        reply_markup=keyboard  
    )

@bot.message_handler(commands=['check'])  
def check_command(message): 
    something_updated = False
    for fic in fics.fics:
        if fic.is_updated():
            bot.send_message(chat_id=channel, text=f'Привет! Счастлива сообщить, что у фанфика {fic.name} появилось продолжение! Ты остановилась на главе {fic.stop}. Ссылка на фик: {fic.url}. Поздравляю!')
            bot.send_message(  
                message.chat.id,  
                'Ответ на канале!'  
            )
            something_updated = True

    if not something_updated:
        bot.send_message(chat_id=channel, text='Обновлений нет, милорд.')
        bot.send_message(  
                message.chat.id,  
                'Ответ на канале!'  
            )


if __name__ == '__main__':
    start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass