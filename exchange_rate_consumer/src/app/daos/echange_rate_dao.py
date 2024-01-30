from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import insert

from app.dblayer.tables import ExchangeRates


class ExchangeRateDAO:
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def create_exchange_rate(self, data: tuple):
        async with self.session() as session:
            await session.execute(
                insert(ExchangeRates)
                .values(currency_pair_name=data[0], price=float(data[1]))
            )
            await session.commit()
