from bs4 import BeautifulSoup
from screenshot import fullpage_screenshot
import os
from WebDAV_ya_disk import screenshot

def extract_asins_from_page(driver, region):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    asin_data = {}

    for div in soup.find_all("div", {"data-asin": True}):
        asin = div.get('data-asin').strip()
        if asin:
            # Находим позицию
            position_div = soup.find("div", {"data-csa-c-item-id": lambda x: x and x.endswith(asin)})
            position = int(position_div.get("data-csa-c-pos")) if position_div and position_div.get(
                "data-csa-c-pos").isdigit() else None

            # Проверяем, является ли продукт спонсируемым
            sponsored_span = div.find("span", text="Sponsored")
            sponsored = "Sponsored" if sponsored_span else "Not Sponsored"

            link = f'https://www.amazon.{region}/dp/' + asin

            # Находим заголовок
            title_span = div.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
            title = title_span.get_text() if title_span else None

            asin_data[asin] = [position, sponsored, link, title]

    return asin_data


def new_function(driver, region, matched_asins, all_asins, asin_codes, page, date_for_excel, date_time, country,
                 keyword, asin_to_sku, for_shot, sh_dict):
    asin_data = extract_asins_from_page(driver, region)
    screenshot_needed = False
    for asin, data in asin_data.items():
        position, sponsored, link, title = data
        if asin in asin_codes:
            screenshot_needed = True
            matched_asins.append((asin, page, position, sponsored, link))
            all_asins.append((date_for_excel, date_time, country, keyword, asin, asin_to_sku[asin], page, position,
                              sponsored, title, link))
    # else: all_asins.append((date_for_excel, date_time, country, keyword, asin, "", page, position, sponsored, title,
    # link))
    if screenshot_needed:
        file_name = f"{region}_{keyword}_p{page}_dt{for_shot}.png"
        # file_path_shot = os.path.join(folder_path, file_name)
        # file_path_yandex = os.path.join(yandex_disk_path, file_name)
        # Создание скриншота
        # fullpage_screenshot(driver, file_path_shot, file_path_yandex)

        binary = screenshot(driver)
        sh_dict[file_name] = binary
    return matched_asins, all_asins, sh_dict
