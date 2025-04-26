from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    timestamp: datetime

    temperature_2m: float | None = None
    temperature_2m_mean: float | None = None
    temperature_2m_max: float | None = None
    temperature_2m_min: float | None = None

    weather_code: str | None = None

    apparent_temperature_2m: float | None = None
    apparent_temperature_max: float | None = None
    apparent_temperature_min: float | None = None
    apparent_temperature_mean: float | None = None

    rain: bool | None = None
    rain_sum: float | None = None
    shower: bool | None = None
    showers_sum: float | None = None
    snowfall: bool | None = None
    snowfall_sum: float | None = None

    wind_speed_10m: float | None = None
    wind_speed_10m_mean: float | None = None
    wind_speed_10m_max: float | None = None
    wind_speed_10m_min: float | None = None
    wind_direction_10m_dominant: float | None = None

    wind_gust_10m: float | None = None
    wind_gust_10m_mean: float | None = None
    wind_gust_10m_max: float | None = None
    wind_gust_10m_min: float | None = None

    visibility: float | None = None
    visibility_mean: float | None = None
    visibility_max: float | None = None
    visibility_min: float | None = None

    cloud_cover: float | None = None
    cloud_cover_mean: float | None = None
    cloud_cover_max: float | None = None
    cloud_cover_min: float | None = None

    relative_humidity_2m: float | None = None
    relative_humidity_mean: float | None = None
    relative_humidity_max: float | None = None
    relative_humidity_min: float | None = None
