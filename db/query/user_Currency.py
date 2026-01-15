async def db_user_Currency(pool, user_tg_id):
    async with pool.acquire() as conn:
        print("db_user_Currency - запускаю")
        rows = await conn.fetch(
            """SELECT code_list
                FROM parserbot.users
                WHERE user_tg_id = $1""",
            user_tg_id,
        )
        print("db_user_Currency - завершение")
        return rows
