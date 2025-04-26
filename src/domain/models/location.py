from dataclasses import dataclass


@dataclass
class Coordinates:
    latitude: float
    longitude: float


@dataclass
class Location:
    country: str
    city: str
    postal_code: str
    coordinates: Coordinates = None
