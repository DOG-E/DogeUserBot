# Credits: @sandy1709
# Idea: @BlazingRobonix
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from telethon.utils import get_display_name

from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import doge, edl, eor, get_user_from_event, wowmydev

plugin_category = "fun"


@doge.bot_cmd(
    pattern="addecho$",
    command=("addecho", plugin_category),
    info={
        "h": "To repeat messages sent by the user.",
        "d": "Reply to user with this cmd so from then his every text and sticker messages will be repeated back to him.",
        "u": "{tr}addecho <reply>",
    },
)
async def echo(event):
    "To echo the user messages"
    if event.reply_to_msg_id is None:
        return await eor(event, "`Reply to a User's message to echo his messages`")
    dogevent = await eor(event, "`Adding Echo to user...`")
    user, rank = await get_user_from_event(event, dogevent, nogroup=True)
    if not user:
        return
    userid = user.id
    if await wowmydev(userid, event):
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = get_display_name(await event.get_chat())
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await eor(event, "The user is already enabled with echo ")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edl(dogevent, f"**Error:**\n`{e}`")
    else:
        await eor(dogevent, "Hi")


@doge.bot_cmd(
    pattern="rmecho$",
    command=("rmecho", plugin_category),
    info={
        "h": "To stop repeating paticular user messages.",
        "d": "Reply to user with this cmd to stop repeating his messages back.",
        "u": "{tr}rmecho <reply>",
    },
)
async def echo(event):
    "To stop echoing the user messages"
    if event.reply_to_msg_id is None:
        return await eor(event, "Reply to a User's message to echo his messages")
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edl(event, f"**Error:**\n`{e}`")
        else:
            await eor(event, "Echo has been stopped for the user")
    else:
        await eor(event, "The user is not activated with echo")


@doge.bot_cmd(
    pattern="delecho( .a)?",
    command=("delecho", plugin_category),
    info={
        "h": "To delete echo in this chat.",
        "d": "To stop echoing users messages of all enabled users in the paticular chat or all chats.",
        "f": {"a": "To stop in all chats"},
        "u": [
            "{tr}delecho",
            "{tr}delecho .a",
        ],
    },
)
async def echo(event):
    "To delete echo in this chat."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edl(
                event, "You haven't enabled echo atleast for one user in any chat."
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edl(event, f"**Error:**\n`{str(e)}`")
        else:
            await eor(event, "Deleted echo for all enabled users in all chats.")
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edl(
                event, "You haven't enabled echo atleast for one user in this chat."
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edl(event, f"**Error:**\n`{e}`")
        else:
            await eor(event, "Deleted echo for all enabled users in this chat")


@doge.bot_cmd(
    pattern="listecho( .a)?$",
    command=("listecho", plugin_category),
    info={
        "h": "shows the list of users for whom you enabled echo",
        "f": {
            "a": "To list echoed users in all chats",
        },
        "u": [
            "{tr}listecho",
            "{tr}listecho .a",
        ],
    },
)
async def echo(event):  # sourcery no-metrics
    "To list all users on who you enabled echoing."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**Echo enabled users:**\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) <= 0:
            return await eor(event, "There are no echo enabled users")
        for echos in lsts:
            if echos.chat_type == "Personal":
                if echos.user_username:
                    private_chats += (
                        f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    )
                else:
                    private_chats += (
                        f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                    )
            elif echos.user_username:
                group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"
            else:
                group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"
        if private_chats != "":
            output_str += "**Private Chats**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**Group Chats**\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await eor(event, "There are no echo enabled users in this chat")

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = "**Echo enabled users in this chat are:**\n" + private_chats

    await eor(event, output_str)


@doge.bot_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
