from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha

def solve_amazon_captcha(driver):
    try:
        # Поиск элемента изображения капчи и извлечение его URL
        captcha_image = driver.find_element(By.XPATH, '//img[contains(@src, "captcha")]')
        captcha_url = captcha_image.get_attribute('src')

        # Решение капчи с использованием извлеченного URL
        captcha = AmazonCaptcha.fromlink(captcha_url)
        solution = captcha.solve()

        # Ввод решения капчи
        input_field = driver.find_element(By.ID, 'captchacharacters')
        input_field.send_keys(solution)

        # Нажатие кнопки подтверждения
        submit_button = driver.find_element(By.XPATH, '//button[contains(@class, "a-button-text")]')
        submit_button.click()

    except Exception as e:
        print("Проблема при обработке капчи:", e)