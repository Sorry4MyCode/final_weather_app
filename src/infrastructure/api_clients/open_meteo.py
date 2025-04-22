from abc import abstractmethod

from requests_cache import CachedSession

from src.domain.models.location import Coordinates
from src.domain.models.weather_data import WeatherData


class WeatherApiClient(ABC):
    @abstractmethod
    def get_forecast(self, coordinates: Coordinates) -> WeatherData:


class OpenMeteoClient(WeatherApiClient):
    def __init__(self, cache: CacheStrategy):
        self.session = CachedSession(cache)

    def get_forecast(self, coordinates: Coordinates, mode: ForecastMode):
        return self.api._parse_response(api_response)