"""
Plugin Alltag by KENZO
for catuserbot
"""
# Based alltag command from ultroid
from asyncio import sleep
from random import choice

from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
)
from telethon.utils import get_display_name

from ..helpers.fonts import emojitag
from . import doge, get_user_from_event, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="(tagall|all)(?:\s|$)([\s\S]*)",
    command=("tagall", plugin_category),
    info={
        "header": "tags recent 50 persons in the group may not work for all",
        "usage": [
            "{tr}all <text>",
            "{tr}tagall",
        ],
    },
)
async def _(event):
    "To tag all."
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(2)
    mentions = input_str or "@all"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 50):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@doge.bot_cmd(
    pattern="report$",
    command=("report", plugin_category),
    info={
        "header": "To tags admins in group.",
        "usage": "{tr}report",
    },
)
async def _(event):
    "To tags admins in group."
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    reply_to_id = await reply_id(event)
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@doge.bot_cmd(
    pattern="men ([\s\S]*)",
    command=("mention", plugin_category),
    info={
        "header": "Tags that person with the given custom text.",
        "usage": [
            "{tr}men username/userid text",
            "text (username/mention)[custom text] text",
        ],
        "examples": ["{tr}men @teledoge hi", "Hi @teledoge[How are you?]"],
    },
)
async def _(event):
    "Tags that person with the given custom text."
    user, input_str = await get_user_from_event(event)
    if not user:
        return
    reply_to_id = await reply_id(event)
    await event.delete()
    await event.client.send_message(
        event.chat_id,
        f"<a href='tg://user?id={user.id}'>{input_str}</a>",
        parse_mode="HTML",
        reply_to=reply_to_id,
    )


@doge.bot_cmd(
    pattern="alltag(?:\s|$)([\s\S]*)",
    command=("alltag", plugin_category),
    info={
        "header": "Tag all members in the group.",
        "description": "This feature is to tag members in the group, including owner and admin. This plugins no admin title required.",
        "usage": [
            "{tr}alltag <text>",
        ],
        "examples": "{tr}alltag",
    },
    groups_only=True,
)
async def alltags(event):
    text = (event.pattern_match.group(1)).strip()
    users = []
    limit = 0

    if event.fwd_from:
        return

    async for x in event.client.iter_participants(event.chat_id):
        if not (x.bot or x.deleted):
            if not isinstance(
                x.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
            ):
                users.append(f" [{get_display_name(x)}](tg://user?id={x.id}) ")
            if isinstance(x.participant, ChannelParticipantAdmin):
                users.append(
                    f"**👮 Admin: **[{get_display_name(x)}](tg://user?id={x.id}) "
                )
            if isinstance(x.participant, ChannelParticipantCreator):
                users.append(
                    f"**🤴 Owner: **[{get_display_name(x)}](tg://user?id={x.id}) "
                )

    mentions = list(user_list(users, 6))
    for mention in mentions:
        try:
            mention = "  |  ".join(map(str, mention))
            if text:
                mention = f"{text}\n{mention}"
            if event.reply_to_msg_id:
                await event.client.send_message(
                    event.chat_id, mention, reply_to=event.reply_to_msg_id
                )

            else:
                await event.client.send_message(event.chat_id, mention)

            limit += 6
            await sleep(2)
        except BaseException:
            pass

    await event.delete()


@doge.bot_cmd(
    pattern="etag(?:\s|$)([\s\S]*)",
    command=("etag", plugin_category),
    info={
        "header": "Tag all with emojis members in the group.",
        "description": "This feature is to tag with emojis members in the group. This plugins no admin title required.",
        "usage": [
            "{tr}etag <text>",
        ],
        "examples": "{tr}etag",
    },
    groups_only=True,
)
async def etags(event):
    text = (event.pattern_match.group(1)).strip()
    users = []
    limit = 0

    if event.fwd_from:
        return

    async for x in event.client.iter_participants(event.chat_id):
        if not (x.bot or x.deleted):
            if not isinstance(
                x.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)
            ):
                users.append(f" [{choice(emojitag)}](tg://user?id={x.id}) ")
            if isinstance(x.participant, ChannelParticipantAdmin):
                users.append(f" [{choice(emojitag)}](tg://user?id={x.id}) ")
            if isinstance(x.participant, ChannelParticipantCreator):
                users.append(f" [{choice(emojitag)}](tg://user?id={x.id}) ")

    mentions = list(user_list(users, 6))
    for mention in mentions:
        try:
            mention = " ".join(map(str, mention))
            if text:
                mention = f"{text}\n{mention}"
            if event.reply_to_msg_id:
                await event.client.send_message(
                    event.chat_id, mention, reply_to=event.reply_to_msg_id
                )

            else:
                await event.client.send_message(event.chat_id, mention)

            limit += 6
            await sleep(2)
        except BaseException:
            pass

    await event.delete()


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]
