from PIL import Image
import requests
import time
from io import BytesIO
from dotenv import load_dotenv
import os
load_dotenv()

def screenshot(driver):
    # Получение размеров окна и всей страницы
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Скроллинг и создание скриншотов
    rectangles = []
    i = 0
    while i < total_height:
        driver.execute_script(f"window.scrollTo(0, {i})")
        time.sleep(0.2)  # Небольшая задержка для загрузки страницы
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))
        rectangles.append(image)
        i += viewport_height

    # Склеивание скриншотов в один файл
    stitched_image = Image.new('RGB', (driver.execute_script("return document.body.scrollWidth"), total_height))
    y_offset = 0

    for img in rectangles:
        stitched_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    # Сохраняем в BytesIO объект, а не на диск
    img_byte_arr = BytesIO()
    stitched_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def webdav(sh_dict, region):
    if region == "com":
        folder_region = 'screenshot_usa'
    elif region == "de":
        folder_region = 'screenshot_de'
    elif region == "co.uk":
        folder_region = 'screenshot_uk'
    elif region == "fr":
        folder_region = 'screenshot_fr'

    folder_general = 'скрины_выдача_амазон'
    headers = {
        'Authorization': f'OAuth {os.getenv('OAUTH_TOKEN')}',
        'Accept': '*/*',
        'Content-Type': 'image/png',
    }
    # Вызов функции для создания полностраничного скриншота
    for file_name, sh in sh_dict.items():
        url = f'https://webdav.yandex.ru/{folder_general}/{folder_region}/{file_name}'
        response = requests.put(url, headers=headers, data=sh)
        if response.status_code == 201:
            print('Скриншот успешно загружен.')
        else:
            print('Ошибка загрузки скриншота:', response.status_code, response.text)
