# Copyright (C) 2020 Frizzy
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, edl, eor, fsmessage, newmsgres

plugin_category = "misc"


@doge.bot_cmd(
    pattern="tiktok ([\s\S]*)",
    command=("tiktok", plugin_category),
    info={
        "h": "To download tiktok video.",
        "d": "Download tiktok videos without watermark.",
        "u": [
            "{tr}tiktok <link>",
        ],
    },
)
async def _(event):
    d_link = event.pattern_match.group(1)
    if "vm." and ".com" not in d_link:
        await edl(
            event,
            "`Sorry, the link is not supported. Please find another link.`\n**Example:** `vm.tiktok.com`",
            15,
        )
    else:
        await eor(event, "**⏳ Processing...**")
    chat = "@TTSaveBot"
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, d_link, chat=chat)
        video = await newmsgres(conv, chat)
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(
            event.chat_id, video.message.media, video_note=True
        )
        await event.delete()
        await conv.mark_read()
        await conv.cancel_all()
