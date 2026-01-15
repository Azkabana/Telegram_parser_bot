import asyncio
from bot.bot import dp, bot
from db.base import create_pool, setup_table
from parser.response import once_request, webrequest_seveindb
from handlers_cb.start import router as start
from handlers_cb.setting import router as setting
from handlers_cb.menu import router as menu
from handlers_cb.current_rate import router as current_rate
from handlers_cb.change_history import router as change_history
from notification.notification import notification

dp.include_router(change_history)
dp.include_router(current_rate)
dp.include_router(menu)
dp.include_router(setting)
dp.include_router(start)
# dp.include_router(seelct_currency)


# Это главный холл гильдии, это не цикл
async def main():
    print("Вечный цикл обработки обновлений: True")
    pool = await create_pool()
    bot.pool = pool
    await setup_table(pool)
    await once_request(pool)
    asyncio.create_task(webrequest_seveindb(pool))
    asyncio.create_task(notification(pool, bot))
    await dp.start_polling(bot)


# точка входа, запускает main(), только если он запущен руками, а не импортом, по сути не обязательноые строки.
if __name__ == "__main__":
    print('Условие [if __name__ == "__main__"]: True ')
    asyncio.run(main())
