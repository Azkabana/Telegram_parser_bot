import requests
from bs4 import BeautifulSoup
import re
import asyncio
from db.query.reg_currency import db_reg_currency
from db.query.upp_rate import db_upp_rate
from decimal import Decimal


# Парсер курса валют
async def web_request():
    url = "https://www.bcc.kz/en/personal/currency-rates/?utm_source=chatgpt.com#fx-2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")  # вместо lxml - можно html.parser

    elements = soup.find_all("div", class_=re.compile("text-dark"))

    dict_valute = {}
    for i in elements:
        box_valute = i.find_all("div", class_=re.compile("py-3.5"))

        for j in box_valute:
            div_valute_name_en = j.find_all("div", class_=re.compile("text-lg"))
            div_values_right = j.find_all("div", class_=re.compile("text-right"))
            currency_name = j.find(
                "div", class_=re.compile("text-neutral-600")
            ).get_text(strip=True)

            for jj in div_valute_name_en:
                a = jj.text.strip()
                dict_valute[a] = None

            list_triple = []
            list_triple.append(currency_name)
            for jj in div_values_right:
                b = jj.text.strip()
                b1 = b.replace(" ", "")
                list_triple.append(b1)
            dict_valute[a] = list_triple

    return dict_valute


# добавления всех валют в бд 1 раз
async def once_request(pool):
    dict1 = await web_request()
    list1 = []
    for key, (key_name) in dict1.items():
        list1.append((key, key_name[0]))
    await db_reg_currency(pool, list1)
    print("Заполнение и проверки валют [once_request]: True")


# Бесконечный цикл с ожиданием в 1 минуту - сохраняем текущий курс в дб курса
async def webrequest_seveindb(pool):
    while True:
        dict1 = await web_request()
        records = [
            (currency, Decimal(values[1]), Decimal(values[2]))
            for currency, values in dict1.items()
        ]
        await db_upp_rate(pool, records)
        print("Заполнение курса [db_upp_rate]: True")
        await asyncio.sleep(60)
