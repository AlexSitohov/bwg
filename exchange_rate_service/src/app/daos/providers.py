from app.daos.exchange_rate_dao import ExchangeRetaDAO


def provide_exchange_rate_dao() -> ExchangeRetaDAO:
    return ExchangeRetaDAO()
