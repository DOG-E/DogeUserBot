# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# bot
# ================================================================
from . import doge, edl, reply_id

plugin_category = "bot"


@doge.bot_cmd(
    pattern="bot(?:\s|$)([\s\S]*)",
    command=("bot", plugin_category),
    info={
        "header": "Send any text through your assistant bot if the bot is in the chat",
        "usage": "{tr}bot <text/reply>",
        "examples": "{tr}bot Hello everyone",
    },
)
async def botmsg(event):
    "Send your text through your bot."
    text = event.pattern_match.group(1)
    chat = event.chat_id
    reply_message = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    if not text:
        if reply_message.media:
            media = await reply_message.download_media()
            if reply_message.text:
                await doge.tgbot.send_file(chat, media, caption=reply_message.text)
            else:
                await doge.tgbot.send_file(chat, media)
            return await event.delete()

        else:
            return await edl(
                event,
                "__What should I send through bot? Give some text or give media with reply.__",
            )

    await doge.tgbot.send_message(chat, text, reply_to=reply_to_id)
    await event.delete()
