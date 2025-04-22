from enum import Enum

class ForecastMode(str, Enum):
    CURRENT = "current"
    PAST = "past"
    FORECAST = "forecast"

    @classmethod
    def get_time_unit(cls, mode: "ForecastMode") -> str:
        '''
        return default time unit for mode
        '''