import requests


# получаем первый топоним
def geocode(toponym_to_find):
    url = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

    response = requests.get(url, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        return None #'Ошибка выполнения запроса'
    toponym = json_response['response']['GeoObjectCollection']['featureMember']
    if toponym:
        return toponym[0]['GeoObject']
    else:
        return None #'Несуществующий адрес'


# получаем координаты из топонима  latitude and longitude - числа
def get_coords(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if toponym:
        coords = toponym['Point']['pos']
        lon, lat = coords.split()
        return float(lon), float(lat)
    else:
        return None, None


# получение параметра ll и spn
def get_ll_spn(toponym_to_find):
    toponym = geocode(toponym_to_find)
    if toponym:
        coords = toponym['Point']['pos']
    ll = ','.join(coords.split())
    left, bottom = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    right, top = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    # вычисляем размеры
    x = abs(left - right) / 2
    y = abs(top - bottom) / 2
    spn = f"{x},{y}"
    return ll, spn
