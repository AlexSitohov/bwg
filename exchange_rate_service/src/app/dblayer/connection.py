from app.core.config import db_config


from asyncpg import create_pool, Pool
from typing import AsyncGenerator


async def get_pool() -> AsyncGenerator[Pool, None]:
    if not hasattr(get_pool, "pool"):
        get_pool.pool = await create_pool(
            user=db_config.username,
            password=db_config.password,
            host=db_config.host,
            port=db_config.port,
            database=db_config.dbname,
            min_size=db_config.pool_size,
            max_size=db_config.pool_size,
        )
    yield get_pool.pool
