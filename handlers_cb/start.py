from aiogram import Router, types
from aiogram.filters import Command
from db.query.reg_user import db_reg_user
from db.query.identi_user import db_identi_user
from keyboards.inline.inline import kb_menu, kb_setting
from db.query.user_Currency import db_user_Currency
from db.query.for_notification import db_identi_sub

router = Router()


@router.message(Command("start"))
async def handler_start(msg: types.Message):
    f = msg.from_user
    pool = msg.bot.pool
    identi_sub = await db_identi_sub(pool, f.id)

    identi_user = await db_identi_user(pool, f.id)
    identi_user = identi_user[0]
    if identi_user == True:
        await msg.bot.send_message(
            chat_id=f.id,
            text="Стартовое меню",
            reply_markup=kb_menu(identi_sub["subscription"]),
        )
        print(f"Активирован [handler_start - с условвием if]")
        return
    else:
        await db_reg_user(pool, f.id, f.first_name)
        r = await db_user_Currency(pool, f.id)
        list_code = r[0][0]
        await msg.bot.send_message(
            chat_id=f.id,
            text=f"Выберите интересующие вас валюты",
            reply_markup=kb_setting(list_code),
        )
        print(f"Активирован [handler_start - с условием else]")
        return
