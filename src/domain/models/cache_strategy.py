import requests_cache

from src.config.settings import expiration_cache, backoff_factor_cache, retries_cache, cache_name


class CacheStrategy():
    def __init__(self, cache_name: str = cache_name, expire_after: int = expiration_cache, retries: int = retries_cache, backoff_factor: float = backoff_factor_cache):
        cache_session = requests_cache.CachedSession(cache_name=cache_name, expire_after=expire_after)
        self.session = retry(cache_session=cache_session, retries=retries, backoff_factor=backoff_factor)
