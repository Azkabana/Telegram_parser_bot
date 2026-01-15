async def db_reg_user(pool, usertg_id, user_fname):  # заполняем курс валют
    async with pool.acquire() as conn:
        result = await conn.execute(
            """INSERT INTO parserbot.users (user_tg_id, user_fname)
                                VALUES ($1, $2)
                                ON CONFLICT (user_tg_id) DO NOTHING
                                RETURNING id""",
            usertg_id,
            user_fname,
        )
    return result
