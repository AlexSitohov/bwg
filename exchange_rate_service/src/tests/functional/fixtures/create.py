from random import choice

from asyncpg import Pool

from tests.functional.test_handlers.test_data import currency_pair_names

import pytest_asyncio


@pytest_asyncio.fixture()
async def create_exchange_rate_fixture(provide_pool: Pool, migrations_fixture):
    async with provide_pool.acquire() as connection:
        return await connection.fetchrow(
            """
            INSERT INTO exchange_rates (currency_pair_name, price)
            VALUES ($1, $2)
            RETURNING id, currency_pair_name, price
            """,
            choice(currency_pair_names),
            9999.99,
        )


@pytest_asyncio.fixture()
async def create_multiple_exchange_rates_fixture(
    provide_pool: Pool, migrations_fixture
):
    async with provide_pool.acquire() as connection:
        values = tuple((name, 9999.99) for name in currency_pair_names)
        query = """
            INSERT INTO exchange_rates (currency_pair_name, price)
            VALUES ($1, $2)
            """
        await connection.executemany(query, values)
