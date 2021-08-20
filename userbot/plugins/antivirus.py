from . import doge, eor, fsmessage, parse_pre, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="scan(i)?$",
    command=("scan", plugin_category),
    info={
        "header": "To scan the replied file for virus.",
        "flag": {"i": "to get output as image."},
        "usage": ["{tr}scan", "{tr}scani"],
    },
)
async def _(event):
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id:
        return await eor(event, "```Reply to any user message.```")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await eor(event, "```Reply to a media message```")
    chat = "@VS_Robot"
    dogevent = await eor(event, "`Sliding my tip, of fingers over it`")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event=event, text="/start", chat=chat)
        await conv.get_response()
        await event.client.forward_messages(chat, reply_message)
        response1 = await conv.get_response()
        if response1.text:
            await event.client.send_read_acknowledge(conv.chat_id)
            return await dogevent.edit(response1.text, parse_mode=parse_pre)
        await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        response3 = await conv.get_response()
        response4 = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if not input_str:
            return await eor(dogevent, response4.text)
        await dogevent.delete()
        await event.client.send_file(
            event.chat_id, response3.media, reply_to=(await reply_id(event))
        )
        await conv.mark_read()
        await conv.cancel_all()
