async def db_user_Currency_del(pool, cur, user_tg_id):
    async with pool.acquire() as conn:
        print("db_user_Currency_del - запускаю")
        await conn.execute(
            """UPDATE parserbot.users
                           SET code_list = array_remove(code_list, $1)
                           WHERE user_tg_id = $2""",
            cur,
            user_tg_id,
        )
        print("db_user_Currency_del - завершение")
    return
