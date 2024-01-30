from app.daos.exchange_rate_dao import ExchangeRetaDAO

from app.repositories.exchange_rate import ExchangeRetaRepository


def provide_exchange_rate_repository_stub():
    raise NotImplementedError


def provide_exchange_rate_repository(auction_dao: ExchangeRetaDAO) -> ExchangeRetaRepository:
    return ExchangeRetaRepository(auction_dao)
