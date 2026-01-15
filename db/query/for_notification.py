async def db_for_notification(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT id, user_tg_id, code_list
                        FROM parserbot.users
                        WHERE subscription = 'YES'"""
        )

        return rows


async def db_identi_sub(pool, user_tg_id):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT subscription
            FROM parserbot.users
            WHERE user_tg_id = $1""",
            user_tg_id,
        )
        return row


async def db_upp_sub(pool, flag, user_tg_id):
    async with pool.acquire() as conn:
        print("Запуск db_upp_sub: Этап 1")
        result = await conn.fetchrow(
            """UPDATE parserbot.users 
                SET subscription = $1
                WHERE user_tg_id = $2
                RETURNING id, code_list""",
            flag,
            user_tg_id,
        )

        if flag == "YES":
            print("Запуск db_upp_sub: Этап 2 [YES]")
            rates = await conn.fetch(
                """SELECT DISTINCT ON (code) code, sell_rate, buy_rate
                    FROM parserbot.exchange_rate 
                    WHERE code = ANY($1)
                    ORDER BY code, created_at DESC""",
                result["code_list"],
            )

            print("Запуск db_upp_sub: Этап 3 [YES]")
            await conn.executemany(
                """INSERT INTO parserbot.user_subscription_rate
                    (user_id, code, sell_rate, buy_rate)
                    VALUES($1, $2, $3, $4)""",
                [
                    (result["id"], i["code"], i["sell_rate"], i["buy_rate"])
                    for i in rates
                ],
            )
            return

        elif flag == "NO":
            print("Запуск db_upp_sub: Этап 3 [NO]")
            # user_id = str(result["id"])
            await conn.execute(
                """DELETE FROM parserbot.user_subscription_rate
                    WHERE user_id = $1""",
                result["id"],
            )
            return
        return


# Отправить уведомление с измененной валютой, пользователю который подписан.
# Мы уже имеем список с подписанными пользователями - из тг_айди и code_list
# Идем циклом по этому списку.
# вытаскиваем текщий курс и курс от подписки
# сравниваем их
