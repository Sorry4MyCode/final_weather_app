import openmeteo_requests

from src.domain.models.cache_strategy import CacheStrategy


class OpenMeteoClient:
    def __init__(self, cache: CacheStrategy):
        self.client = openmeteo_requests.Client(session=cache.retry_session)

    def get_weather(self, url, params: dict):
        return self.client.weather_api(url, params)[0]