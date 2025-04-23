from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location
from src.infrastructure.api_clients.open_meteo_api import OpenMeteoClient


class Validation:
    def validate_location(self, location: Location):
        if location.coordinates is None:
            raise ValueError(f"Location not found. Please verify the details:\n{location}")
        return True

    def validate_time_interval(self, time_interval: str, mode: ForecastMode):
        if time_interval not in mode.time_interval:
            raise ValueError(f"Invalid time interval for {mode}. Please choose from {mode.time_interval}")
        return True

    def validate_response(self, response):
        if response.status_code != 200:
            raise ValueError(f"Invalid response from OpenMeteo: {response.status_code}")
        return True