from src.domain.factory.weather_client_factory import WeatherClientFactory
from src.domain.models.forecast_mode import ForecastMode
from src.infrastructure.api_clients.geopy_adapter import *
from src.infrastructure.api_clients.open_meteo_api import *

class WeatherService:
    def __init__(self, api_name):
        self.geo_client = GeoLocationClient
        self.weather_client = WeatherClientFactory(api_name)

    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str, time: int):
        location.coordinates = self.geo_client.get_coordinates(location)
        if validate_location(self, location=location):
            return self.weather_client.get_weather(location=location, mode=mode, time_interval=time_interval, time=time)