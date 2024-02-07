import json
import logging
from functools import wraps
from uuid import UUID
from datetime import datetime
from redis.exceptions import ConnectionError


from app.dblayer.redis.providers import redis_cache

logger = logging.getLogger(__name__)


def custom_serializer(obj):
    if isinstance(obj, (UUID, datetime)):
        return str(obj)
    raise TypeError


def cache_response(hash_name: str, expiration_time: int):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{hash_name}:{args}:{kwargs}"
            try:
                cached_value = await redis_cache.redis.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)

                result = await func(*args, **kwargs)

                await redis_cache.redis.set(
                    cache_key,
                    json.dumps(result, default=custom_serializer),
                    ex=expiration_time,
                )
                return result
            except ConnectionError as e:
                logging.exception(f"Не удается подключиться к Redis {e}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator
