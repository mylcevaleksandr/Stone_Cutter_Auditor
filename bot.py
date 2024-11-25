from config import telegram_token
import telebot
import threading
import json

# Initialize the bot
bot = telebot.TeleBot(telegram_token)


# Get user data from json file if it exists
def get_user_data():
    file = open('user_data.json', 'r')
    try:
        user_data_from_json = json.load(file)
    except FileNotFoundError:
        user_data_from_json = {}
    except json.decoder.JSONDecodeError:
        user_data_from_json = {}
    finally:
        file.close()
    return user_data_from_json


# Dictionary to store user data
user_data = get_user_data()


# Save user data to a json file
def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)


# Handler for /start command to initiate the process
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = str(message.chat.id)
    bot.send_message(user_id,
                     "Welcome! Here is a list of available commands/n"
                     "* /saw 1 - sets the current saw number*"
                     "+ /block 4141353115 - sets the block number for the chosen saw",
                     parse_mode="Markdown")
    # bot.send_message(user_id, user_data)


# Handler to process user input for saw number
@bot.message_handler(commands=['saw'])
def process_saw_number(message):
    user_id: str = str(message.chat.id)
    split_message = message.text.split()
    if len(split_message) > 1:

        saw_number = split_message[-1]
        if saw_number.isdigit():

            if user_id not in user_data:
                user_data[user_id] = {'available_saws': {}, 'current_saw_number': None}
                user_data[user_id]['current_saw_number'] = saw_number

            if saw_number not in user_data[user_id]['available_saws']:
                user_data[user_id]['available_saws'][saw_number] = {}
                user_data[user_id]['current_saw_number'] = saw_number
            else:
                user_data[user_id]['current_saw_number'] = saw_number
            save_user_data()

            bot.send_message(user_id,
                             f"Saw number {saw_number} selected. Enter the block number using /block <your number here>")
        else:
            bot.send_message(user_id, "Please enter a valid integer as the saw number.")

    else:
        bot.send_message(user_id, "Please enter a valid saw number after the /saw command. */saw 1*",
                         parse_mode="Markdown")


# Handler to process user input for block number
@bot.message_handler(commands=['block'])
def process_block_number(message):
    user_id = str(message.chat.id)
    block_number = message.text.split()[-1]
    if user_id in user_data and 'available_saws' in user_data[user_id]:
        available_saws = user_data[user_id]['available_saws']
        current_saw_number = user_data[user_id].get('current_saw_number')
        if current_saw_number and current_saw_number in available_saws:
            available_saws[current_saw_number][block_number] = {}
            save_user_data()
            bot.send_message(user_id, f"Block number {block_number} saved for saw number {current_saw_number}.")
        else:
            bot.send_message(user_id, "Please select saw number first")
    else:
        bot.send_message(user_id, "No user data found")


# Handler to process user input for cubic meters and calculate square
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, message.text)


def start_bot_polling():
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"An error occured: {e}")


polling_thread = threading.Thread(target=start_bot_polling)
polling_thread.start()

print("Bot started successfully without errors!")
