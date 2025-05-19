from pandas import DataFrame

from domain.factory.weather_client_factory import WeatherClientFactory
from domain.models.cache_strategy import CacheStrategy
from infrastructure.api_clients.geopy_api import *
from utils.validation import Validation


class WeatherFacade:
    def __init__(self, api_name):
        self.cache = CacheStrategy()
        self.geo_client = GeoLocationClient()
        self.weather_client = WeatherClientFactory.create_client(api_name=api_name, cache=self.cache)

    @debug_log
    def get_weather(self, location: Location, time_interval: str, duration: int) -> DataFrame | None:
        try:
            location.coordinates = self.geo_client.get_coordinates(location=location)
            if Validation.validate_location(location=location):
                return self.weather_client.get_weather(location=location, time_interval=time_interval,
                                                       duration=duration)
            return None
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
