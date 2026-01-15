from dotenv import load_dotenv
import os
import asyncpg

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")


# ceated_pool
async def create_pool():
    return await asyncpg.create_pool(
        user=USER, password=PASSWORD, database=DATABASE, host=HOST
    )


# db_table - created
async def setup_table(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS parserbot.users(
            id SERIAL PRIMARY KEY,
            user_tg_id BIGINT UNIQUE,
            user_fname TEXT,
            code_list TEXT[] DEFAULT '{}',
            subscription TEXT DEFAULT 'NO',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )
        print("Проверка таблицы [users]: True")

        await conn.execute(
            """CREATE TABLE IF NOT EXISTS parserbot.currency(
                           id SERIAL PRIMARY KEY,
                           code VARCHAR UNIQUE,
                           name VARCHAR,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )
        print("Проверка таблицы [currency]: True")

        await conn.execute(
            """CREATE TABLE IF NOT EXISTS parserbot.exchange_rate(
                           id SERIAL PRIMARY KEY,
                           code VARCHAR REFERENCES parserbot.currency(code), 
                           sell_rate DECIMAL,
                           buy_rate DECIMAL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )
        print("Проверка таблицы [exchange_rate]: True")

        await conn.execute(
            """CREATE TABLE IF NOT EXISTS parserbot.user_subscription_rate(
                            id SERIAL PRIMARY KEY,
                            user_id INT REFERENCES parserbot.users(id) ON DELETE CASCADE,
                            code VARCHAR REFERENCES parserbot.currency(code),
                            sell_rate DECIMAL,
                            buy_rate DECIMAL,
                            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )
        print("Проверка таблицы [user_subscription_rate]: True")


# code - это сама валюта - EUR | USD | RUB
# name - наименование самой валюты - Евро | Доллар | Рубль
