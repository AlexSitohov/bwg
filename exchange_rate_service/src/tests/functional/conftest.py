import os
import pathlib
from argparse import Namespace

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from app.dblayer.connection import provide_engine
from app.main import build_app

pytest_plugins = (
    "tests.functional.utils.fixtures.daos",
    "tests.functional.utils.fixtures.creators",
)


@pytest.fixture(scope="session")
def provide_postgres_container() -> PostgresContainer:
    postgres_container = PostgresContainer(
        "berupor/test-postgresql:latest",
        user=os.environ["POSTGRES_DB_LOGIN"],
        password=os.environ["POSTGRES_DB_PASSWORD"],
        port=os.environ["POSTGRES_DB_PORT"],
        dbname=os.environ["POSTGRES_DB_NAME"],
    )
    postgres_container.start()

    yield postgres_container

    postgres_container.stop()


pytest.fixture(scope="session")


def provide_engine_singleton(provide_postgres_container):
    engine = provide_engine(
        url=provide_postgres_container.get_connection_url(), echo=False, pool_size=5
    )
    yield engine

    engine.dispose()


@pytest.fixture(scope="session")
def provide_app(
    provide_engine_singleton,
):
    app = build_app(
        provide_engine_singleton,
    )
    yield app


@pytest.fixture(scope="session")
def provide_test_client(provide_app):
    client = TestClient(provide_app)

    yield client

    client.close()


@pytest.fixture(scope="session", autouse=True)
def migrate(provide_postgres_container):
    alembic_cfg = Config(cmd_opts=Namespace(x={"data=True"}))
    alembic_cfg.set_main_option(
        "script_location",
        str(pathlib.Path(__file__).parent.resolve().parent.parent / "app/alembic"),
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url", provide_postgres_container.get_connection_url()
    )
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(autouse=True)
def truncate_tables(
    provide_engine_singleton,
):
    yield

    with provide_engine_singleton.begin() as connection:
        tables = []
        for table in tables:
            connection.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
