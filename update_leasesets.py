import sqlite3

def insert_into_lease_sets(database_path, lease_sets):
    # Подключение к базе данных
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Создание таблицы, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lease_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                b32_address TEXT UNIQUE
            )
        ''')

        # Вставка данных в таблицу
        for address in lease_sets:
            cursor.execute('INSERT OR IGNORE INTO lease_sets (b32_address) VALUES (?)', (address,))

        # Подтверждение изменений и закрытие соединения
        conn.commit()
        print("Данные успешно добавлены в базу данных.")
    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)
    finally:
        conn.close()

# Чтение адресов лизсетов из файла
def read_lease_sets_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Путь к вашей базе данных
database_path = './ip_port_database.db'

# Путь к файлу leasesets.txt
leasesets_file_path = './leasesets.txt'

# Получение адресов лизсетов из файла
lease_sets_to_add = read_lease_sets_from_file(leasesets_file_path)

# Вызов функции для вставки данных в базу данных
insert_into_lease_sets(database_path, lease_sets_to_add)

