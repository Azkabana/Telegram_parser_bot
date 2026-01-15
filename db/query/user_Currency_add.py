async def db_user_Currency_add(pool, cur, user_tg_id):
    async with pool.acquire() as conn:
        print("db_user_Currency_add - запускаю")
        await conn.execute(
            """UPDATE parserbot.users
                           SET code_list = array_append(code_list, $1)
                           WHERE user_tg_id = $2 AND NOT($1 = ANY(code_list))""",
            cur,
            user_tg_id,
        )
        print("db_user_Currency_add - завершение")
    return
