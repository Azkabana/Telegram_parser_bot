import asyncio
from aiogram import Bot
from db.query.for_notification import db_for_notification
from db.query.current_rate import db_current_rate
from db.query.sub_rate import db_sub_rate


async def notification(pool, bot: Bot):
    print("Запуск [notification]")
    while True:
        row = await db_for_notification(pool)
        if row is None:
            print("Нет подписок")
            await asyncio.sleep(60)

        else:
            for i in row:
                list1 = []
                sub_rate = await db_sub_rate(pool, int(i["id"]))  # курс подписки
                for j in sub_rate:
                    list1.append(j["code"])
                dict_OldRate = {r["code"]: r for r in sub_rate}

                current_rate = await db_current_rate(pool, list1)  # текущий курс
                dict_NewRate = {r["code"]: r for r in current_rate}
                text = ""
                for j in list1:
                    old = dict_OldRate[j]["sell_rate"]
                    new = dict_NewRate[j]["sell_rate"]
                    threshold = old / 1000

                    if abs(old - new) >= threshold:
                        # print(abs(old - new))
                        text += f"{j} ▲ +{abs(old - new)}₸\n"
                        """await bot.send_message(
                            chat_id=i["user_tg_id"],
                            text=f"Курс [{j}] увеличился на {abs(old - new)}₸ !")"""

                    elif old - new <= (threshold * (-1)):
                        text += f"{j} ▼ -{abs(old - new)}₸\n"
                        """await bot.send_message(
                            chat_id=i["user_tg_id"],
                            text=f"Курс [{j}] уменьшился на {abs(old - new)}₸ !")"""

                await bot.send_message(chat_id=i["user_tg_id"], text=text)

            await asyncio.sleep(60)
