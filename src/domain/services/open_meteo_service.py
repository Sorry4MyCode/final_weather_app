from src.domain.models.cache_strategy import CacheStrategy
from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location
from src.domain.models.weather_data import WeatherData
from src.infrastructure.api_clients.open_meteo_api import OpenMeteoClient
from src.utils.validation import Validation

class OpenMeteoService:
    def __init__(self, cache: CacheStrategy):
        self.client = OpenMeteoClient(cache=cache)

    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> list[WeatherData]:
        params = self._build_parameter(location=location, mode=mode, time_interval=time_interval, time=time)
        response = self.client.get_weather(params=params, url="https://api.open-meteo.com/v1/forecast")
        #TODO validate response
        return self._handle_response(response=response, params=params)

    def _build_parameter(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> dict:
        #TODO finish this
        params = {
            "latitude": location.coordinates.latitude,
            "longitude": location.coordinates.longitude,
            "timezone": "auto"
        }

        if time_interval == "current":
            params["current"] = "temperature_2m"
            return params
        elif time_interval == "daily":
            params["daily"] = ["temperature_2m_max", "temperature_2m_min", "weather_code", "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean", "temperature_2m_mean", "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant", "visibility_mean", "visibility_min", "visibility_max", "wind_speed_10m_mean", "winddirection_10m_dominant", "wind_speed_10m_min", "wind_gusts_10m_min", "wind_gusts_10m_mean", "relative_humidity_2m_min", "relative_humidity_2m_max", "relative_humidity_2m_mean", "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min"]
        else: #hourly
            params["hourly"] = "temperature_2m"

        if mode is ForecastMode.FORECAST:
            params["forecast"] = time
        else: #past
            params["forecast_days"] = 1
            params["past_days"] = time

        return params

    def _handle_response(response, params: dict):
        #TODO finish this
        if "daily" in params:
            daily = response.Daily()




        return list[WeatherData]