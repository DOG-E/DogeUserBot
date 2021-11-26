# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from . import doge

plugin_category = "misc"


@doge.bot_cmd(
    pattern="schd (\d*) ([\s\S]*)",
    command=("schd", plugin_category),
    info={
        "h": "To schedule a message after given time(in seconds).",
        "u": "{tr}schd <time_in_seconds>  <message to send>",
        "e": "{tr}schd 120 hello",
    },
)
async def _(event):
    "To schedule a message after given time"
    dog = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = dog[1]
    ttl = int(dog[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
