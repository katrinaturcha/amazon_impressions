from PIL import Image
import time
import os

def fullpage_screenshot(driver, file_path_shot, file_path_yandex):
    # Получение размеров окна и всей страницы
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Скроллинг и создание скриншотов
    rectangles = []
    i = 0
    while i < total_height:
        driver.execute_script(f"window.scrollTo(0, {i})")
        time.sleep(0.2)  # Небольшая задержка для загрузки страницы
        img_file = f"part_{i}.png"
        driver.get_screenshot_as_file(img_file)
        rectangles.append(img_file)
        i += viewport_height

    # Склеивание скриншотов в один файл
    stitched_image = Image.new('RGB', (driver.execute_script("return document.body.scrollWidth"), total_height))
    y_offset = 0

    for img_file in rectangles:
        # Добавьте проверку на существование файла и его размер
        if os.path.exists(img_file) and os.path.getsize(img_file) > 0:
            img = Image.open(img_file)
            stitched_image.paste(img, (0, y_offset))
            y_offset += img.size[1]
            img.close()
            os.remove(img_file)  # Удаление временных файлов
        else:
            print(f"Файл {img_file} не найден или пуст.")

    stitched_image.save(file_path_shot)
    stitched_image.save(file_path_yandex)
    stitched_image.close()
