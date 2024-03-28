from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import pytz
from asin_to_sku import asin_to_sku
from keywords import key_words_usa, key_words_de, key_words_uk, key_words_fr
from telegram import channel_id_usa, channel_id_de, channel_id_uk, channel_id_fr
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


asin_codes = list(asin_to_sku.keys())

# start_date = datetime(2024, 3, 23, 16, 0)
end_date = datetime(2024, 4, 1, 9, 0)


if __name__ == '__main__':
    # # Текущее время
    current_time = datetime.now()

    # # Если текущее время меньше времени начала, ожидаем до начала
    # if current_time < start_date:
    #     wait_time = (start_date - current_time).total_seconds()
    #     time.sleep(wait_time)

    # Обновляем текущее время после ожидания
    # current_time = datetime.now(pytz.timezone('Europe/Moscow'))
    print(f"Цикл запущен в {current_time}")


    # Цикл, который выполняется каждые два часа
    while current_time < end_date:
        # Переходим к следующему времени запуска (через 3 часа)
        next_run_time = current_time + timedelta(hours=3)
        print(f"Время след-го запуска {next_run_time}")

        current_datetime = datetime.now(pytz.timezone('Europe/Moscow'))
        for_shot = current_datetime.replace(second=0, microsecond=0).strftime("%d_%m+%H_%M")
        date_for_excel = current_datetime.replace(minute=0, second=0, microsecond=0)
        msc_for_telegram = date_for_excel.strftime("%d.%m.%Y %H:%M")

        for region in ["com", "de", "co.uk", "fr"]:
            all_asins = []
            message_test = "<b><i>Проверка запущена</i></b>"
            sh_dict = {}
            if region == 'com':
                country = 'США'
                key_words = key_words_usa
                date_time = datetime.now(pytz.timezone('America/New_York')).replace(minute=0, second=0, microsecond=0,
                                                                                    tzinfo=None)
                bot_usa.send_message(channel_id_usa, message_test, parse_mode='HTML')
                postal_code = '10019'
                extension = 'extension_usa'
            elif region == 'de':
                country = 'Германия'
                key_words = key_words_de
                date_time = datetime.now(pytz.timezone('Europe/Berlin')).replace(minute=0, second=0, microsecond=0,
                                                                                 tzinfo=None)
                bot_de.send_message(channel_id_de, message_test, parse_mode='HTML')
                postal_code = "10115"
                extension = 'extension_de'
            elif region == 'fr':
                country = 'Франция'
                key_words = key_words_fr
                date_time = datetime.now(pytz.timezone('Europe/Paris')).replace(minute=0, second=0, microsecond=0,
                                                                                tzinfo=None)
                bot_fr.send_message(channel_id_fr, message_test, parse_mode='HTML')
                postal_code = "75000"
                extension = 'extension_fr'
            elif region == 'co.uk':
                country = 'Англия'
                key_words = key_words_uk
                date_time = datetime.now(pytz.timezone('Europe/London')).replace(minute=0, second=0, microsecond=0,
                                                                                 tzinfo=None)
                bot_uk.send_message(channel_id_uk, message_test, parse_mode='HTML')
                postal_code = "EC1Y 1BE"
                extension = 'extension_uk'

            local_for_telegram = date_time.replace(tzinfo=None).strftime("%d.%m.%Y %H:%M")

            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--remote-debugging-port=9222")  # Выберите свободный порт
            chrome_options.add_argument("--headless")
            s = Service('/home/amz_imp/chromedriver')
            chrome_options.add_argument(f'--load-extension=/home/amz_imp/{extension}')
            driver = webdriver.Chrome(service=s, options=chrome_options)
            driver.implicitly_wait(20)
            driver.set_page_load_timeout(20)  # Установка неявного ожидания
            driver.set_window_size(1920, 1080)
            driver.execute_script("document.body.style.zoom='60%'")
            first_url = f"https://www.amazon.{region}"
            driver.get(first_url)
            time.sleep(3)
            def captcha_check(driver):
                # Using find_elements instead of find_element
                captcha_elements = driver.find_elements(By.ID, "captchacharacters")
                if captcha_elements:
                    print("Капча обнаружена")
                    return True
                else:
                    print("Капча не обнаружена")
                    return False

            while captcha_check(driver):
                solve_amazon_captcha(driver)
                time.sleep(3)

            try:
                # Проверяем, есть ли на странице ссылка с указанным фрагментом в href
                link = driver.find_element(By.XPATH, "//a[contains(@href, 'ref=cs_503_link')]")
                if link:
                    # Если ссылка найдена, кликаем по ней
                    check_and_click_link(driver, region)
            except NoSuchElementException:
                # Если элемент не найден, это исключение будет поймано
                print("Link with 'ref=cs_503_link' not found.")

            accept_cookies(driver)

            try:
                set_location_on_amazon(driver, region, postal_code)
            except Exception as e:
                print(f"Error setting location: {e}")

            for keyword in key_words:
                base_url = "https://www.amazon.{region}/s?k={keyword}&page={page}"
                matched_asins = []

                for page in range(1, 21):
                    screenshot_needed = False
                    url = base_url.format(region=region, keyword=keyword, page=page)
                    try:
                        driver.get(url)
                        time.sleep(3)

                        matched_asins, all_asins, sh_dict = new_function(driver, region, matched_asins, all_asins, asin_codes, page,
                                                                date_for_excel, date_time, country, keyword, asin_to_sku,
                                                                for_shot, sh_dict)

                    except Exception as e:
                        # Обработка любых других исключений
                        print(f"Произошла неожиданная ошибка: {e}")
                        driver.get(url)
                        time.sleep(3)
                        matched_asins, all_asins, sh_dict = new_function(driver, region, matched_asins, all_asins, asin_codes, page,
                                                                date_for_excel, date_time, country, keyword, asin_to_sku,
                                                                for_shot, sh_dict)

                # обработка данных
                if len(matched_asins) == 0:
                    header = f"Country: {country} \nDate (MoscowTime): {msc_for_telegram} \nDate (LocalTime): {local_for_telegram} \nKeyword: {keyword}\n\n"
                    message = header + "Не найдено ни одного ASIN Onkron"
                else:
                    formatted_asins = []
                    for asin_set in matched_asins:
                        asin_link = f"[{asin_set[0]}]({asin_set[4]})"  # ASIN в квадратных скобках, URL в круглых
                        formatted_asin = (
                            f"ASIN: {asin_link}\n"
                            f"SKU: {asin_to_sku[asin_set[0]]}\n"
                            f"Page: {asin_set[1]}\n"
                            f"Position: {asin_set[2]}\n"
                            f"Type: {asin_set[3]}\n"
                        )
                        formatted_asins.append(formatted_asin)
                    header = f"Country: {country} \nDate (MoscowTime): {msc_for_telegram} \nDate (LocalTime): {local_for_telegram} \nKeyword: {keyword}\n\n"
                    message = header + "\n\n".join(formatted_asins)

                send_to_telegram(region, message)
            message_end = "<b><i>Проверка завершена</i></b>"
            end_telegram(region, message_end)
            print('Отправка скриншотов')
            webdav(sh_dict, region)
            driver.quit()
            unique_asins = []
            for asin_data in all_asins:
                if asin_data not in unique_asins:
                    unique_asins.append(asin_data)
            print('начало записи в базу данных')
            to_database(unique_asins)

        current_time = datetime.now()
        if current_time >= end_date:
            break
        # Расчет времени до следующего запуска
        time_to_next_run = (next_run_time - datetime.now()).total_seconds()
        print(f"До запуска осталось {time_to_next_run}")
        if time_to_next_run > 0:
            time.sleep(time_to_next_run)
