from app.dblayer.enums import CoursePair
from asyncpg import Pool


class ExchangeRetaDAO:

    async def find_all(self, pool: Pool, param: CoursePair | None):
        query = """
                    SELECT er.id, er.currency_pair_name, er.price, er.created_at
                    FROM exchange_rates er
                    JOIN (
                        SELECT currency_pair_name, MAX(created_at) AS latest_created_at
                        FROM exchange_rates
                        GROUP BY currency_pair_name
                    ) AS subquery
                    ON er.currency_pair_name = subquery.currency_pair_name
                    AND er.created_at = subquery.latest_created_at
                    """

        if param is not None:
            query += " WHERE er.currency_pair_name = $1"

        if param is not None:
            result = await pool.fetch(query, param)
        else:
            result = await pool.fetch(query)

        results_dict = [dict(record) for record in result]

        return results_dict
