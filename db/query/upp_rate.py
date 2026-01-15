async def db_upp_rate(pool, records):  # заполняем курс валют
    async with pool.acquire() as conn:
        await conn.copy_records_to_table(
            table_name="exchange_rate",
            schema_name="parserbot",
            records=records,
            columns=("code", "sell_rate", "buy_rate"),
        )
