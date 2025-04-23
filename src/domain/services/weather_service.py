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

    def _build_parameter(self, coordinates: Coordinates, mode: ForecastMode, time_interval: str, time: int) -> dict:
        if time_interval not in mode.time_interval:
            raise ValueError(f"Invalid time interval for {mode}. Please choose from {mode.time_interval}")

        params = {
            "latitude": coordinates.latitude,
            "longitude": coordinates.longitude,
            "timezone": "auto"
        }

        if time_interval == "current":
            params["current"] = "temperature_2m"
            return params
        elif time_interval == "daily":
            params["daily"] = ["temperature_2m_max", "temperature_2m_min"]
        else: #hourly
            params["hourly"] = "temperature_2m"

        if mode is ForecastMode.FORECAST:
            params["forecast"] = time
        else: #past
            params["forecast_days"] = 1
            params["past_days"] = time

        return params