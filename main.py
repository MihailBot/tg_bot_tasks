import telebot
from telebot import types
from custom_handlers import sort_few_tasks, short_sent

TOKEN_BOT = '6395798798:AAFKLPZZaPT4ZzYHM6K5_VWiXdjVh4j6XiE'
bot = telebot.TeleBot(TOKEN_BOT)
buttons_list = []
signal = None 
callback_button = None

@bot.message_handler(commands=['start'])
def start_menu(message):
    bot.send_message(message.chat.id, 'Привет, я рад что ты решил воспользоваться моим ботом) С ним ты сможешь составить свои планы на день и непрерывно идти к своей цели')
    bot.send_message(message.chat.id, 'Чтобы начать работу введи /menu')
    bot.send_message(message.chat.id, 'Если нужна помощь введи /help')

#главное меню
@bot.message_handler(commands=['menu'])
def main_menu(message):
    global signal
    signal = None
    markup = types.InlineKeyboardMarkup()
    button_count = 0
    for i in range(len(buttons_list)):
        short = short_sent(buttons_list[button_count])
        markup.add(types.InlineKeyboardButton(short, callback_data=short))
        button_count += 1
    if len(buttons_list) == 0:
        bot.send_message(message.chat.id, 'У вас нет задач, создайте их командой <b>/new</b>', reply_markup=markup, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Вот ваши задачи🗒', reply_markup=markup)
        
#содание задачи
@bot.message_handler(commands=['new'])
def create_new_button(message):
    global signal
    bot.send_message(message.chat.id, 'Введи название задачи✍')
    signal = 'new'
    bot.register_message_handler(message, text_handler)
    
#добавление нескольких задач
@bot.message_handler(commands=['few'])
def add_few_buttons(message):
    global signal
    bot.send_message(message.chat.id, 'Введи несколько заданий через запятую и я их добавлю  Пример: Задание, Задание 2, Задание 3')
    signal = 'few'
    bot.register_message_handler(message, text_handler)
    
#инструкция к боту
@bot.message_handler(commands=['help'])
def help_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Инструкция бота', url='https://telegra.ph/Rukovodstvo-k-botu-05-06'))
    bot.send_message(message.chat.id, 'Нужна помощь?', reply_markup=markup)
    
#обработчик пользовательского текста
@bot.message_handler(content_types=['text'])
def text_handler(message):
    global signal
    global buttons_list
    global callback_button
    if signal == 'new':
        bot.delete_message(message.chat.id, message.message_id-1)
        buttons_list.append(message.text) 
        main_menu(message)
        signal = None
        
    elif signal == 'few':
        bot.delete_message(message.chat.id, message.message_id-1)
        spis_buttons = sort_few_tasks(message.text)
        
        index = 0
        for i in range(len(spis_buttons)):
            buttons_list.append(spis_buttons[index])
            index += 1
        bot.delete_message(message.chat.id, message.message_id)
        main_menu(message)
        signal = None

    elif signal == 'edit':
        index = buttons_list.index(callback_button)
        buttons_list.pop(index)
        buttons_list.insert(index, message.text)
        bot.delete_message(message.chat.id, message.message_id - 1)
        main_menu(message)
  
#callback обработчик
@bot.callback_query_handler(func=lambda callback: True)
def markup_handler(callback):
    global callback_button
    global signal
    #кнопка "назад в меню"
    if callback.data == 'menu':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        main_menu(callback.message)
        
    #кнопка collect в меню кнопки
    elif callback.data == 'collect':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        buttons_list.remove(callback_button)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('⬅️Назад в меню', callback_data='menu'))
        bot.send_message(callback.message.chat.id, 'Задача выполнена', reply_markup=markup)

    #кнопка "редактировать"
    elif callback.data == 'edit':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,  'Введите новое название для задачи')
        signal = 'edit'
        bot.register_message_handler(callback.message, text_handler)

    #вывод меню в кнопке
    button_count = 0
    for i in range(len(buttons_list)):
        if callback.data == short_sent(buttons_list[button_count]):
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            callback_button = buttons_list[button_count]
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('⬅️Назад в меню', callback_data='menu')
            btn2 = types.InlineKeyboardButton('✅Выполнить✅', callback_data='collect')
            btn3 = types.InlineKeyboardButton('Редактировать✏️', callback_data='edit')
            markup.row(btn2)
            markup.row(btn1, btn3)
            bot.send_message(callback.message.chat.id, buttons_list[button_count], reply_markup=markup)
            break
        else:
            button_count += 1

bot.polling(none_stop = True)

        
