# Credits: TeamUltroid - github.com/teamultroid
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from re import compile

from . import (
    Button,
    CallbackQuery,
    InlineQuery,
    calcc,
    check_owner,
    dgvar,
    doge,
    gvar,
    lan,
    sgvar,
)

c = [
    "AC",
    "C",
    "⫷",
    "%",
    "7",
    "8",
    "9",
    "+",
    "4",
    "5",
    "6",
    "-",
    "1",
    "2",
    "3",
    "x",
    "00",
    "0",
    ".",
    "÷",
]
dog = [Button.inline(f"{x}", data=f"calc{x}") for x in c]
lst = list(zip(dog[::4], dog[1::4], dog[2::4], dog[3::4]))
lst.append([Button.inline("=", data="calc=")])


@doge.tgbot.on(InlineQuery(pattern="calc"))
@check_owner
async def calc_(e):
    calc = e.builder.article("Calc", text=f"🧮 {lan('icalctext')} 🧮", buttons=lst)
    await e.answer([calc])


@doge.tgbot.on(CallbackQuery(data=compile(b"calc(.*)")))
@check_owner
async def calculator(e):
    x = (e.data_match.group(1)).decode()
    if x == "AC":
        dgvar("calc")
        await e.edit(
            f"🧮 {lan('icalctext')} 🧮",
            buttons=[Button.inline(f"🧮 {lan('icalcopen')}", data="recalc")],
        )
    elif x == "C":
        dgvar("calc")
        await e.answer(f"🗑 {lan('icalcclear')}")
    elif x == "⫷":
        get = gvar("calc")
        if get:
            sgvar("calc", get[:-1])
            await e.answer(str(get[:-1]))
    elif x == "%":
        get = gvar("calc")
        if get:
            sgvar("calc", get + "/100")
            await e.answer(str(get + "/100"))
    elif x == "÷":
        get = gvar("calc")
        if get:
            sgvar("calc", get + "/")
            await e.answer(str(get + "/"))
    elif x == "x":
        get = gvar("calc")
        if get:
            sgvar("calc", get + "*")
            await e.answer(str(get + "*"))
    elif x == "=":
        get = gvar("calc")
        if get:
            if get.endswith(("*", ".", "/", "-", "+")):
                get = get[:-1]
            out = await calcc(get, e, lan("succ_"))
            try:
                num = float(out)
                await e.answer(f"🧮 {lan('result')}: {num}", cache_time=0, alert=True)
            except BaseException:
                dgvar("calc")
                await e.answer(lan("errr_"), cache_time=0, alert=True)
        await e.answer(lan("noresult"))
    else:
        get = gvar("calc")
        if get:
            sgvar("calc", get + x)
            await e.answer(str(get + x))
        sgvar("calc", x)
        await e.answer(str(x))


@doge.tgbot.on(CallbackQuery(data=b"recalc"))
@check_owner
async def recalc_(e):
    await e.edit(f"🧮 {lan('icalctext')} 🧮", buttons=lst)
