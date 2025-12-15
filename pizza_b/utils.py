# utils/coordinates.py
def parse_coordinates(coord_string):
    """
    Парсит строку координат "широта,долгота"
    Возвращает (lat, lon) или (None, None) при ошибке
    """
    if not coord_string:
        return None, None
    
    try:
        lat_str, lon_str = coord_string.split(',')
        return float(lat_str.strip()), float(lon_str.strip())
    except (ValueError, IndexError):
        return None, None

def format_coordinates(lat, lon, decimals=19):
    """
    Форматирует координаты в строку
    """
    return f"{lat:.{decimals}f},{lon:.{decimals}f}"