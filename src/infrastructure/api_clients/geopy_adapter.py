# noinspection PyUnresolvedReferences
from geopy_adapter.geocoders import Nominatim
from src.config.settings import *
from src.domain.models.location import Coordinates, Location

class GeoLocationClient:
    def __init__(self):
        self.geo_client = Nominatim(agent_name)

    def get_coordinates(self, location: Location) -> Coordinates:
        address_parts = [
            f"Country: {location.country}",
            f"Postal Code: {location.postal_code}",
            f"City: {location.city}"
        ]
        address = ", ".join(address_parts)
        response = self.geo_client.geocode(address)

        return Coordinates(latitude=response.latitude, longitude=response.longitude)