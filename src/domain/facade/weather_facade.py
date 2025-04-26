from pandas import DataFrame

from src.domain.factory.weather_client_factory import WeatherClientFactory
from src.domain.models.cache_strategy import CacheStrategy
from src.domain.models.forecast_mode import ForecastMode
from src.infrastructure.api_clients.geopy_api import *
from src.utils.validation import Validation


class WeatherFacade:
    def __init__(self, api_name):
        self.cache = CacheStrategy()
        self.geo_client = GeoLocationClient()
        self.weather_client = WeatherClientFactory.create_client(api_name=api_name, cache=self.cache)

    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> DataFrame | None:
        try:
            location.coordinates = self.geo_client.get_coordinates(location=location)
            if Validation.validate_location(location=location):
                return self.weather_client.get_weather(location=location, mode=mode, time_interval=time_interval, time=time)
            return None
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
