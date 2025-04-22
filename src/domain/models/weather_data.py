from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherData:
    weather_code: str | None

    temperature: float | None
    apparent_temperature: float | None
    maximum_temperature: float | None
    minimum_temperature: float | None

    rainfall: float | None
    rainfall_unit: str | None
    sum_rainfall: float | None

    snowfall: float | None
    snowfall_unit: str | None
    sum_snowfall: float | None

    wind_speed: float | None
    wind_direction: str | None

    visibility: float | None

    cloudiness: float | None

    timestamp: datetime