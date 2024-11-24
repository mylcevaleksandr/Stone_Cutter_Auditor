from config import telegram_token
import telebot

bot = telebot.TeleBot(telegram_token)

print("Hello World!!!")

print(telegram_token)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
