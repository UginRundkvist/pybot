import telebot
from telebot import types

#bot = telebot.TeleBot('6078696552:AAHcGGJHMNYeaIzV6wW2QMIhpRZOaEr8SrQ', parse_mode = None) # токен лежит в файле config.py

@bot.message_handler(commands=['start'])
def tess(message):
     bot.send_message(message.chat.id, 'hi')
     markup = types.InlineKeyboardMarkup(row_width=2)
     button1 = types.InlineKeyboardButton('легко', callback_data='eazy')
     button2 = types.InlineKeyboardButton('сложно', callback_data='hard')
     markup.add(button1, button2)
     bot.send_message(message.chat.id, 'hi', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def but1(call):
    if call.message:
        if call.data == 'eazy':
            bot.send_message(call.message.chat.id, 'Работает')
        elif call.data == 'hard':  
            bot.send_message(call.message.chat.id, 'Тоже Работает')            
            
            
bot.polling(none_stop=True)      