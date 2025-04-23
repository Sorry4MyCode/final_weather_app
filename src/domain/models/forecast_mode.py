from enum import Enum

class ForecastMode(str, Enum):
    CURRENT = ("current", ["current"])
    PAST = ("past", ["daily", "hourly"])
    FORECAST = ("forecast", ["daily", "hourly"])

    def __init__(self, mode, time_interval):
        self.mode = mode
        self.time_interval = time_interval
