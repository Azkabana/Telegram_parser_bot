from aiogram.utils.keyboard import InlineKeyboardBuilder


def kb_menu(sub):
    kb = InlineKeyboardBuilder()
    kb.button(text=f"Текущий курс", callback_data="curent_rate")
    kb.button(text=f"История изменений", callback_data="change_history")
    if sub == "YES":
        kb.button(text=f"Подписка на уведомление ✅", callback_data="noti_sub")
    else:
        kb.button(text=f"Подписка на уведомление ", callback_data="noti_sub")
    kb.button(text=f"Настройки", callback_data="settings")
    kb.adjust(2)
    return kb.as_markup()


def kb_change_history():
    kb = InlineKeyboardBuilder()
    kb.button(text=f"Подробнее", callback_data="MoreInfo")
    kb.button(text=f"Главное меню", callback_data="StartMenu")
    kb.adjust(2)
    return kb.as_markup()


def kb_setting(code_list):
    kb = InlineKeyboardBuilder()
    CURRENCIES = [
        "USD",
        "EUR",
        "RUB",
        "GBP",
        "GOLD",
        "CNY",
        "AED",
        "SILVER",
        "CAD",
        "CHF",
        "TRY",
        "UZS",
        "JPY",
    ]

    for i in CURRENCIES:
        data = f"currency:{i}"
        if i in code_list:
            kb.button(text=f"{i} ✅", callback_data=data)
        else:
            kb.button(text=i, callback_data=data)
    kb.button(text=f"Главное меню", callback_data="StartMenu")
    kb.adjust(2)
    return kb.as_markup()


def kb_currency_menu():
    kb = InlineKeyboardBuilder()
    data = f"mqin10:"
    data1 = f"hour1:"
    kb.button(text=f"10 минут", callback_data=data)
    kb.button(text=f"1 Час", callback_data=data1)
    kb.adjust(2)
    return kb.as_markup()
