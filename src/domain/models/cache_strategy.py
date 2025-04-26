import requests_cache
from retry_requests import retry

from src.config.settings import expiration_cache, backoff_factor_cache, retries_cache, cache_name


class CacheStrategy:
    def __init__(self, name_cache: str = cache_name, expire_after: int = expiration_cache, retries: int = retries_cache,
                 backoff_factor: float = backoff_factor_cache):
        cache_session = requests_cache.CachedSession(cache_name=name_cache, expire_after=expire_after)
        self.retry_session = retry(session=cache_session, retries=retries, backoff_factor=backoff_factor)
