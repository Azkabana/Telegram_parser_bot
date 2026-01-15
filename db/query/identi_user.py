async def db_identi_user(pool, user_tg_id):
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            """SELECT EXISTS(
            SELECT 1
            FROM parserbot.users
            WHERE user_tg_id = $1)""",
            user_tg_id,
        )
        return result
