import openmeteo_requests

from config.logging_config import debug_log
from domain.models.cache_strategy import CacheStrategy


class OpenMeteoClient:
    def __init__(self, cache: CacheStrategy):
        self.client = openmeteo_requests.Client(session=cache.retry_session)

    @debug_log
    def get_weather(self, url, params: dict):
        return self.client.weather_api(url, params)[0]
