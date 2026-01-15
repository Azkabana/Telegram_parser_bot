from aiogram import Router, F, types
from db.query.rate_30min import db_rate_30min
from db.query.user_Currency import db_user_Currency
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.inline.inline import kb_change_history, kb_menu
from db.query.for_notification import db_identi_sub


router = Router()


class change_historyFSM(StatesGroup):
    One = State()


@router.callback_query(F.data.startswith("change_history"))
async def change_history(call: types.CallbackQuery, state: FSMContext):
    pool = call.bot.pool
    f = call.from_user

    cur_list = await db_user_Currency(pool, f.id)
    cur_list = cur_list[0][0]

    result_list = await db_rate_30min(pool, cur_list)
    await state.set_state(change_historyFSM.One)
    await state.update_data(result_list=result_list)

    text_sell = ""

    for i in result_list:
        change_sell = i[0]["sell_rate"] - i[1]["sell_rate"]
        if change_sell < 0:
            text_ChangeSell = f"▼ {change_sell}"
        elif change_sell > 0:
            text_ChangeSell = f"▲ +{change_sell}"
        else:
            text_ChangeSell = f"■ {change_sell}"

        text_sell += f"{i[0]["code"]}: {i[0]["sell_rate"]}₸ {text_ChangeSell}\n"

    await call.message.delete()
    await call.bot.send_message(
        chat_id=f.id, text=text_sell, reply_markup=kb_change_history()
    )

    await call.answer()
    return


@router.callback_query(F.data.startswith("MoreInfo"))
async def MoreInfo(call: types.CallbackQuery, state: FSMContext):
    pool = call.bot.pool
    f = call.from_user
    data = await state.get_data()
    result_list = data.get("result_list")

    text = f""
    for i in result_list:
        change_sell = i[0]["sell_rate"] - i[1]["sell_rate"]
        if change_sell < 0:
            text_ChangeSell = f"▼ {change_sell}"
        elif change_sell > 0:
            text_ChangeSell = f"▲ +{change_sell}"
        else:
            text_ChangeSell = f"■ {change_sell}"

        change_buy = i[0]["buy_rate"] - i[1]["buy_rate"]
        if change_buy < 0:
            text_ChangeBuy = f"▼ {change_sell}"
        elif change_buy > 0:
            text_ChangeBuy = f"▲ +{change_sell}"
        else:
            text_ChangeBuy = f"■ {change_sell}"

        time = i[0]["created_at"].strftime("%H:%M %d.%m.%Y")
        text += f"{i[0]["code"]} - {time}\n💰 Покупка: {i[0]["buy_rate"]}₸  {text_ChangeBuy}\n💸 Продажа: {i[0]["sell_rate"]}₸  {text_ChangeSell}\n"

    await call.message.edit_text(chst_id=f.id, text=text)

    identi_sub = await db_identi_sub(pool, f.id)
    await call.bot.send_message(
        chat_id=f.id,
        text="Стартовое меню",
        reply_markup=kb_menu(identi_sub["subscription"]),
    )

    await call.answer()
    return
