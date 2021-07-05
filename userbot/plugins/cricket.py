# Created: @jisan7509 (@jisan09)
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id

plugin_category = "extra"


@doge.ub(
    pattern="score$",
    command=("score", plugin_category),
    info={
        "header": "To see the score of an ongoing match.",
        "usage": "{tr}score",
    },
)
async def _(event):
    "To see the score of an ongoing match."
    chat = "@cricbuzz_bot"
    reply_to_id = await reply_id(event)
    dogevent = await edit_or_reply(event, "```Gathering info...```")
    async with event.client.conversation(chat) as conv:
        try:
            try:
                msg_start = await conv.send_message("/start")
            except YouBlockedUserError:
                event.client(UnblockRequest(chat))
                await dogevent.edit(
                    "**⛔ You've previously blocked @Cricbuzz_Bot!\
                    \n🔔 I unblocked @Cricbuzz_Bot and I'm trying again.**"
                )
                msg_start = await conv.send_message("/start")

            response = await conv.get_response()
            msg = await conv.send_message("/score")
            respond = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if respond.text.startswith("I can't find that"):
                await dogevent.edit("sorry i can't find it")
            else:
                await dogevent.delete()
                await event.client.send_message(
                    event.chat_id, respond.message, reply_to=reply_to_id
                )
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, msg.id, response.id, respond.id]
            )
        except:
            return await edit_delete(dogevent, "**🔔 Something went wrong!**")


@doge.ub(
    pattern="cric ([\s\S]*)",
    command=("cric", plugin_category),
    info={
        "header": "To see the scoreboard or commentary of a match",
        "description": "To check commands showed in {tr}score cmd that is for getting scoreboard or commentary.",
        "usage": "{tr}cric <command showed in {tr}score>",
        "examples": "{tr}cric /scorecard_30....",
    },
)
async def _(event):
    "To see the scoreboard or commentary of a match"
    details = event.pattern_match.group(1)
    chat = "@cricbuzz_bot"
    reply_to_id = await reply_id(event)
    dogevent = await edit_or_reply(event, "```Gathering info...```")
    async with event.client.conversation(chat) as conv:
        try:
            try:
                msg_start = await conv.send_message("/start")
            except YouBlockedUserError:
                event.client(UnblockRequest(chat))
                await dogevent.edit(
                    "**⛔ You've previously blocked @Cricbuzz_Bot!\
                    \n🔔 I unblocked @Cricbuzz_Bot and I'm trying again.**"
                )
                msg_start = await conv.send_message("/start")

                response = await conv.get_response()
                msg = await conv.send_message(f"{details}")
                respond = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            if respond.text.startswith("I can't find that"):
                await dogevent.edit("sorry i can't find it")
            else:
                await dogevent.delete()
                await event.client.send_message(
                    event.chat_id, respond.message, reply_to=reply_to_id
                )
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, msg.id, response.id, respond.id]
            )

        except:
            return await edit_delete(dogevent, "**🔔 Something went wrong!**")
