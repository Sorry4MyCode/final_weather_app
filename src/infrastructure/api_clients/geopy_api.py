# noinspection PyUnresolvedReferences
from geopy.geocoders import Nominatim

from config.logging_config import debug_log
from config.settings import agent_name
from domain.models.location import Coordinates, Location


class GeoLocationClient:
    def __init__(self):
        self.geo_client = Nominatim(user_agent=agent_name)

    @debug_log
    def get_coordinates(self, location: Location) -> Coordinates:
        address_parts = [
            location.city,
            location.postal_code,
            location.country
        ]
        address = ", ".join(filter(None, address_parts))

        response = self.geo_client.geocode(address)

        if not response:
            raise ValueError(f"Location not found: {address}")

        return Coordinates(
            latitude=response.latitude,
            longitude=response.longitude
        )
