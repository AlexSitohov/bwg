from app.core.config import redis_config
from app.dblayer.redis.redis_cache import RedisCache


def get_redis_cache(redis_url: str) -> RedisCache:
    redis_cache = RedisCache(redis_url)
    redis_cache.setup()
    return redis_cache


redis_cache = get_redis_cache(redis_config.url)
