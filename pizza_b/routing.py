import requests
import os

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")  # Ключ из .env

class Routing:
    @staticmethod
    def CoordsFromAddr(address: str):
        """
        Преобразует адрес в координаты через Yandex Geocode API
        """
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": YANDEX_API_KEY,
            "geocode": address,
            "format": "json"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        try:
            pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lng, lat = map(float, pos.split())
            return {"lat": lat, "lng": lng}
        except (IndexError, KeyError):
            raise ValueError(f"Address not found: {address}")

    @staticmethod
    def GetRoute(start: dict, end: dict):
        """
        Строит маршрут через Yandex Directions API
        """
        # Yandex Directions API (Routing API) требует POST / GET с координатами
        url = "https://api.routing.yandex.net/v2/route"
        headers = {"Authorization": f"Api-Key {YANDEX_API_KEY}"}
        params = {
            "points": [
                {"lat": start["lat"], "lon": start["lng"]},
                {"lat": end["lat"], "lon": end["lng"]}
            ],
            "mode": "driving",
        }
        response = requests.post(url, json=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Простейший вариант: суммируем расстояние и время
        distance_m = data["routes"][0]["legs"][0]["distance"]
        duration_s = data["routes"][0]["legs"][0]["duration"]

        return {
            "distance_km": round(distance_m / 1000, 2),
            "duration_min": round(duration_s / 60, 1),
        }
