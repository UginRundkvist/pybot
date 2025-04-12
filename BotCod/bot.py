import telebot
from telebot import types
import time
from datetime import datetime, timedelta
import sqlite3
import threading

bot = telebot.TeleBot('6078696552:AAHcGGJHMNYeaIzV6wW2QMIhpRZOaEr8SrQ', parse_mode = None)

def create_connection(path):
    connection = None
    connection = sqlite3.connect(path)
    return connection


def proverka(non):
    bd = sqlite3.connect('TableUsers.db')
    conn = bd.cursor()
    while(True):
        sel = conn.execute('''SELECT word_id, words, chatt_id FROM userwords 
                           INNER JOIN users ON userwords.chatt_id = users.chat_id 
                           WHERE time_next_rem <= datetime('now') AND send=0''')
        results = sel.fetchone()
        
        chatid=results[2]
        word = results[1]
        wid = results[0]
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('Легко', callback_data='eazy', )
        button2 = types.InlineKeyboardButton('Сложно', callback_data='hard')
        markup.add(button1,button2)
        
        bot.send_message(chatid, word, reply_markup=markup)
        conn.execute('''UPDATE userwords SET send = ? WHERE word_id=?''', (1, wid))
        bd.commit()
        time.sleep(6) 

      
@bot.callback_query_handler(func=lambda call: True)
def but(call):
    bd = sqlite3.connect('TableUsers.db')
    conn = bd.cursor()
    nxeztime = datetime.now() - timedelta(hours=2.99)
    htime = nxeztime.strftime('%Y-%m-%d %H:%M:%S')
    eztime = nxeztime.strftime('%Y-%m-%d %H:%M:%S')
    if call.message:
        if call.data == 'eazy':
            conn.execute('''UPDATE userwords SET send = ?, time_next_rem = ? WHERE word_id=?''', (0, eztime, call.message.chat.id)) 
            bot.send_message(call.message.chat.id, 'Работает') 
        elif call.data == 'hard':
            conn.execute('''UPDATE userwords SET send = ?, time_next_rem = ? WHERE word_id=?''', (0, htime, call.message.chat.id))
            bot.send_message(call.message.chat.id, 'Тож Работает')
    bd.commit()
        
        
def main():
    print('hi!')
    bd = sqlite3.connect('TableUsers.db')
    bd.close() 
    x = threading.Thread(target=proverka, args=('1',))
    x.start()       

     
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Информация')
    bd = create_connection("TableUsers.db")
    conn = bd.cursor() 
    conn.execute('INSERT INTO users (chat_id, user_id, Name) VALUES (?, ?, ?)', (message.chat.id, message.from_user.id, message.from_user.username))
    bd.commit()
    bd.close()    


@bot.message_handler(commands=['new'])
def create(message):
    mesg = bot.send_message(message.chat.id, 'Введите новое слово')
    bot.register_next_step_handler(mesg, new)


def new(message):
    bot.send_message(message.chat.id,'Вы добавили слово ' + message.text)    
    bd = create_connection('TableUsers.db')
    conn = bd.cursor()
    ctime = datetime.now()
    nextime = datetime.now() - timedelta(hours=2.99)
    tt = nextime.strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('''INSERT INTO userwords (words, create_time, time_next_rem, chatt_id) VALUES (?, ?, ?, ?)''', (message.text, ctime, tt, message.chat.id))
    bd.commit()
    bd.close() 
  
  
main()
bot.polling(none_stop=True)