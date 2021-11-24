# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, edl, eor, fsmessage, newmsgres, parse_pre, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="scan(i)?$",
    command=("scan", plugin_category),
    info={
        "header": lan("scan1"),
        "flag": {"i": lan("scan2")},
        "usage": ["{tr}scan", "{tr}scani"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        return await edl(event, lan("scan3"))
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edl(event, lan("scan3"))
    chat = "@VS_Robot"
    dogevent = await eor(event, lan("scan5"))
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response1 = await newmsgres(conv, chat)
        if response1.text:
            await event.client.send_read_acknowledge(conv.chat_id)
            return await dogevent.edit(response1.text, parse_mode=parse_pre)
        await newmsgres(conv, chat)
        await event.client.send_read_acknowledge(conv.chat_id)
        response3 = await newmsgres(conv, chat)
        response4 = await newmsgres(conv, chat)
        await event.client.send_read_acknowledge(conv.chat_id)
        if not input_str:
            return await eor(dogevent, response4.text)
        await dogevent.delete()
        await event.client.send_file(
            event.chat_id, response3.message.media, reply_to=(await reply_id(event))
        )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="vscan$",
    command=("vscan", plugin_category),
    info={
        "header": lan("vscan1"),
        "usage": "{tr}vscan",
    },
)
async def vscan(event):
    if not event.reply_to_msg_id:
        return await edl(event, lan("vscan2"))
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edl(event, lan("vscan3"))
    chat = "@DrWebBot"
    dogevent = await eor(event, lan("vscan4"))
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Forward"):
            return await edl(
                dogevent,
                lan("vscan5"),
            )
        elif response.text.startswith("Select"):
            await event.client.send_message(chat, "English")
            response = await newmsgres(conv, chat)
            await event.client.forward_messages(chat, reply_message)
            response = await newmsgres(conv, chat)
            await dogevent.edit(f"**{lan('vscan6')}** {response.message.message}")
        elif response.text.startswith("No threats"):
            await event.edit(lan("vscan8"))
        elif response.text.startswith("Still"):
            await dogevent.edit(lan("vscan7"))
            response = await newmsgres(conv, chat)
            if response.text.startswith("No threats"):
                await event.edit(lan("vscan8"))
            else:
                await event.edit(lan("vscan9").format(response.message.message))
        await conv.mark_read()
        await conv.cancel_all()
