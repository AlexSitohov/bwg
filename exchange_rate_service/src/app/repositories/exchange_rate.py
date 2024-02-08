from asyncpg import Pool

from app.dblayer.enums import CoursePair


class ExchangeRetaRepository:
    def __init__(self, exchange_rate_dao):
        self.exchange_rate_dao = exchange_rate_dao

    async def find_all(self, pool: Pool, params: CoursePair):
        return await self.exchange_rate_dao.find_all(pool, params)
