import sqlite3
import requests
from concurrent.futures import ThreadPoolExecutor

# Параметры базы данных SQLite
db_file = "ip_port_database.db"
table_name = "lease_sets"

# Прокси-адрес
proxy_url = "http://localhost:4444"

# Целевая таблица для сохранения результатов
result_table = "websites"

# Функция для проверки веб-сайта
def check_website(url):
    try:
        # Используем прокси для запроса
        response = requests.get(url, proxies={"http": proxy_url, "https": proxy_url}, timeout=10)

        # Если код ответа 200 и нет таймаута, сохраняем в базу данных
        if response.status_code == 200:
            save_result(url)
        else:
            print(f"Ошибка: {url} вернул код {response.status_code}")
    except requests.Timeout:
        print(f"Таймаут: {url}")

# Функция для сохранения результата в базу данных
def save_result(url):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Создаем таблицу, если её ещё нет
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {result_table} (url TEXT)")

    # Вставляем данные
    cursor.execute(f"INSERT INTO {result_table} (url) VALUES (?)", (url,))
    print("Added {}".format(url))
    conn.commit()
    conn.close()

# Функция для обработки одной строки из базы данных
def process_row(row):
    url = f"http://{row[1]}.b32.i2p"  # Собираем полный URL
    check_website(url)

# Получаем список URL из базы данных
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {table_name}")
urls = cursor.fetchall()
conn.close()

# Используем многопоточность для параллельной проверки
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_row, urls)

