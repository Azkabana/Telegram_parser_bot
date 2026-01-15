from aiogram import Router, types, F
from db.query.user_Currency import db_user_Currency
from keyboards.inline.inline import kb_setting, kb_menu
from db.query.for_notification import db_identi_sub, db_upp_sub


router = Router()


@router.callback_query(F.data.startswith("StartMenu"))
async def menu(call: types.CallbackQuery):
    pool = call.bot.pool
    f = call.from_user
    row = await db_identi_sub(pool, f.id)

    await call.message.edit_text(
        text="Стартовое меню", reply_markup=kb_menu(row["subscription"])
    )
    await call.answer()
    return


@router.callback_query(F.data.startswith("settings"))
async def setting(call: types.CallbackQuery):
    pool = call.bot.pool
    f = call.from_user
    r = await db_user_Currency(pool, f.id)
    code_list = r[0][0]
    await call.message.edit_text(
        text="Выберите интересующие вас валюты", reply_markup=kb_setting(code_list)
    )
    await call.answer()
    return


@router.callback_query(F.data.startswith("noti_sub"))
async def notification(call: types.CallbackQuery):
    pool = call.bot.pool
    f = call.from_user
    row = await db_identi_sub(pool, f.id)
    print(row["subscription"])

    if row["subscription"] == "NO":
        await call.message.edit_reply_markup(reply_markup=kb_menu("YES"))
        await db_upp_sub(
            pool,
            "YES",
            f.id,
        )

        call.answer()
        return

    else:
        await call.message.edit_reply_markup(reply_markup=kb_menu("NO"))
        await db_upp_sub(pool, "NO", f.id)

        call.answer()
        return
