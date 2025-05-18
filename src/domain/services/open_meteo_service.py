from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import pandas as pd
from pandas import DataFrame

import config.settings
from config.logging_config import debug_log
from src.domain.interface.weather_client_interface import WeatherClientInterface
from src.domain.models.cache_strategy import CacheStrategy
from src.domain.models.location import Location
from src.domain.models.weather_data import WeatherData
from src.infrastructure.api_clients.open_meteo_api import OpenMeteoClient


class OpenMeteoService(WeatherClientInterface):
    def __init__(self, cache: CacheStrategy):
        self.client = OpenMeteoClient(cache=cache)

    @debug_log
    def get_weather(self, location: Location, time_interval: str, duration: int) -> DataFrame:
        params = self._build_parameter(location=location, time_interval=time_interval, duration=duration)
        response = self.client.get_weather(params=params, url="https://api.open-meteo.com/v1/forecast")
        return self._handle_response(response=response, params=params)

    @debug_log
    def _build_parameter(self, location: Location, time_interval: str, duration: int) -> dict:
        params = {
            "latitude": location.coordinates.latitude,
            "longitude": location.coordinates.longitude,
            "timezone": "Europe/Berlin",
            "forecast_days": abs(duration[1]),
            "past_days": abs(duration[0])
        }

        # TODO fix forecast/past days

        if time_interval == "days":
            params["daily"] = config.settings.daily_params
        else:  # Hours
            params["hourly"] = config.settings.hourly_params
        return params

    @debug_log
    def _handle_response(self, response, params: dict) -> DataFrame:
        if isinstance(response, list):
            response = response[0]

        if "daily" in params:
            weather_data = self._daily_data_handling(response=response, params=params)
        elif "hourly" in params:
            weather_data = self._hourly_data_handling(response=response, params=params)
        else:
            raise ValueError("Unexpected response parameters")

        return self._dictionary_to_dataframe(weather_data=weather_data)

    @staticmethod
    @debug_log
    def _dictionary_to_dataframe(weather_data: list) -> DataFrame:
        data = [asdict(weather) for weather in weather_data]
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        df.dropna(how='all', axis=1, inplace=True)
        return df

    @staticmethod
    @debug_log
    def _hourly_data_handling(response, params: dict) -> list[WeatherData]:
        hourly = response.Hourly()

        start_time = datetime.fromtimestamp(hourly.Time(), tz=timezone.utc)
        end_time = datetime.fromtimestamp(hourly.TimeEnd(), tz=timezone.utc)
        interval = hourly.Interval()

        timestamps = []
        current_time = start_time
        while current_time < end_time:
            timestamps.append(current_time)
            current_time += timedelta(seconds=interval)

        # Extract all hourly variables in order
        variables = []
        for i in range(len(params["hourly"])):
            var = hourly.Variables(i).ValuesAsNumpy()
            variables.append(var)

        weather_data_list = []
        params_order = config.settings.hourly_params
        for i in range(len(timestamps)):
            current_values = [var[i] for var in variables]
            data = dict(zip(params_order, current_values))

            # Create WeatherData instance
            weather_data = WeatherData(
                timestamp=timestamps[i],
                temperature_2m=data.get("temperature_2m"),
                weather_code=data.get("weather_code"),
                apparent_temperature_2m=data.get("apparent_temperature"),
                relative_humidity_2m=data.get("relative_humidity_2m"),
                snowfall=data.get("snowfall"),
                shower=data.get("showers"),
                rain=data.get("rain"),
                cloud_cover_low=data.get("cloud_cover_low"),
                cloud_cover_mid=data.get("cloud_cover_mid"),
                cloud_cover_high=data.get("cloud_cover_high"),
                cloud_cover=data.get("cloud_cover"),
                visibility=data.get("visibility"),
                wind_speed_10m=data.get("wind_speed_10m"),
                wind_direction_10m_dominant=data.get("wind_direction_10m"),
                wind_gust_10m=data.get("wind_gusts_10m")
            )
            weather_data_list.append(weather_data)

        return weather_data_list

    @staticmethod
    @debug_log
    def _daily_data_handling(response, params: dict) -> list[WeatherData]:
        daily = response.Daily()

        start_time = datetime.fromtimestamp(daily.Time(), tz=timezone.utc)
        end_time = datetime.fromtimestamp(daily.TimeEnd(), tz=timezone.utc)
        interval = daily.Interval()

        timestamps = []
        current_time = start_time
        while current_time < end_time:
            timestamps.append(current_time)
            current_time += timedelta(seconds=interval)

        # Extract all hourly variables in order
        variables = []
        for i in range(len(params["daily"])):
            var = daily.Variables(i).ValuesAsNumpy()
            variables.append(var)

        weather_data_list = []
        params_order = config.settings.daily_params
        for i in range(len(timestamps)):
            current_values = [var[i] for var in variables]
            data = dict(zip(params_order, current_values))

            weather_data = WeatherData(
                timestamp=timestamps[i],
                temperature_2m_max=data.get("temperature_2m_max"),
                temperature_2m_min=data.get("temperature_2m_min"),
                weather_code=data.get("weather_code"),
                apparent_temperature_max=data.get("apparent_temperature_max"),
                apparent_temperature_min=data.get("apparent_temperature_min"),
                apparent_temperature_mean=data.get("apparent_temperature_mean"),
                temperature_2m_mean=data.get("temperature_2m_mean"),
                rain_sum=data.get("rain_sum"),
                showers_sum=data.get("showers_sum"),
                snowfall_sum=data.get("snowfall_sum"),
                wind_speed_10m_max=data.get("wind_speed_10m_max"),
                wind_direction_10m_dominant=data.get("wind_direction_10m_dominant"),
                visibility_max=data.get("visibility_max"),
                visibility_min=data.get("visibility_min"),
                visibility_mean=data.get("visibility_mean"),
                wind_speed_10m_mean=data.get("wind_speed_10m_mean"),
                wind_speed_10m_min=data.get("wind_speed_10m_min"),
                wind_gust_10m_min=data.get("wind_gusts_10m_min"),
                wind_gust_10m_max=data.get("wind_gusts_10m_max"),
                wind_gust_10m_mean=data.get("wind_gusts_10m_mean"),
                relative_humidity_min=data.get("relative_humidity_2m_min"),
                relative_humidity_max=data.get("relative_humidity_2m_max"),
                relative_humidity_mean=data.get("relative_humidity_2m_mean"),
                cloud_cover_mean=data.get("cloud_cover_mean"),
                cloud_cover_max=data.get("cloud_cover_max"),
                cloud_cover_min=data.get("cloud_cover_min")
            )
            weather_data_list.append(weather_data)

        return weather_data_list
