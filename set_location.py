from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def set_location_on_amazon(driver, region, postal_code, attempt=1, max_attempts=3):
    try:
        time.sleep(1)
        # Нажатие на ссылку для изменения локации
        location_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "nav-global-location-popover-link"))
        )
        location_link.click()

        # Ожидание загрузки поля ввода и ввод почтового кода
        input_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "GLUXZipUpdateInput"))
        )
        input_field.send_keys(postal_code)
        #         input_field.send_keys(Keys.ENTER)

        apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "GLUXZipUpdate"))
        )
        apply_button.click()

        time.sleep(1)
        if region == "com":
            done_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "a-autoid-3-announce"))
            )
            done_button.click()
        elif region == "de":
            ActionChains(driver).send_keys(Keys.ENTER).perform()

        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(2)
        # Проверка, что локация установлена
        location_text = driver.find_element(By.ID, "nav-global-location-slot").text
        print(location_text)
        if postal_code in location_text:
            print("Локация успешно установлена.")
        else:
            print(f"Локация не установлена. Попытка {attempt} из {max_attempts}.")
            if attempt < max_attempts:
                set_location_on_amazon(driver, region, postal_code, attempt + 1, max_attempts)
            else:
                print("Превышено максимальное количество попыток установки локации.")
        # Ожидание обновления локации


    except (TimeoutException, ElementClickInterceptedException):
        if attempt < max_attempts:
            print(f"Повторная попытка установки локации. Попытка {attempt} из {max_attempts}.")
            time.sleep(2)  # небольшая задержка перед повторной попыткой
            set_location_on_amazon(driver, region, postal_code, attempt + 1, max_attempts)
        else:
            print("Превышено максимальное количество попыток установки локации.")

    except Exception as e:
        print(f"Произошла ошибка при установке локации: {e}")
        # Здесь можно добавить дополнительные действия для обработки ошибки
    action = ActionChains(driver)
    action.move_by_offset(10, 10)  # Перемещение курсора на 10 пикселей вправо и вниз от верхнего левого угла
    action.click()
    action.perform()