import time
import telebot
from telebot.apihelper import ApiTelegramException
from dotenv import load_dotenv
import os
load_dotenv()

bot_usa = telebot.TeleBot(os.getenv('BOT_TOKEN_USA'))
bot_de = telebot.TeleBot(os.getenv('BOT_TOKEN_DE'))
bot_uk = telebot.TeleBot(os.getenv('BOT_TOKEN_UK'))
bot_fr = telebot.TeleBot(os.getenv('BOT_TOKEN_FR'))

def send_to_telegram(region, message):
    try:
        if region == "com":
            bot_usa.send_message(os.getenv('CHANNEL_ID_USA'), message, parse_mode='Markdown', timeout=30)
        elif region == "de":
            bot_de.send_message(os.getenv('CHANNEL_ID_DE'), message, parse_mode='Markdown', timeout=30)
        elif region == "fr":
            bot_fr.send_message(os.getenv('CHANNEL_ID_FR'), message, parse_mode='Markdown', timeout=30)
        elif region == "co.uk":
            bot_uk.send_message(os.getenv('CHANNEL_ID_UK'), message, parse_mode='Markdown', timeout=30)
    except ApiTelegramException as e:
        if e.error_code == 429:
            print("Превышен лимит запросов, ожидание 15 секунд...")
            time.sleep(15)
            send_to_telegram(region, message)
    except Exception as e:
        return str(e)

def end_telegram(region, message_end):
    try:
        if region == "com":
            bot_usa.send_message(os.getenv('CHANNEL_ID_USA'), message_end, parse_mode='HTML')
        elif region == "de":
            bot_de.send_message(os.getenv('CHANNEL_ID_DE'), message_end, parse_mode='HTML')
        elif region == "fr":
            bot_fr.send_message(os.getenv('CHANNEL_ID_FR'), message_end, parse_mode='HTML')
        elif region == "co.uk":
            bot_uk.send_message(os.getenv('CHANNEL_ID_UK'), message_end, parse_mode='HTML')
    except ApiTelegramException as e:
        if e.error_code == 429:
            print("Превышен лимит запросов, ожидание 15 секунд...")
    except Exception as e:
        print(e)