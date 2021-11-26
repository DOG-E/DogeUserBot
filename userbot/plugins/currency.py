# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import loads
from re import sub

from . import CURRENCY_API, AioHttp, doge, edl, eor, tr

plugin_category = "tool"


@doge.bot_cmd(
    pattern="cur(?:\s|$)([\s\S]*)",
    command=("cur", plugin_category),
    info={
        "h": "To convert one currency value to other.",
        "d": "To find exchange rates of currencies.",
        "u": "{tr}cur <value> <from currencyid> <to currencyid>",
        "e": "{tr}cur 10 USD INR",
        "note": "List of currency ids are [Country & Currency](https://telegra.ph/CURRENCY-DATA-06-30)",
    },
)
async def currency(event):
    """To convert one currency value to other."""
    if CURRENCY_API is None:
        return await edl(
            event,
            f"__You haven't set the api value.__ `{tr}setdog CURRENCY_API <api>` __from https://free.currencyconverterapi.com__.",
            link_preview=False,
        )
    input_str = event.pattern_match.group(1)
    values = input_str.split(" ")
    if len(values) == 3:
        value, fromcurrency, tocurrency = values
    else:
        return await edl(event, "__Use proper syntax. check__ `.doge .c cur`")
    fromcurrency = fromcurrency.upper()
    tocurrency = tocurrency.upper()
    try:
        value = float(value)
        aresponse = await AioHttp().get_json(
            f"https://free.currconv.com/api/v7/convert?q={fromcurrency}_{tocurrency}&compact=ultra&apiKey={CURRENCY_API}"
        )
        symbols = await AioHttp().get_raw(
            "https://raw.githubusercontent.com/DOG-E/Source/DOGE/Core/currency.py"
        )
        symbols = loads(sub(", *\n *}", "}", symbols.decode("utf-8")))
        try:
            result = aresponse[f"{fromcurrency}_{tocurrency}"]
        except KeyError:
            return await edl(
                event,
                "__You have used wrong currency codes or Api can't fetch details or try by restarting bot it will work if everything is fine.__",
            )
        output = float(value) * float(result)
        output = round(output, 4)
        await eor(
            event,
            f"The Currency value of **{symbols[fromcurrency]}{value} {fromcurrency}** in **{tocurrency}** is **{symbols[tocurrency]}{output}**",
        )
    except Exception:
        await eor(
            event,
            "__It seems you're using different currency value. which doesn't exist on earth.__",
        )
