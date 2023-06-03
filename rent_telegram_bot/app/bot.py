import datetime
from io import BytesIO

import requests
import telebot
from PIL import Image
from telebot import types

from const import BOT_TOKEN
from const import language

bot = telebot.TeleBot(token=BOT_TOKEN)

# Back button
back_button_menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_button = telebot.types.KeyboardButton('Back')
back_button_menu_markup.add(back_button)

back_button_menu_markup_ru = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_button_ru = telebot.types.KeyboardButton('Назад')
back_button_menu_markup_ru.add(back_button_ru)

back_button_menu_markup_srb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_button_srb = telebot.types.KeyboardButton('Jeziku')
back_button_menu_markup_srb.add(back_button_srb)


# Define the main menu handler
@bot.message_handler(func=lambda message: message.text.lower() == 'start' or message.text.lower() == '/start')
def main_handler(message):
    buttons = [
        types.InlineKeyboardButton('russian', callback_data='ru'),
        types.InlineKeyboardButton('english', callback_data='en'),
        types.InlineKeyboardButton('serbian', callback_data='srb')
    ]
    reply_markup = types.InlineKeyboardMarkup(row_width=3)
    reply_markup.add(*buttons)
    bot.send_message(chat_id=message.chat.id, text='Izaberite jezik / Select language / Выберите язык',
                     reply_markup=reply_markup)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('ru') or call.data.startswith('en') or call.data.startswith('srb'))
def handle_language(callback_query):
    # Define the main menu
    main_menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    moto_button = telebot.types.KeyboardButton(f'{language[callback_query.data]["moto"]}')
    yacht_button = telebot.types.KeyboardButton(f'{language[callback_query.data]["yacht"]}')
    main_menu_markup.add(moto_button, yacht_button)

    bot.send_message(callback_query.message.chat.id,
                     text=language[f"{callback_query.data}"]["welcome"], reply_markup=main_menu_markup)


# Define the moto handler
@bot.message_handler(func=lambda
        message: message.text.lower() == 'moto' or message.text.lower() == 'мото' or message.text.lower() == 'motocikl')
def moto_handler(message):
    global selected_language
    if message.text.lower() == 'мото':
        bot.send_message(message.chat.id, language['ru']['available_moto'],
                         reply_markup=back_button_menu_markup_ru)
        selected_language = 'ru'

    if message.text.lower() == 'moto':
        bot.send_message(message.chat.id, language['en']['available_moto'],
                         reply_markup=back_button_menu_markup)
        selected_language = 'en'

    if message.text.lower() == 'motocikl':
        bot.send_message(message.chat.id, language['srb']['available_moto'],
                         reply_markup=back_button_menu_markup_srb)
        selected_language = 'srb'

    response = requests.get('http://0.0.0.0:8000/moto/')
    vehicle_type = 'Moto'
    response_parser(message=message, response=response, vehicle_type=vehicle_type, selected_language=selected_language)


# Define the yacht handler
@bot.message_handler(func=lambda
        message: message.text.lower() == 'яхта' or message.text.lower() == 'yacht' or message.text.lower() == 'jahte')
def yacht_handler(message):
    global selected_language
    if message.text.lower() == 'яхта':
        bot.send_message(message.chat.id, language['ru']['available_yacht'],
                         reply_markup=back_button_menu_markup_ru)
        selected_language = 'ru'

    if message.text.lower() == 'yacht':
        bot.send_message(message.chat.id, language['en']['available_yacht'],
                         reply_markup=back_button_menu_markup)
        selected_language = 'en'

    if message.text.lower() == 'jahte':
        bot.send_message(message.chat.id, language['srb']['available_yacht'],
                         reply_markup=back_button_menu_markup_srb)
        selected_language = 'srb'

    response = requests.get('http://0.0.0.0:8000/yacht/')
    vehicle_type = 'Yacht'
    response_parser(message=message, response=response, vehicle_type=vehicle_type, selected_language=selected_language)


# Returns vehicles available for rent
def response_parser(message, response: requests.models.Response, vehicle_type: str, selected_language: str):
    parsed_json = response.json()
    if parsed_json:
        for i in parsed_json:
            if not i['rented']:
                response = requests.get(i['photo'])
                img = Image.open(BytesIO(response.content))
                button_text = f'{language[selected_language]["order"]} {i["model_name"]}'
                reply_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(button_text,
                                                                                       callback_data=button_text)]])
                bot.send_photo(
                    message.chat.id, img,
                    f'{language[selected_language][vehicle_type.lower()]}: {i["model_name"]}, \n{language[selected_language]["price_per_day"]} {i["price_per_day"]}€',
                    reply_markup=reply_markup)
    else:
        bot.send_message(
            message.chat.id,
            f'{language[selected_language]["sorry"]}')


# Handle moto and yacht order
@bot.callback_query_handler(
    func=lambda call: call.data.startswith('Арендовать') or call.data.startswith('Order') or call.data.startswith(
        'Poruči'))
def handle_order(callback_query):
    global selected_language
    if callback_query.data.lower() == 'арендовать':
        selected_language = 'ru'
    if callback_query.data.lower() == 'order':
        selected_language = 'en'
    if callback_query.data.lower() == 'poruči':
        selected_language = 'srb'

    caption = callback_query.json['message']['caption'].split(',')[0]
    bot.send_message(callback_query.message.chat.id,
                     text=f"{language[selected_language]['want']} {caption}{language[selected_language]['rent']}")
    should_handle_message = True

    # Register a new message handler
    @bot.message_handler(func=lambda message: should_handle_message)
    def handle_user_reply(message):
        # Process the user's reply here
        # Extract the necessary information from the message
        user_message = message.text
        current_time = datetime.datetime.now()
        reply_text = language[selected_language]['details'] + '\n' + user_message + language[selected_language][
            'we_will']
        manager_id = '-1001964290876'
        manager_message = f"{current_time.ctime()}\nNew booking request for {caption}.\n{user_message}"

        # Send a message to manager
        bot.send_message(manager_id, text=manager_message)
        bot.send_message(message.chat.id, text=reply_text)

        nonlocal should_handle_message
        should_handle_message = False


# Define the back handler
@bot.message_handler(func=lambda
        message: message.text.lower() == 'back' or message.text.lower() == 'назад' or message.text.lower() == 'jeziku')
def back_handler(message):
    global selected_language
    if message.text.lower == 'back':
        selected_language = 'en'
    if message.text.lower == 'назад':
        selected_language = 'ru'
    if message.text.lower == 'jeziku':
        selected_language = 'srb'
    bot.send_message(message.chat.id, language[selected_language]['return'])
    buttons = [
        types.InlineKeyboardButton('russian', callback_data='ru'),
        types.InlineKeyboardButton('english', callback_data='en'),
        types.InlineKeyboardButton('serbian', callback_data='srb')
    ]
    reply_markup = types.InlineKeyboardMarkup(row_width=3)
    reply_markup.add(*buttons)
    bot.send_message(chat_id=message.chat.id, text='Izaberite jezik / Select language / Выберите язык',
                     reply_markup=reply_markup)


# Run the bot
bot.polling()
