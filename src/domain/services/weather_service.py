from src.domain.models.forecast_mode import ForecastMode
from src.infrastructure.api_clients.geopy_adapter import *
from src.infrastructure.api_clients.open_meteo import *

class WeatherService:
    def __init__(self, geo_client: GeoLocationClient, weather_client: WeatherApiClient):
        self.geo_client = geo_client
        self.weather_client = weather_client

    def get_weather(self, location: Location, mode: ForecastMode, time: int) -> WeatherData:
        coordinates = self.geo_client.get_coordinates(location)

        return self.weather_client.get_weather(coordinates, mode)

    def _build_parameter(self, coordinates: Coordinates, mode: ForecastMode, time: int) -> dict:
        parameter = {
            "latitude": coordinates.latitude,
            "longitude": coordinates.longitude,
            "timezone": "auto"
        }

        if mode == ForecastMode.CURRENT:
            parameter["current"] = "temperature_2m"
            return parameter
        elif mode == ForecastMode.PAST:
            parameter["forecast_days"] = 1
            parameter["past_days"] = time
        else