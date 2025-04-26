from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location


class Validation:
    @staticmethod
    def validate_location(location: Location) -> bool:
        if location.coordinates is None:
            raise ValueError(f"Location not found. Please verify the details:\n{location}")
        return True

    @staticmethod
    def validate_time_interval(time_interval: str, mode: ForecastMode) -> bool:
        if time_interval not in mode.time_interval:
            raise ValueError(f"Invalid time interval for {mode}. Please choose from {mode.time_interval}")
        return True

    @staticmethod
    def validate_response(response) -> bool:
        if response.status_code != 200:
            raise ValueError(f"Invalid response from OpenMeteo: {response.status_code}")
        return True
