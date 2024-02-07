from app.dblayer.enums import CoursePair
from asyncpg import Pool


class ExchangeRetaDAO:
    @staticmethod
    async def find_all(pool: Pool, param: CoursePair | None):
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

    @staticmethod
    async def create_exchange_rate(pool: Pool, data: tuple[str, float]):
        await pool.execute(
            """
            INSERT INTO exchange_rates (currency_pair_name, price)
            VALUES ($1, $2)
            """,
            data[0],
            float(data[1]),
        )
