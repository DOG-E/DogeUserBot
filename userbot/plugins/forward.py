# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from string import ascii_lowercase

from telethon.tl.types import Channel, MessageMediaWebPage

from . import PRIVATE_CHANNEL_ID, doge, edl, logging

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


class FPOST:
    def __init__(self) -> None:
        self.GROUPSID = []
        self.MSG_CACHE = {}


FPOST_ = FPOST()


async def all_groups_id(dog):
    doggroups = []
    async for dialog in dog.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            doggroups.append(entity.id)
    return doggroups


@doge.bot_cmd(
    pattern="frwd$",
    command=("frwd", plugin_category),
    info={
        "h": "To get view counter for the message. that is will delete old message and send new message where you can see how any people saw your message",
        "u": "{tr}frwd",
    },
)
async def _(event):
    "To get view counter for the message"
    if PRIVATE_CHANNEL_ID is None:
        return await edl(
            event,
            "Please set the required environment variable `PRIVATE_CHANNEL_ID` for this plugin to work",
        )
    try:
        e = await event.client.get_entity(PRIVATE_CHANNEL_ID)
    except Exception as e:
        await edl(event, str(e))
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        try:
            await event.delete()
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")


@doge.bot_cmd(
    pattern="resend$",
    command=("resend", plugin_category),
    info={
        "h": "To resend the message again. Useful to remove forword tag",
        "u": "{tr}resend",
    },
)
async def _(event):
    "To resend the message again"
    try:
        await event.delete()
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    m = await event.get_reply_message()
    if not m:
        return
    if m.media and not isinstance(m.media, MessageMediaWebPage):
        return await event.client.send_file(event.chat_id, m.media, caption=m.text)
    await event.client.send_message(event.chat_id, m.text)


@doge.bot_cmd(
    pattern="fpost ([\s\S]*)",
    command=("fpost", plugin_category),
    info={
        "h": "Split the word and forwards each letter from previous messages in that group",
        "u": "{tr}fpost <text>",
        "e": "{tr}fpost DogeUserBot",
    },
)
async def _(event):
    "Split the word and forwards each letter from previous messages in that group"
    await event.delete()
    text = event.pattern_match.group(1)
    destination = await event.get_input_chat()
    if len(FPOST_.GROUPSID) == 0:
        FPOST_.GROUPSID = await all_groups_id(event)
    for c in text.lower():
        if c not in ascii_lowercase:
            continue
        if c not in FPOST_.MSG_CACHE:
            async for msg in event.client.iter_messages(event.chat_id, search=c):
                if msg.raw_text.lower() == c and msg.media is None:
                    FPOST_.MSG_CACHE[c] = msg
                    break
        if c not in FPOST_.MSG_CACHE:
            for i in FPOST_.GROUPSID:
                async for msg in event.client.iter_messages(event.chat_id, search=c):
                    if msg.raw_text.lower() == c and msg.media is None:
                        FPOST_.MSG_CACHE[c] = msg
                        break
        await event.client.forward_messages(destination, FPOST_.MSG_CACHE[c])
