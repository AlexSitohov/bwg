import os
import pathlib
from typing import AsyncIterator
from urllib.parse import urlparse

import pytest
import pytest_asyncio
from httpx import AsyncClient
from testcontainers.postgres import PostgresContainer
from asyncpg import create_pool
from testcontainers.redis import RedisContainer
from yoyo import read_migrations, get_backend

from app.core.config import db_config
from app.builder import Application
from app.dblayer.connection import get_pool


pytest_plugins = ("tests.functional.fixtures.create",)


@pytest.fixture(scope="session")
def provide_postgres_container() -> PostgresContainer:
    postgres_container = PostgresContainer(
        "postgres:alpine",
        user=os.environ["POSTGRES_DB_LOGIN"],
        password=os.environ["POSTGRES_DB_PASSWORD"],
        port=5432,
        dbname=os.environ["POSTGRES_DB_NAME"],
    )

    postgres_container.get_container_host_ip = lambda: "localhost"
    postgres_container.start()

    yield postgres_container

    postgres_container.stop()


@pytest.fixture(scope="session")
def provide_redis_container() -> RedisContainer:
    redis_container = RedisContainer(
        "redis:7.2.1",
        port_to_expose=6379,
        password=None,
    )
    redis_container.get_container_host_ip = lambda: "localhost"

    redis_container.start()

    yield redis_container

    redis_container.stop()


@pytest_asyncio.fixture()
async def provide_pool(provide_postgres_container):
    pool = await create_pool(
        user=db_config.username,
        password=db_config.password,
        host="localhost",
        port=provide_postgres_container.get_exposed_port(5432),
        database=db_config.dbname,
        min_size=db_config.pool_size,
        max_size=db_config.pool_size,
    )
    return pool


@pytest_asyncio.fixture()
async def override_get_pool(provide_postgres_container, provide_pool):
    async def _override_get_pool():
        return provide_pool

    yield _override_get_pool


@pytest_asyncio.fixture()
async def provide_app(override_get_pool):
    builder = Application()
    app: Application = builder.build_application()
    app.app.dependency_overrides[get_pool] = override_get_pool
    yield app


@pytest_asyncio.fixture()
async def migrations_fixture(provide_postgres_container):
    db_url = provide_postgres_container.get_connection_url()

    parsed_url = urlparse(db_url)
    username = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port
    database = parsed_url.path.strip("/")

    uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    backend = get_backend(uri)

    migrations = read_migrations(
        str(pathlib.Path(__file__).parent.resolve().parent / "app/migrations"),
    )
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    def rollback_migrations():
        with backend.lock():
            backend.rollback_migrations(backend.to_rollback(migrations))

    yield

    rollback_migrations()


@pytest_asyncio.fixture()
async def provide_test_client(provide_app) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        app=provide_app.app, base_url="http://localhost:8000"
    ) as client:
        yield client
