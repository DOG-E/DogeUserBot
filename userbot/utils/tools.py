# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import ChatAdminRights


async def create_supergroup(group_name, client, botusername, descript, photo):
    try:
        result = await client(
            CreateChannelRequest(
                title=group_name,
                about=descript,
                megagroup=True,
            )
        )
        created_chat_id = result.chats[0].id
        await client(
            InviteToChannelRequest(
                channel=created_chat_id,
                users=[botusername],
            )
        )
        if photo:
            await client(
                EditPhotoRequest(
                    channel=created_chat_id,
                    photo=photo,
                )
            )
    except Exception as e:
        return "error", str(e)
    if not str(created_chat_id).startswith("-100"):
        created_chat_id = int("-100" + str(created_chat_id))
    return result, created_chat_id


async def create_channel(channel_name, client, descript, photo):
    try:
        result = await client(
            CreateChannelRequest(
                title=channel_name,
                about=descript,
                megagroup=False,
            )
        )
        created_chat_id = result.chats[0].id
        if photo:
            await client(
                EditPhotoRequest(
                    channel=created_chat_id,
                    photo=photo,
                )
            )
    except Exception as e:
        return "error", str(e)
    if not str(created_chat_id).startswith("-100"):
        created_chat_id = int("-100" + str(created_chat_id))
    return result, created_chat_id


async def add_bot_to_logger_group(client, chat_id, botusername, admintag):
    """
    Asistan botu log gruplarına ekler
    """
    try:
        await client(
            AddChatUserRequest(
                chat_id=chat_id,
                user_id=botusername,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await client(
                InviteToChannelRequest(
                    channel=chat_id,
                    users=[botusername],
                )
            )
        except Exception as e:
            return "error", str(e)
    await sleep(0.5)
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    try:
        await client(EditAdminRequest(chat_id, botusername, rights, admintag))
    except Exception as e:
        return "error", str(e)
    return
