from sqlalchemy import func, select, and_

from app.db.enums import CoursePair
from app.db.tables import ExchangeRates


class ExchangeRetaDAO:
    def __init__(self, session):
        self.session = session

    async def find_all(self, param: CoursePair | None):
        async with self.session() as session:
            subquery = (
                select(
                    ExchangeRates.currency_pair_name,
                    func.max(ExchangeRates.created_at).label("latest_created_at")
                )
                .group_by(ExchangeRates.currency_pair_name)
                .subquery()
            )

            latest_rates = (
                select(
                    ExchangeRates.id,
                    ExchangeRates.currency_pair_name,
                    ExchangeRates.price,
                    ExchangeRates.created_at
                )
                .join(subquery, and_(
                    ExchangeRates.currency_pair_name == subquery.c.currency_pair_name,
                    ExchangeRates.created_at == subquery.c.latest_created_at
                ))
            )

            if param is not None:
                latest_rates = latest_rates.filter(ExchangeRates.currency_pair_name == param)

            return (await session.execute(latest_rates)).all()
