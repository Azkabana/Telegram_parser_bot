# Заполняем валюты
async def db_reg_currency(pool, list1):
    async with pool.acquire() as conn:
        query = """INSERT INTO parserbot.currency (code, name)
                VALUES ($1, $2)
                ON CONFLICT (code) DO NOTHING"""

        await conn.executemany(query, list1)
