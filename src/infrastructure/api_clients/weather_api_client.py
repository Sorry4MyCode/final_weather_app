from abc import abstractmethod, ABC

from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location
from src.domain.models.weather_data import WeatherData


class WeatherAPIClient(ABC):
    @abstractmethod
    def get_weather(self, location: Location, mode: ForecastMode, time_interval: str) -> list[WeatherData]:
        pass #TODO fabric logic