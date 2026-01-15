from aiogram import Router, types, F
from db.query.user_Currency import db_user_Currency
from db.query.user_Currency_add import db_user_Currency_add
from db.query.user_Currency_del import db_user_Currency_del
from keyboards.inline.inline import kb_setting

router = Router()


@router.callback_query(F.data.startswith("currency:"))
async def select_currency_USD(call: types.CallbackQuery):
    pool = call.bot.pool
    currency = call.data.split(":")[1]
    f = call.from_user
    print(currency)
    # Получаем текущий саписок валют пользователя
    r = await db_user_Currency(pool, f.id)
    code_list = r[0][0]
    print(code_list)
    # Проверяем есть ли он в списке, да - запрос в бд, на удаление \ нет - запрос в бд на добавление
    if currency in code_list:
        await db_user_Currency_del(pool, currency, f.id)
        print("if currency in code_list: - OK")
        r1 = await db_user_Currency(pool, f.id)
        code_list1 = r1[0][0]

        kb = kb_setting(code_list1)
        print("kb = kb_setting(code_list) - ok")
        await call.message.edit_reply_markup(reply_markup=kb)
        await call.answer()
        return
    # Изменить текущую кнопку и вернуть клаву пользователю.
    elif currency not in code_list:
        await db_user_Currency_add(pool, currency, f.id)
        print("if currency in code_list: - NOT OK")
        r2 = await db_user_Currency(pool, f.id)
        code_list2 = r2[0][0]

        kb = kb_setting(code_list2)
        print(" kb = kb_setting(code_list) - ok")
        await call.message.edit_reply_markup(reply_markup=kb)
        await call.answer()
        return
    else:
        pass
    await call.answer()
    return
