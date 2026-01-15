from aiogram import Router, types, F
from db.query.user_Currency import db_user_Currency
from db.query.current_rate import db_current_rate
from keyboards.inline.inline import kb_menu
from db.query.for_notification import db_identi_sub


router = Router()


@router.callback_query(F.data.startswith("curent_rate"))
async def current_rate(call: types.CallbackQuery):
    # просто выдаем все курсы, которые есть по его code_list
    pool = call.bot.pool
    f = call.from_user
    cur_list = await db_user_Currency(pool, f.id)
    cur_list = cur_list[0][0]

    lists_current_rate = await db_current_rate(pool, cur_list)
    big_msg = ""
    for row in lists_current_rate:
        # print(row[0], row[1], row[2], row[3], row[4])
        time = f"🕒 Обновлено: {row[4].strftime('%d.%m.%Y %H:%M')}"
        text = f"{row[0]} - {row[1]}\n💸 Продажа: {row[2]}\n💰 Покупка: {row[3]}\n{time}\n\n"
        big_msg += text

    await call.message.delete()
    await call.bot.send_message(chat_id=f.id, text=big_msg)

    identi_sub = await db_identi_sub(pool, f.id)
    await call.bot.send_message(
        chat_id=f.id,
        text="Стартовое меню",
        reply_markup=kb_menu(identi_sub["subscription"]),
    )

    await call.answer()
    return
