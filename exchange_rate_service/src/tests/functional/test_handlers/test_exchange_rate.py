import pytest

from tests.functional.test_handlers.test_data import currency_pair_names


@pytest.mark.asyncio
async def test_find_one(provide_test_client, create_exchange_rate_fixture):
    exchange_rate_data = create_exchange_rate_fixture
    response = await provide_test_client.get(
        url="/exchange_rate/api/v1/courses",
        params={"course_rate_pare": exchange_rate_data["currency_pair_name"]},
    )
    data = response.json()[0]
    assert response.status_code == 200
    assert data["id"] == str(exchange_rate_data["id"])
    assert data["currency_pair_name"] == exchange_rate_data["currency_pair_name"]
    assert data["currency_pair_name"] in currency_pair_names
    assert data["price"] == exchange_rate_data["price"]


@pytest.mark.asyncio
async def test_find_all(provide_test_client, create_multiple_exchange_rates_fixture):
    response = await provide_test_client.get(url="/exchange_rate/api/v1/courses")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(currency_pair_names) == 8
