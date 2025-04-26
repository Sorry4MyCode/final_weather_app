import math
from dataclasses import asdict

import pandas as pd
from pandas import DataFrame

from src.domain.interface.weather_client_interface import WeatherClientInterface
from src.domain.models.cache_strategy import CacheStrategy
from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location
from src.domain.models.weather_data import WeatherData
from src.infrastructure.api_clients.open_meteo_api import OpenMeteoClient

from datetime import datetime, timedelta, timezone


# noinspection PyTypeChecker
class OpenMeteoService(WeatherClientInterface):
    def __init__(self, cache: CacheStrategy):
        self.client = OpenMeteoClient(cache=cache)

    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> DataFrame:
        params = self._build_parameter(location=location, mode=mode, time_interval=time_interval, time=time)
        response = self.client.get_weather(params=params, url="https://api.open-meteo.com/v1/forecast")
        # TODO validate response
        return self._handle_response(response=response, params=params)

    def _build_parameter(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> dict:
        params = {
            "latitude": location.coordinates.latitude,
            "longitude": location.coordinates.longitude,
            "timezone": "auto"
        }

        if time_interval == "current":
            params["current"] = ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "snowfall",
                                 "showers", "rain",
                                 "weather_code", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]
            return params
        elif time_interval == "daily":
            params["daily"] = ["temperature_2m_min", "temperature_2m_max", "weather_code", "apparent_temperature_max",
                               "apparent_temperature_min", "apparent_temperature_mean", "temperature_2m_mean",
                               "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max",
                               "wind_direction_10m_dominant", "visibility_mean", "visibility_min", "visibility_max",
                               "wind_speed_10m_mean", "wind_speed_10m_min", "wind_gusts_10m_min", "wind_gusts_10m_max", "wind_gusts_10m_mean",
                               "relative_humidity_2m_mean", "relative_humidity_2m_max", "relative_humidity_2m_min",
                               "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min"]
            if mode is ForecastMode.FORECAST:
                params["forecast_days"] = time
            else: #past
                params["forecast_days"] = 1
                params["past_days"] = time
        else:  # hourly
            params["hourly"] = ["temperature_2m", "weather_code", "apparent_temperature", "relative_humidity_2m", "snowfall", "showers", "rain", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "wind_speed_10m"]
            if mode is ForecastMode.FORECAST:
                params["forecast_days"] = math.ceil(time / 24)
            else: #past
                params["forecast_days"] = 1
                params["past_days"] = math.ceil(time / 24)

        return params

    def _handle_response(self, response, params: dict) -> DataFrame:
        if isinstance(response, list):
            response = response[0]

        if "daily" in params:
            weather_data = self._daily_data_handling(response=response, params=params)
        elif "hourly" in params:
            weather_data = self._hourly_data_handling(response=response, params=params)
        else:  # current
            weather_data = self._current_data_handling(response=response, params=params)
        return self._dictionary_to_dataframe(weather_data=weather_data)

    @staticmethod
    def _dictionary_to_dataframe(weather_data: list) -> DataFrame:
        data = [asdict(weather) for weather in weather_data]
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        df.dropna(how='all',axis=1,inplace=True)
        df.to_csv(r"D:\personal\df.csv")
        return df

    @staticmethod
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
        for i in range(len(timestamps)):
            # Get values for current hour
            (
                temperature_2m, weather_code, apparent_temperature, relative_humidity_2m, snowfall,
                 showers, rain, cloud_cover, cloud_cover_low, cloud_cover_mid, cloud_cover_high,
                 visibility, wind_speed_10m
            ) = (var[i] for var in variables)

            # Create WeatherData instance
            weather_data = WeatherData(
                timestamp=timestamps[i],
                temperature_2m=temperature_2m,
                weather_code=weather_code,
                apparent_temperature_2m=apparent_temperature,
                rain=rain,
                rain_sum=rain,
                shower=showers,
                snowfall=snowfall,
                wind_speed_10m=wind_speed_10m,
                visibility=visibility,
                cloud_cover=cloud_cover,
                cloud_cover_max=cloud_cover_high,
                cloud_cover_min=cloud_cover_low,
                cloud_cover_mean=cloud_cover_mid,
                relative_humidity_2m=relative_humidity_2m
            )
            weather_data_list.append(weather_data)

        return weather_data_list

    @staticmethod
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
        for i in range(len(timestamps)):
            (
                temperature_2m_max, temperature_2m_min, weather_code, apparent_temperature_2m_max,
                apparent_temperature_2m_min, apparent_temperature_2m_mean, temperature_2m_mean, rain_sum, shower_sum,
                snowfall_sum, wind_speed_10m_max, wind_direction_10m_dominant, visibility_mean, visibility_min,
                visibility_max, wind_speed_10m_mean, wind_speed_10m_min, wind_gusts_10m_min, wind_gusts_10m_max,
                wind_gusts_10m_mean, relative_humidity_2m_min, relative_humidity_2m_max, relative_humidity_2m_mean,
                cloud_cover_mean, cloud_cover_max, cloud_cover_min
            ) = (var[i] for var in variables)

            weather_data = WeatherData(
                timestamp=timestamps[i],
                temperature_2m_max=temperature_2m_max,
                temperature_2m_min=temperature_2m_min,
                weather_code=weather_code,
                apparent_temperature_max=apparent_temperature_2m_max,
                apparent_temperature_min=apparent_temperature_2m_min,
                apparent_temperature_mean=apparent_temperature_2m_mean,
                temperature_2m_mean=temperature_2m_mean,
                rain_sum=rain_sum,
                showers_sum=shower_sum,
                snowfall_sum=snowfall_sum,
                wind_speed_10m_max=wind_speed_10m_max,
                wind_direction_10m_dominant=wind_direction_10m_dominant,
                visibility_mean=visibility_mean,
                visibility_min=visibility_min,
                visibility_max=visibility_max,
                wind_speed_10m_mean=wind_speed_10m_mean,
                wind_speed_10m_min=wind_speed_10m_min,
                wind_gust_10m_min=wind_gusts_10m_min,
                wind_gust_10m_max=wind_gusts_10m_max,
                wind_gust_10m_mean=wind_gusts_10m_mean,
                relative_humidity_min=relative_humidity_2m_min,
                relative_humidity_max=relative_humidity_2m_max,
                relative_humidity_mean=relative_humidity_2m_mean,
                cloud_cover_mean=cloud_cover_mean,
                cloud_cover_max=cloud_cover_max,
                cloud_cover_min=cloud_cover_min
            )
            weather_data_list.append(weather_data)

        return weather_data_list

    @staticmethod
    def _current_data_handling(response, params: dict) -> list[WeatherData]: #TODO broken?
        current = response.Current()

        # Extract all hourly variables in order
        variables = []
        for i in range(len(params["current"])):
            var = current.Variables(i).ValuesAsNumpy()
            variables.append(var)

        weather_data_list = []
        # Get values for current hour
        (
            temperature_2m, apparent_temperature, relative_humidity_2m,
            snowfall, showers, rain,
            weather_code, wind_speed_10m, wind_direction_10m, wind_gusts_10m
        ) = (var[0] for var in variables)
        # Create WeatherData instance
        weather_data = WeatherData(
            timestamp=datetime.fromtimestamp(current.Time(), tz=timezone.utc),
            temperature_2m=temperature_2m,
            apparent_temperature_2m=apparent_temperature,
            relative_humidity_2m=relative_humidity_2m,
            snowfall=snowfall,
            shower=showers,
            rain=rain,
            weather_code=weather_code,
            wind_speed_10m=wind_speed_10m,
            wind_direction_10m_dominant=wind_direction_10m,
            wind_gust_10m=wind_gusts_10m
        )
        weather_data_list.append(weather_data)

        return weather_data_list
