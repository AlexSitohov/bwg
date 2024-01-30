from sqlalchemy.ext.asyncio import async_sessionmaker

from app.daos.exchange_rate_dao import ExchangeRetaDAO


def provide_exchange_rate_dao(session: async_sessionmaker) -> ExchangeRetaDAO:
    return ExchangeRetaDAO(session)
