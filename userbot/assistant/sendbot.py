# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, edl, reply_id

plugin_category = "bot"


@doge.bot_cmd(
    pattern="bot(?:\s|$)([\s\S]*)",
    command=("bot", plugin_category),
    info={
        "h": "Bot sohbetteyse, yardımcı botunuzdan herhangi bir metni gönderin.",
        "u": "{tr}bot <yazı/yanıtlanmış mesaj>",
        "e": "{tr}bot Herkese Merhaba!",
    },
)
async def botmsg(event):
    "Bot sohbetteyse, yardımcı botunuzdan herhangi bir metni gönderin."
    text = event.pattern_match.group(1)
    chat = event.chat_id
    reply_message = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    if not text:
        if reply_message.media:
            media = await reply_message.download_media()
            if reply_message.text:
                await doge.bot.send_file(chat, media, caption=reply_message.text)
            else:
                await doge.bot.send_file(chat, media)
            return await event.delete()

        else:
            return await edl(
                event,
                "__Bot üzerinden ne göndermeliyim? Bana bir metin verin ya da mesajı yanıtlayın.__",
            )

    await doge.bot.send_message(chat, text, reply_to=reply_to_id)
    await event.delete()
