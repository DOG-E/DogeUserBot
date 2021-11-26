# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from . import doge, logging

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


@doge.bot_cmd(
    pattern="sdm (\d*) ([\s\S]*)",
    command=("sdm", plugin_category),
    info={
        "h": "To self destruct the message after paticualr time.",
        "d": "Suppose if you use .sdm 10 hi then message will be immediately send new message as hi and then after 10 sec this message will auto delete.`",
        "u": "{tr}sdm [number] [text]",
        "e": "{tr}sdm 10 hi",
    },
)
async def selfdestruct(destroy):
    "To self destruct the sent message"
    dog = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = dog[1]
    ttl = int(dog[0])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, message)
    await sleep(ttl)
    await smsg.delete()


@doge.bot_cmd(
    pattern="selfdm (\d*) ([\s\S]*)",
    command=("selfdm", plugin_category),
    info={
        "h": "To self destruct the message after paticualr time. and in message will show the time.",
        "d": "Suppose if you use .sdm 10 hi then message will be immediately will send new message as hi and then after 10 sec this message will auto delete.",
        "u": "{tr}selfdm [number] [text]",
        "e": "{tr}selfdm 10 hi",
    },
)
async def selfdestruct(destroy):
    "To self destruct the sent message"
    dog = ("".join(destroy.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = dog[1]
    ttl = int(dog[0])
    text = message + f"\n\n`This message shall be self-destructed in {ttl} seconds`"
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(ttl)
    await smsg.delete()
