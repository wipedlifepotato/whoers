import requests
import tarfile
import os

# Загрузка файла
url = 'https://antebeot.world/netDb.tar'
response = requests.get(url)

if response.status_code == 200:
    # Сохранение в файл
    with open('outf', 'wb') as out:
        out.write(response.content)

    # Папка для распаковки
    target_folder = 'tmp'

    # Проверка наличия папки tmp, создание при необходимости
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Распаковка
    with tarfile.open('outf', 'r') as tar:
        tar.extractall(target_folder)

    print(f"Файл успешно загружен и распакован в папку {target_folder}")
else:
    print(f"Ошибка: Невозможно получить содержимое. Код состояния: {response.status_code}")

