async def db_current_rate(pool, currency_list: list):
    async with pool.acquire() as conn:
        list_rows = []
        for cur in currency_list:
            row = await conn.fetchrow(
                """SELECT c.code, c.name, e.sell_rate, e.buy_rate, e.created_at 
                    FROM parserbot.exchange_rate e
                    JOIN parserbot.currency c
                    ON c.code = e.code
                    WHERE c.code = $1
                    ORDER BY e.created_at DESC
                    LIMIT 1""",
                cur,
            )
            list_rows.append(row)
        return list_rows
