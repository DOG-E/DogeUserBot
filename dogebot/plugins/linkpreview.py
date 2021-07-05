# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from dogebot import doge

from ..core.managers import edit_or_reply
from ..helpers.functions.functions import linkpreviewb

plugin_category = "utils"


@doge.ub(
    pattern="ctg$",
    command=("ctg", plugin_category),
    info={
        "header": "Reply to link To get link preview using Telegra.ph",
        "usage": "{tr}ctg",
    },
)
async def _(event):
    "To get link preview"
    reply_message = await event.get_reply_message()
    if not reply_message:
        await edit_or_reply(event, "```Reply to a Link.```")
        return
    if not reply_message.text:
        await edit_or_reply(event, "```Reply to a Link```")
        return
    dogevent = await edit_or_reply(event, "```Processing```")
    await linkpreviewb(event.client, event.chat_id, reply_message)
    