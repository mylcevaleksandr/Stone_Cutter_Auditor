from typing import List, Dict
from messages import *

from config import telegram_token
import telebot
import threading
import json

# Initialize the bot
bot = telebot.TeleBot(telegram_token)
# Global variable to store temporary message data for user confirmation
temporary_data: Dict[str, str] = {}


# Get user data from json file if it exists
def get_user_data() -> dict:
    """
    Get saved user data.

    :return:
        {
            user_id:{
                "available_saws":
                {
                     saw_number:{
                    "blocks_decommissioned":[
                        {
                            block_number:str,
                            block_cubic_meters:"int"
                        }
                    ],
                    "new_slabs":[
                        {
                            slab_number:
                            {
                                "width":int,
                                "length":int,
                                "thickness":int.
                                "square_meters":int
                            }
                        }
                    ],
                    "tech_cuts":[
                        {
                            "block_number":str,
                            "width":int,
                            "length":int
                            "square_meters":int
                        }
                    ],
                    "new_blocks":[
                        {
                            block_number:str,
                            "width":int,
                            "length":int,
                            "height":int,
                            "block_cubic_meters":int
                        }
                    ]
                },
            }
        }
    }

    """

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


# Find and set key in the user data nested dictionary structure
def find_and_set_key_recursive(data, target_key, new_value):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                data[key] = new_value
                return True
            if find_and_set_key_recursive(value, target_key, new_value):
                return True
    elif isinstance(data, list):
        for item in data:
            if find_and_set_key_recursive(item, target_key, new_value):
                return True

    return False


# Handler for /start command to initiate the process
@bot.message_handler(commands=['start'])
def process_start_message(message):
    reply_message = start_message()
    user_id = str(message.chat.id)
    bot.send_message(user_id, reply_message, parse_mode='Markdown')


# Handler to process user input for saw number
@bot.message_handler(commands=['saw'])
def process_saw_number(message):
    user_id: str = str(message.chat.id)
    split_message = message.text.split()
    saw_data = {
        "blocks_decommissioned": {},
        "new_slabs": [],
        "tech_cuts": [],
        "new_blocks": []
    }
    if len(split_message) > 1:
        saw_number = split_message[-1]
        if saw_number.isdigit():
            if user_id not in user_data:
                user_data[user_id] = {'available_saws': {saw_number: saw_data}, 'current_saw_number': saw_number}
            elif saw_number not in user_data[user_id]['available_saws']:
                user_data[user_id]['available_saws'][saw_number] = saw_data
                user_data[user_id]['current_saw_number'] = saw_number
            else:
                saw_data = user_data[user_id]['available_saws'][saw_number]
                user_data[user_id]['current_saw_number'] = saw_number
            save_user_data()
            saw_message = ""
            for key, value in saw_data.items():
                if not value:
                    empty_message = empty_entry_message(key=key, saw_number=saw_number)
                    saw_message += empty_message
                else:
                    if key == "blocks_decommissioned":
                        saw_message += blocks_decommissioned_message(key, value, saw_number)
                    if key == "new_slabs":
                        saw_message += new_slabs_message(key, value, saw_number)
                    if key == "tech_cuts":
                        saw_message += tech_cuts_message(key, value, saw_number)
                    if key == "new_blocks":
                        saw_message += new_blocks_message(key, value, saw_number)
            bot.send_message(user_id, saw_message, parse_mode='Markdown')
        else:
            bot.send_message(user_id, "Please enter a valid integer as the saw number.")

    else:
        bot.send_message(user_id, "Please enter a valid saw number after the /saw command. Example: /saw <number>")


# Handler to process user input for block number
@bot.message_handler(commands=['block'])
def process_block_number(message):
    user_id = str(message.chat.id)
    if user_id in user_data and 'available_saws' in user_data[user_id]:
        available_saws = user_data[user_id]['available_saws']
        current_saw_number = user_data[user_id].get('current_saw_number')
        if current_saw_number and current_saw_number in available_saws:
            block_number = message.text.split(' ')[-2]
            block_value = message.text.split(' ')[-1]

            blocks_decommissioned: Dict = available_saws[current_saw_number]['blocks_decommissioned']
            if block_number not in blocks_decommissioned:
                blocks_decommissioned[block_number] = block_value

                message = block_decommissioned_message(block_number=block_number, saw_number=current_saw_number)
                bot.send_message(user_id, message)
                save_user_data()
            else:
                value = blocks_decommissioned[block_number]
                global temporary_data
                temporary_data = {
                    'found_data': user_data.get(user_id, {}).get('available_saws', {}).get(current_saw_number, {}).get(
                        'blocks_decommissioned', {}), 'target_key': block_number, 'new_value': block_value}
                bot.send_message(user_id,
                                 f"It seems like you're trying to make changes to existing entry; {block_number}: {value}. Type /yes to accept changes or /no to discard")
        else:
            bot.send_message(user_id, "Please select saw number first")
    else:
        bot.send_message(user_id, "No user data found")


@bot.message_handler(commands=['yes'])
def process_submit_changes(message):
    user_id = str(message.chat.id)
    global temporary_data
    key = temporary_data['target_key']
    value = temporary_data['new_value']
    if find_and_set_key_recursive(data=temporary_data['found_data'], target_key=key, new_value=value):
        save_user_data()
        bot.send_message(user_id, f"Key {key} updated with new value {value}")


@bot.message_handler(commands=['no'])
def process_discard_changes():
    global temporary_data


# Handler to process user input for cubic meters and calculate square
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(message.text)
    bot.reply_to(message, message.text)


def start_bot_polling():
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"An error occurred: {e}")


polling_thread = threading.Thread(target=start_bot_polling)
polling_thread.start()

# my_saw_number = 7
# my_saw_data = {
#     "blocks_decommissioned": [
#         {
#             "block_number": "123E/1",
#             "block_m3": 3
#         },
#         {
#             "block_number": "123E/2",
#             "block_m3": 1
#         },
#     ],
#     "new_slabs": [
#         {
#             "123E/1-1":
#                 {
#                     "width": 1100,
#                     "length": 550,
#                     "thickness": 50,
#                     "square_meters": .60
#                 }
#         },
#         {
#             "123E/1-3":
#                 {
#                     "width": 1200,
#                     "length": 650,
#                     "thickness": 50,
#                     "square_meters": .75
#                 }
#         }
#     ],
#     "tech_cuts": [
#         {
#             "123/1":
#                 {
#                     "width": 1200,
#                     "length": 650,
#                     "square_meters": .75
#                 }
#         }
#     ],
#     "new_blocks": [
#         {
#             "123/2":
#                 {
#                     "width": 1200,
#                     "length": 650,
#                     "height": 500,
#                     "square_meters": .75
#                 }
#         }
#     ]
# }
# my_saw_message = ""
# for my_key, my_value in my_saw_data.items():
#     if not my_value:
#         my_empty_message = create_pretty_table(field_names=[my_key], rows=[["This entry is currently empty"]],
#                                                title=f"Saw number: {my_saw_number} selected")
#         my_saw_message += my_empty_message
#     else:
#         if my_key == "blocks_decommissioned":
#             my_saw_message += blocks_decommissioned_message(my_key, my_value, my_saw_number)
#         if my_key == "new_slabs":
#             my_saw_message += new_slabs_message(my_key, my_value, my_saw_number)
#         if my_key == "tech_cuts":
#             my_saw_message += tech_cuts_message(my_key, my_value, my_saw_number)
#         if my_key == "new_blocks":
#             my_saw_message += new_blocks_message(my_key, my_value, my_saw_number)

# print(my_saw_message)
print("Bot started successfully without errors!")
