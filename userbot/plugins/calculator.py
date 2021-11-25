# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import calcc, doge, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="calc ([\s\S]*)",
    command=("calc", plugin_category),
    info={
        "header": "To solve basic mathematics equations.",
        "description": "Solves the given maths equation.",
        "usage": ["{tr}calc", "{tr}calc 3+5+7+8+9-1"],
    },
)
async def calculator(event):
    "To solve basic mathematics equations."
    cmd = event.text.split(" ", maxsplit=1)[1]
    event = await eor(event, "Calculating...")
    out = await calcc(cmd, event, "Sorry I can't find result for the given equation")
    final_output = "**EQUATION:** `{}` \n\n **SOLUTION:** \n`{}` \n".format(cmd, out)
    await event.edit(final_output)
