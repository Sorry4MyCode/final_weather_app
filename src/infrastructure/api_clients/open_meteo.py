from abc import abstractmethod

from requests_cache import CachedSession

from src.domain.models import cache_strategy
from src.domain.models.cache_strategy import CacheStrategy
from src.domain.models.location import Coordinates
from src.domain.models.weather_data import WeatherData


class WeatherApiClient():
    @abstractmethod
    def get_forecast(self, coordinates: Coordinates) -> WeatherData:


class OpenMeteoClient(WeatherApiClient):
    def __init__(self, cache: CacheStrategy):
        self._om = OMClient(session=cache_strategy.session)

    def get_forecast(self, coordinates: Coordinates, mode: ForecastMode):
        return self.api._parse_response(api_response)