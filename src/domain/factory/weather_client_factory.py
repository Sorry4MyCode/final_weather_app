from src.domain.interface.weather_client_interface import WeatherClientInterface
from src.domain.models.cache_strategy import CacheStrategy
from src.domain.services.open_meteo_service import OpenMeteoService


class WeatherClientFactory:
    @staticmethod
    def create_client(api_name: str, cache: CacheStrategy) -> WeatherClientInterface:
        if api_name == "open-meteo":
            return OpenMeteoService(cache=cache)
        else:
            pass
        # TODO add other api
