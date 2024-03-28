import psycopg2

def to_database(all_asins):
# Данные для подключения к базе данных
    dbname = "onkron"
    user = "on_kron"
    password = "kd93h4D"
    host = "localhost"
    port = "22"

    try:
        # Подключение к базе данных
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # SQL-запрос для вставки данных
        insert_query = """
        INSERT INTO public.amz_imp (date_time_msc, local_time, country, keyword, asin, sku, page, position, type, title, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Выполнение запроса для каждого набора данных
        for asin_data in all_asins:
            cur.execute(insert_query, asin_data)

        # Фиксация изменений
        conn.commit()

        # Закрытие соединения
        cur.close()
        conn.close()

    except psycopg2.DatabaseError as error:
        print(f"Ошибка базы данных: {error}")
    finally:
        if conn is not None:
            conn.close()


