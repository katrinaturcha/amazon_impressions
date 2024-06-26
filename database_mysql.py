import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

# Конфигурация для подключения к базе данных
def to_database(all_asins):
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'raise_on_warnings': True
    }
    connection = None

    try:
        # Установление подключения к базе данных
        connection = mysql.connector.connect(**config)
        # Создание курсора
        cursor = connection.cursor()
        # Выполнение запроса INSERT
        insert_query = '''
            INSERT INTO amz_imp (date_time_msc, local_time, country, keyword, asin, sku, page, position, type, title, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

        for asin in all_asins:
            cursor.execute(insert_query, asin)

        # Коммит изменений
        connection.commit()

        print(f"Успешно вставлено {cursor.rowcount} строк.")

    except mysql.connector.Error as e:
        print("Ошибка при подключении к MySQL:", e)

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Соединение с MySQL закрыто")
