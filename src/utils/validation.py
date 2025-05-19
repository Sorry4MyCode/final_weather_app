from config.logging_config import debug_log
from domain.models.location import Location


class Validation:
    @staticmethod
    @debug_log
    def validate_location(location: Location) -> bool:
        if location.coordinates is None:
            raise ValueError(f"Location not found. Please verify the details:\n{location}")
        return True

    @staticmethod
    @debug_log
    def validate_response(response) -> bool:
        if response.status_code != 200:
            raise ValueError(f"Invalid response from OpenMeteo: {response.status_code}")
        return True
