from typing import List, OrderedDict

from prettytable import PrettyTable, HRuleStyle, VRuleStyle

from config import telegram_token
import telebot
import threading
import json

# Initialize the bot
bot = telebot.TeleBot(telegram_token)


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


# function to create pretty table
def create_pretty_table(field_names: List[str], rows: List[List:str],
                        title: str = "Welcome! These are all input options:"):
    table = PrettyTable(hrules=HRuleStyle.ALL, vrules=VRuleStyle.ALL, header=True, header_style='upper')
    table.align = 'l'
    table.title = title
    table.field_names = field_names
    table.add_rows(rows)

    return f'```\n{table}```'


# Handler for /start command to initiate the process
@bot.message_handler(commands=['start'])
def start_message(message):
    table_start = create_pretty_table(
        field_names=["Commands", "Input Options"],
        rows=[
            ["/start", "Start interaction with bot"],
            ["/saw", "/saw <number>"],
            ["/block", "/block, <number>, <cubic meters>"],
            ["/slab", "/slab, <number>, <width>, <height>, <thickness>"],
            ["/tech", "/tech, <block number>, <width>, <height>"]
        ])

    user_id = str(message.chat.id)
    bot.send_message(user_id,
                     table_start,
                     parse_mode='Markdown'
                     )


# Handler to process user input for saw number
@bot.message_handler(commands=['saw'])
def process_saw_number(message):
    user_id: str = str(message.chat.id)
    split_message = message.text.split()
    saw_data = {
        "blocks_decommissioned": [],
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
                    empty_message = create_pretty_table(field_names=[key], rows=[["This entry is currently empty"]],
                                                        title=f"Saw number: {saw_number} selected")
                    saw_message += empty_message

            bot.send_message(user_id,
                             saw_message,
                             parse_mode='Markdown')
        else:
            bot.send_message(user_id, "Please enter a valid integer as the saw number.")

    else:
        bot.send_message(user_id, "Please enter a valid saw number after the /saw command. Example: /saw <number>")


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
        print(f"An error occurred: {e}")


polling_thread = threading.Thread(target=start_bot_polling)


# polling_thread.start()

def blocks_decommissioned_message(key, value, saw_number) -> str:
    unique_keys = list(OrderedDict.fromkeys(key for d in value for key in d.keys()))
    row_values = []
    for item in value:
        row_values.append(list(item.values()))
    message = create_pretty_table(field_names=unique_keys, rows=row_values,
                                  title=f"Saw # {saw_number}, {key}")
    return message


def new_slabs_message(key, value, saw_number) -> str:
    title = key
    field_names = ["number", "w", "l", "t", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["thickness"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message


def tech_cuts_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message


def new_blocks_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "h", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["height"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message


def calculate_square_meters(width_mm: int, length_mm: int) -> float:
    width_cm = width_mm / 10
    length_cm = length_mm / 10
    area_cm2 = width_cm * length_cm
    area_m2 = area_cm2 / 10000
    area_m2_formatted = format(area_m2, '.2f')
    return float(area_m2_formatted)


my_saw_number = 7
my_saw_data = {
    "blocks_decommissioned": [
        {
            "block_number": "123E/1",
            "block_m3": 3
        },
        {
            "block_number": "123E/2",
            "block_m3": 1
        },
    ],
    "new_slabs": [
        {
            "123E/1-1":
                {
                    "width": 1100,
                    "length": 550,
                    "thickness": 50,
                    "square_meters": .60
                }
        },
        {
            "123E/1-3":
                {
                    "width": 1200,
                    "length": 650,
                    "thickness": 50,
                    "square_meters": .75
                }
        }
    ],
    "tech_cuts": [
        {
            "123/1":
                {
                    "width": 1200,
                    "length": 650,
                    "square_meters": .75
                }
        }
    ],
    "new_blocks": [
        {
            "123/2":
                {
                    "width": 1200,
                    "length": 650,
                    "height": 500,
                    "square_meters": .75
                }
        }
    ]
}
my_saw_message = ""
for my_key, my_value in my_saw_data.items():
    if not my_value:
        my_empty_message = create_pretty_table(field_names=[my_key], rows=[["This entry is currently empty"]],
                                               title=f"Saw number: {my_saw_number} selected")
        my_saw_message += my_empty_message
    else:
        if my_key == "blocks_decommissioned":
            my_saw_message += blocks_decommissioned_message(my_key, my_value, my_saw_number)
        if my_key == "new_slabs":
            my_saw_message += new_slabs_message(my_key, my_value, my_saw_number)
        if my_key == "tech_cuts":
            my_saw_message += tech_cuts_message(my_key, my_value, my_saw_number)
        if my_key == "new_blocks":
            my_saw_message += new_blocks_message(my_key, my_value, my_saw_number)

print(my_saw_message)
print("Bot started successfully without errors!")
