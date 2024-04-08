from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import pytz
from asin_to_sku import asin_to_sku
from keywords import key_words_usa, key_words_de, key_words_uk, key_words_fr
from database_mysql import to_database
from amazon_captcha import solve_amazon_captcha
from extract_asins import new_function
from check_and_click import check_and_click_link
from cookies import accept_cookies
from set_location import set_location_on_amazon
from telegram import send_to_telegram, end_telegram, bot_usa, bot_de, bot_uk, bot_fr
from WebDAV_ya_disk import webdav
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
load_dotenv()

chrome_options = Options()
chrome_options.binary_location = "C:\\Users\\e.turchaninova\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe"

# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--remote-debugging-port=9222")  # Выберите свободный порт
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--load-extension=C:\\Users\\e.turchaninova\\PycharmProjects\\pythonProject1\\extension_usa')

with webdriver.Chrome(options=chrome_options) as driver:
    print('создание экземпляра драйвера')
    driver.implicitly_wait(20)
    driver.set_page_load_timeout(20)  # Установка неявного ожидания
    driver.set_window_size(1920, 1080)
    driver.execute_script("document.body.style.zoom='60%'")
    first_url = "https://www.amazon.com"
    driver.get(first_url)
    time.sleep(10)


