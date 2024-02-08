import logging

from redis.asyncio import ConnectionPool, Redis


class RedisCache:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis = None
        self.logger = logging.getLogger(__name__)

    def setup(self):
        pool = ConnectionPool.from_url(self.redis_url)
        self.redis = Redis(connection_pool=pool, encoding="utf-8")

    async def get(self, key):
        try:
            data = await self.redis.get(key)

            return data.decode("utf-8") if data else None
        except Exception as e:
            self.logger.exception(f"Error getting key {key} from cache: {str(e)}")
            return None

    async def set(self, key, value, ttl=None):
        try:
            if ttl is not None:
                return await self.redis.setex(key, ttl, value.encode("utf-8"))
            else:
                return await self.redis.set(key, value.encode("utf-8"))
        except Exception as e:
            self.logger.exception(f"Error setting key {key} in cache: {str(e)}")
            return False
