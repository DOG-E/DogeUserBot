from json import loads
from re import sub

from . import AioHttp, Config, doge, edl, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="cur(?:\s|$)([\s\S]*)",
    command=("cur", plugin_category),
    info={
        "header": "To convert one currency value to other.",
        "description": "To find exchange rates of currencies.",
        "usage": "{tr}cur <value> <from currencyid> <to currencyid>",
        "examples": "{tr}cur 10 USD INR",
        "note": "List of currency ids are [Country & Currency](https://telegra.ph/CURRENCY-DATA-06-30)",
    },
)
async def currency(event):
    """To convert one currency value to other."""
    if Config.CURRENCY_API is None:
        return await edl(
            event,
            "__You haven't set the api value. Set Api var __`CURRENCY_API` __in heroku get value from https://free.currencyconverterapi.com__.",
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
            f"https://free.currconv.com/api/v7/convert?q={fromcurrency}_{tocurrency}&compact=ultra&apiKey={Config.CURRENCY_API}"
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
            "__It seems you are using different currency value. which doesn't exist on earth.__",
        )
