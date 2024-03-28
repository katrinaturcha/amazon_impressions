from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def accept_cookies(driver):
    try:
        accept_cookies_button = driver.find_element(By.ID, "sp-cc-accept")
        accept_cookies_button.click()
        # Явное ожидание исчезновения кнопки
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "sp-cc-accept")))
        print("Cookies accepted.")
    except NoSuchElementException:
        print("Accept cookies button not found.")
    except TimeoutException:
        print("Accept cookies button did not disappear in time.")

