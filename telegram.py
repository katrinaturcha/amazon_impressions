import telebot
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
import time

bot_token_de = '6896086571:AAHzUCNHHi3x0-jJelervlrEsdA8emHn88U'
bot_token_usa = '6799208243:AAHdSn_KheFq4GEiM9GlUfz21Dlna0CGAGc'
bot_token_fr = '6953093444:AAHlYrPtG10j7NwJJGZzjdnbGKzlF1EVl80'
bot_token_uk = '6666657055:AAFhEZ6kI1oA0g4B8mMRwLt9R1aFHq5oMg8'

channel_id_de = '-1002085666457'
channel_id_usa = '-1002049229125'
channel_id_fr = '-1002086444878'
channel_id_uk = '-1002034189233'

bot_de = telebot.TeleBot(bot_token_de)
bot_usa = telebot.TeleBot(bot_token_usa)
bot_fr = telebot.TeleBot(bot_token_fr)
bot_uk = telebot.TeleBot(bot_token_uk)

def send_to_telegram(region, message):
    # bot_de = telebot.TeleBot(bot_token_de)
    # bot_usa = telebot.TeleBot(bot_token_usa)
    # bot_fr = telebot.TeleBot(bot_token_fr)
    # bot_uk = telebot.TeleBot(bot_token_uk)
    # channel_id_de = '-1002085666457'
    # channel_id_usa = '-1002049229125'
    # channel_id_fr = '-1002086444878'
    # channel_id_uk = '-1002034189233'

    try:
        if region == "com":
            bot_usa.send_message(channel_id_usa, message, parse_mode='Markdown', timeout=30)
        elif region == "de":
            bot_de.send_message(channel_id_de, message, parse_mode='Markdown', timeout=30)
        elif region == "fr":
            bot_fr.send_message(channel_id_fr, message, parse_mode='Markdown', timeout=30)
        elif region == "co.uk":
            bot_uk.send_message(channel_id_uk, message, parse_mode='Markdown', timeout=30)
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
            bot_usa.send_message(channel_id_usa, message_end, parse_mode='HTML')
        elif region == "de":
            bot_de.send_message(channel_id_de, message_end, parse_mode='HTML')
        elif region == "fr":
            bot_fr.send_message(channel_id_fr, message_end, parse_mode='HTML')
        elif region == "co.uk":
            bot_uk.send_message(channel_id_uk, message_end, parse_mode='HTML')
    except ApiTelegramException as e:
        if e.error_code == 429:
            print("Превышен лимит запросов, ожидание 15 секунд...")
    except Exception as e:
        print(e)