from asyncpg import Pool


class ExchangeRateDAO:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def create_exchange_rate(self, data: tuple):
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO exchange_rates (currency_pair_name, price)
                VALUES ($1, $2)
                """,
                data[0],
                float(data[1]),
            )
