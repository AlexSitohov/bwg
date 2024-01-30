from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.engine import URL

from app.core.config import db_config


def construct_url(
        username: str, password: str, host: str, port: int, dbname: str
) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=username,
        password=password,
        host=host,
        port=port,
        database=dbname,
    )


def provide_engine(url: URL | str, echo: bool, pool_size: int) -> AsyncEngine:
    return create_async_engine(url=url, echo=echo, pool_size=pool_size, future=True)


def provide_session(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def configure_engine() -> AsyncEngine:
    db_connection_uri = construct_url(
        db_config.username,
        db_config.password,
        db_config.host,
        db_config.port,
        db_config.dbname,
    )
    engine = provide_engine(
        db_connection_uri,
        echo=db_config.echo,
        pool_size=db_config.pool_size,
    )
    return engine
