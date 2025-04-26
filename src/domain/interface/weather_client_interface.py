from abc import abstractmethod, ABC

from pandas import DataFrame

from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location


class WeatherClientInterface(ABC):
    @abstractmethod
    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> DataFrame:
        pass

    @abstractmethod
    def _build_parameter(self, location: Location, mode: ForecastMode, time_interval: str, time: int) -> dict:
        pass

    @abstractmethod
    def _handle_response(self, response: dict, params: dict) -> dict:
        pass
