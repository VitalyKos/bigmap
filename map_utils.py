import sys
import requests


def get_map(api_params):
    api_map='http://static-maps.yandex.ru/1.x/'
    response = requests.get(api_map, params=api_params)

    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "data//map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file