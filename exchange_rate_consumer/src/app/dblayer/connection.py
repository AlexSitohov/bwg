import asyncpg
from app.core.config import db_config


async def create_pool():
    pool = await asyncpg.create_pool(
        user=db_config.username,
        password=db_config.password,
        host=db_config.host,
        port=db_config.port,
        database=db_config.dbname,
        min_size=db_config.pool_size,
        max_size=db_config.pool_size,
    )
    return pool
