from random import choice

import pytest
from asyncpg import Pool

from app.builder import Application
from tests.functional.test_handlers.test_data import currency_pair_names


@pytest.mark.asyncio
async def test_create_one(
    provide_app: Application, provide_pool: Pool, migrations_fixture
):
    create_exchange_rate_data = (choice(currency_pair_names), 9999.99)
    await provide_app.exchange_rate_dao.create_exchange_rate(
        provide_pool, create_exchange_rate_data
    )
    result = await provide_app.exchange_rate_dao.find_all(provide_pool, None)

    assert result[0]["currency_pair_name"] == create_exchange_rate_data[0]
    assert result[0]["price"] == create_exchange_rate_data[1]
