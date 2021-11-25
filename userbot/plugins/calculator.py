# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from ..assistant.icalculator import lst
from . import BOT_USERNAME, calcc, dgvar, doge, eor, lan

plugin_category = "tool"


@doge.bot_cmd(
    pattern="calc ([\s\S]*)",
    command=("calc", plugin_category),
    info={
        "header": "To solve basic mathematics equations.",
        "description": "Solves the given maths equation by BODMAS rule.",
        "usage": ["{tr}calc", "{tr}calc 3+5+7+8+9-1"],
    },
)
async def calculator(event):
    "To solve basic mathematics equations."
    cmd = event.text.split(" ", maxsplit=1)[1]
    try:
        dgvar("calc")
        if event.client._bot:
            return await event.reply(f"🧮 {lan('icalctext')} 🧮", buttons=lst)
        results = await event.client.inline_query(BOT_USERNAME, "calc")
        await results[0].click(event.chat_id, silent=True, hide_via=True)
        await event.delete()
    except Exception or cmd:
        event = await eor(event, "Calculating...")
        out = await calcc(
            cmd, event, "Sorry I can't find result for the given equation"
        )
        final_output = "**EQUATION:** `{}` \n\n **SOLUTION:** \n`{}` \n".format(
            cmd, out
        )
        await event.edit(final_output)
