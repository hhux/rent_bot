from io import BytesIO

import requests
import telebot
from PIL import Image
from telebot import types

from const import BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN)

# Define the main menu
main_menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
moto_button = telebot.types.KeyboardButton('Moto')
yacht_button = telebot.types.KeyboardButton('Yacht')
main_menu_markup.add(moto_button, yacht_button)

# Back button
back_button_menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_button = telebot.types.KeyboardButton('Back')
back_button_menu_markup.add(back_button)


# Define the main menu handler
@bot.message_handler(func=lambda message: message.text.lower() == 'start' or message.text.lower() == '/start')
def main_handler(message):
    bot.send_message(message.chat.id, "Welcome! Please select a vehicle:", reply_markup=main_menu_markup)


# Define the moto handler
@bot.message_handler(func=lambda message: message.text.lower() == 'moto')
def moto_handler(message):
    bot.send_message(message.chat.id, "Here is the list of available motorcycles:",
                     reply_markup=back_button_menu_markup)
    response = requests.get('http://127.0.0.1:8000/moto/')
    for i in response.json():
        if not i['rented']:
            response = requests.get(i['photo'])
            img = Image.open(BytesIO(response.content))
            button_text = f'Order {i["model_name"]}'
            reply_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(button_text,
                                                                                   callback_data=button_text)]])
            bot.send_photo(message.chat.id, img, f'Moto: {i["model_name"]}, \nPrice per day: {i["price_per_day"]}€',
                           reply_markup=reply_markup)


# Define the yacht handler
@bot.message_handler(func=lambda message: message.text.lower() == 'yacht')
def yacht_handler(message):
    bot.send_message(message.chat.id, "Here is the list of available yachts:", reply_markup=back_button_menu_markup)
    response = requests.get('http://127.0.0.1:8000/yacht/')
    for i in response.json():
        response = requests.get(i['photo'])
        img = Image.open(BytesIO(response.content))
        button_text = f'Order {i["model_name"]}'
        reply_markup = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(button_text,
                                                                               callback_data=button_text)]])
        bot.send_photo(message.chat.id, img, f'Yacht: {i["model_name"]}, \nPrice per day: {i["price_per_day"]}€',
                       reply_markup=reply_markup)


# Handle moto and yacht order
@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def handle_order(callback_query):
    caption = callback_query.json['message']['caption'].split(',')[0]
    bot.send_message(callback_query.message.chat.id,
                     text=f"You want to rent {caption}.\n\nWith a reply message, indicate:\n 1. Your name\n"
                          " 2. Contact phone number for confirmation\n 3. Booking date")
    should_handle_message = True

    # Register a new message handler
    @bot.message_handler(func=lambda message: should_handle_message)
    def handle_user_reply(message):
        # Process the user's reply here
        # Extract the necessary information from the message
        user_message = message.text

        reply_text = f"Thank you for providing the following details:\n{user_message}.\nWe'll get back to you soon."
        manager_id = '-1001964290876'
        manager_message = f"New booking request for {caption}.\n{user_message}"

        # Send a message to manager
        bot.send_message(manager_id, text=manager_message)
        bot.send_message(message.chat.id, text=reply_text)

        nonlocal should_handle_message
        should_handle_message = False


# Define the back handler
@bot.message_handler(func=lambda message: message.text.lower() == 'back')
def back_handler(message):
    bot.send_message(message.chat.id, "Returning to the main menu.", reply_markup=main_menu_markup)


# Run the bot
bot.polling()
