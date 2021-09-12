# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from logging import getLogger
from typing import Union

from telethon.tl.types import Channel, Chat, User
from telethon.utils import get_display_name

from .events import NewMessage

LOGS = getLogger("userbot")


def printUser(entity: User) -> None:
    """Print the user's first name + last name upon start"""
    user = get_display_name(entity)
    LOGS.warning("Successfully logged in as {0}".format(user))


async def get_chat_link(
    arg: Union[User, Chat, Channel, NewMessage.Event], reply=None
) -> str:
    if isinstance(arg, (User, Chat, Channel)):
        entity = arg
    else:
        entity = await arg.get_chat()

    if isinstance(entity, User):
        if entity.is_self:
            name = 'your "Saved Messages"'
        else:
            name = get_display_name(entity) or "Deleted Account?"
        extra = f"[{name}](tg://user?id={entity.id})"
    else:
        if hasattr(entity, "username") and entity.username is not None:
            username = "@" + entity.username
        else:
            username = entity.id
        if reply is not None:
            if isinstance(username, str) and username.startswith("@"):
                username = username[1:]
            else:
                username = f"c/{username}"
            extra = f"[{entity.title}](https://t.me/{username}/{reply})"
        elif isinstance(username, int):
            username = f"`{username}`"
            extra = f"{entity.title} ( {username} )"
        else:
            extra = f"[{entity.title}](tg://resolve?domain={username})"
    return extra
