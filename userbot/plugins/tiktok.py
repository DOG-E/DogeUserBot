# Copyright (C) 2020 Frizzy.
from . import doge, edl, eor, fsmessage, lan

plugin_category = "misc"


@doge.bot_cmd(
    pattern="tiktok ([\s\S]*)",
    command=("tiktok", plugin_category),
    info={
        "header": "To download tiktok video.",
        "description": "Download tiktok videos without watermark.",
        "usage": [
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
        await eor(event, lan("processing"))
    chat = "@TTSaveBot"
    async with event.client.conversation(chat) as conv:
        await fsmessage(event=event, text=d_link, chat=chat)
        await conv.get_response()
        video = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(event.chat_id, video, video_note=True)
        await event.delete()
        await conv.mark_read()
        await conv.cancel_all()
