from enum import Enum

class ForecastMode(str, Enum):
    CURRENT = ('current', ['current'])
    PAST = ('past', ['daily', 'hourly'])
    FORECAST = ('forecast', ['daily', 'hourly'])

    def __new__(cls, value, time_interval):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __init__(self, value, time_interval):
        self.time_interval = time_interval