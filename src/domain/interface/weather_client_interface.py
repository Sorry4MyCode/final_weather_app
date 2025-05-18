from abc import abstractmethod, ABC

from pandas import DataFrame

from src.domain.models.location import Location


class WeatherClientInterface(ABC):
    @abstractmethod
    def get_weather(self, location: Location, time_interval: str, duration: int) -> DataFrame:
        pass

    @abstractmethod
    def _build_parameter(self, location: Location, time_interval: str, duration: int) -> dict:
        pass

    @abstractmethod
    def _handle_response(self, response: dict, params: dict) -> dict:
        pass
