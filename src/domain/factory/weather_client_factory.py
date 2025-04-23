from src.domain.models.cache_strategy import CacheStrategy
from src.infrastructure.api_clients.open_meteo_api import OpenMeteoClient
from src.infrastructure.api_clients.weather_api_client import WeatherAPIClient


class WeatherClientFactory:
    @staticmethod
    def create_client(api_name: str, cache: CacheStrategy) -> WeatherAPIClient:
        if api_name == 'open-meteo':
            return OpenMeteoClient(cache=cache)
        raise ValueError(f"unsupported API: {api_name}")