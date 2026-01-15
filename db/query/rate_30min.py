async def db_rate_30min(pool, currency_list):
    async with pool.acquire() as conn:
        list_result = []
        for cur in currency_list:
            new_list = []
            new_rate = await conn.fetchrow(
                """SELECT code, sell_rate, buy_rate, created_at
                FROM parserbot.exchange_rate
                WHERE code = $1
                ORDER BY created_at DESC
                LIMIT 1""",
                cur,
            )
            new_list.append(new_rate)

            old_rate = await conn.fetchrow(
                """SELECT sell_rate, buy_rate, created_at
                FROM parserbot.exchange_rate
                WHERE code = $1
                AND created_at <= NOW() - INTERVAL '30 minutes'
                ORDER BY created_at DESC
                LIMIT 1""",
                cur,
            )
            new_list.append(old_rate)

            list_result.append(new_list)
        return list_result
