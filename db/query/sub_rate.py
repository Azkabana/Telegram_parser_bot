async def db_sub_rate(pool, user_id):
    async with pool.acquire() as conn:
        sub_rate = await conn.fetch(
            """SELECT code, sell_rate, buy_rate
                FROM parserbot.user_subscription_rate
                WHERE user_id = $1""",
            user_id,
        )
        return sub_rate
