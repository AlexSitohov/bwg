from app.core.config import db_config


import asyncpg


async def get_pool():
    if not hasattr(get_pool, "pool"):
        get_pool.pool = await asyncpg.create_pool(
            user=db_config.username,
            password=db_config.password,
            host=db_config.host,
            port=db_config.port,
            database=db_config.dbname,
            min_size=db_config.pool_size,
            max_size=db_config.pool_size,
        )
    yield get_pool.pool
