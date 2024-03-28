from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_and_click_link(driver, region):
    try:
        # Формирование URL для перехода
        link_url = f"https://www.amazon.{region}/ref=cs_503_link"

        # Явное ожидание кликабельности ссылки по атрибуту href
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{link_url}')]"))
        )
        link.click()

        # Явное ожидание, что ссылка больше не кликабельна (предполагая, что страница изменилась после клика)
        WebDriverWait(driver, 10).until_not(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{link_url}')]"))
        )
        print("Переход по ссылке выполнен.")
        return True

    except TimeoutException:
        print("Ссылка не исчезла после клика.")
        return False
    except NoSuchElementException:
        print("Ссылка не найдена.")
        return False