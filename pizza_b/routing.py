apikey = '34ef38d4d8fc4d5ba29da472883852f1'
yapikey = 'f4501883-d055-434f-af32-c819a8adf539'
import requests
import json
from .utils import format_coordinates, parse_coordinates
from django.conf import settings
from django.core.cache import cache

class Routing:
    def Geocode(self, address):
        """
        Преобразует адрес в координаты, используя кэширование.
        """
        api_key = yapikey
        cache_key = f'yandex_geocode:{address}'
        result = cache.get(cache_key)
        if result is not None:
            return result
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': api_key,
            'lang': 'ru_RU',
            'geocode': address,
            'format': 'json'
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()

            try:
                pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                # pos возвращается в формате "долгота широта"
                lon, lat = pos.split()
                result = format_coordinates(lon,lat)
            except (KeyError, IndexError):
                result = 'Адрес не найден или ответ имеет неожиданную структуру.'

        except requests.exceptions.RequestException as e:
            result = f'Ошибка сети или API: {str(e)}'
        except json.JSONDecodeError:
            result = 'Не удалось разобрать ответ от сервера.'

        cache.set(cache_key, result, timeout=86400)
        return result
    def GetRoute(self, start_location, end_location, mode='driving'): 
        """
        Строит маршрут между двумя координатами, используя кэширование.
        mode: 'driving' (авто), 'transit' (общественный транспорт), 'walking' (пешком)[citation:4][citation:10].
        """
        api_key = yapikey
        # Создаем ключ для кэша на основе всех параметров
        cache_key = f'yandex_route:{start_location}:{end_location}:{mode}'
        start_location_lat, start_location_lon = parse_coordinates(start_location)
        end_location_lat, end_location_lon = parse_coordinates(end_location)
        result = cache.get(cache_key)
        if result is not None:
            return result

        url = "https://api.routing.yandex.net/v2/route"
        params = {
            'apikey': api_key,
            'waypoints': f"{start_location_lat},{start_location_lon}|{end_location_lat},{end_location_lon}",
            'mode': mode, 
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            route = data['routes'][0]
            result = {
                'distance_meters': route['legs'][0]['distance']['value'],  # Расстояние в метрах
                'duration_seconds': route['legs'][0]['duration']['value'],  # Время в секундах
                # Можно также сохранить геометрию маршрута (polyline) для отрисовки на карте
                'geometry': route['legs'][0]['geometry']
            }
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            result = {'error': f'Ошибка при построении маршрута: {str(e)}'}

        timeout = 5
        cache.set(cache_key, result, timeout=timeout)
        return result

        #  """ 
        #  Получает маршрут между двумя точками через OpenRouteService
    
        #   Args:
        # coords_start: tuple/list [lat, lon] или [lon, lat] начальной точки
        # coords_end: tuple/list [lat, lon] или [lon, lat] конечной точки
        # profile: тип маршрута (driving-car, foot-walking, cycling-regular и т.д.)
        # api_url: URL локального ORS сервера
    
        #  Returns:
        # dict: данные маршрута или None в случае ошибки
        # """
        # if isinstance(coords_start, (list, tuple)) and len(coords_start) == 2:
        #     start_coords = [float(coords_start[1]), float(coords_start[0])]
        # else:
        #     raise ValueError("coords_start должен быть списком/кортежем [lat, lon] или [lon, lat]")
        # if isinstance(coords_end, (list, tuple)) and len(coords_end) == 2:
        #     end_coords = [float(coords_end[1]), float(coords_end[0])]
        # else:
        #     raise ValueError("coords_end должен быть списком/кортежем [lat, lon] или [lon, lat]")
            

        # url = f"{api_url}/ors/v2/directions/{profile}"
            
        # payload = {
        #         "coordinates": [start_coords, end_coords],
        #         "instructions": True, 
        #         "language": "ru",  
        #         "units": "km", 
        #         "geometry": True, 
        #         "geometry_format": "geojson",  
        #         "elevation": True,
        #         "options": {
        #             "avoid_features": ["ferries", "tunnels"]  
        #         }
        #     }
            

        #     headers = {
        #         'Content-Type': 'application/json',
        #         'Accept': 'application/json, application/geo+json'
        #     }
            
        #     try:
        #         response = requests.post(
        #             url,
        #             data=json.dumps(payload),
        #             headers=headers,
        #             timeout=5  
        #         )
                
        #         if response.status_code == 200:
        #             return response.json()
        #         else:
        #             print(f"Ошибка ORS API: {response.status_code}")
        #             print(f"Ответ: {response.text}")
        #             return None
                    
        #     except requests.exceptions.ConnectionError:
        #         print(f"Не удалось подключиться к ORS серверу по адресу {api_url}")
        #         return None
        #     except requests.exceptions.Timeout:
        #         print("Таймаут при запросе к ORS")
        #         return None
        #     except requests.exceptions.RequestException as e:
        #         print(f"Ошибка запроса: {e}")
        #         return None
        #         return None