# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from . import (
    BOT_USERNAME,
    BOTLOG,
    BOTLOG_CHATID,
    OWNER_ID,
    _format,
    dgvar,
    doge,
    edl,
    eor,
    gvar,
    logging,
    reply_id,
    sgvar,
    time_formatter,
    tr,
)
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


@doge.shiba_cmd(pattern="^/help$", from_users=OWNER_ID)
async def bot_help(event):
    await event.reply(
        f"""🐾 The commands in the bot are:
**Noᴛᴇ:** __This commands work only in this bot:__ {BOT_USERNAME}

• **Cᴍᴅ:** /uinfo <reply to user message>
• **Iɴꜰo:** __You have noticed that forwarded stickers/emoji doesn't have forward tag so you can identify the user who sent thoose messages by this cmd.__
• **Noᴛᴇ:** __It works for all forwarded messages. Even for users who's permission forward message nobody.__

• **Cᴍᴅ:** /ban <username> <reason>
• **Iɴꜰo:** __Reply to a user message with reason so he will be notified as you banned from the bot and his messages won't be forwarded to you further.__
• **Noᴛᴇ:** __Reason is must. Without reason it won't work.__

• **Cᴍᴅ:** /unban <username> <reason>
• **Iɴꜰo:** __Reply to user message or provide username/userid to unban from the bot.__
• **Noᴛᴇ:** `{tr}botbans` __To check banned users list use.__

• **Cᴍᴅ:** /broadcast
• **Iɴꜰo:** `{tr}botusers` __Reply to a message to get broadcasted to every user who started your bot. To get list of users use.__
• **Noᴛᴇ:** __If user stoped/blocked the bot then he will be removed from your database that is he will erased from the bot_starters list.__
"""
    )


@doge.shiba_cmd(pattern="^/broadcast$", from_users=OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**ℹ️ Reply to a message for broadcasting first!**")

    start_ = datetime.now()
    br_cast = await replied.reply("**🔊 Broadcasting...**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply(
            "**ℹ️ No one started your {} yet.**".format(BOT_USERNAME)
        )

    users = get_all_starters()
    if users is None:
        return await event.reply(f"**🚨 Eʀʀoʀ:**\n`➡️ While fetching users list.`")

    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "**🔊 You received a new broadcast.**"
            )
            await event.client.send_message(int(user.user_id), replied)
            await sleep(0.8)
        except FloodWaitError as e:
            await sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**🚨 Eʀʀoʀ:**\n`ℹ️ While broadcasting.`\n➡️ `{e}`"
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        f"**🔊 Broadcasting...**\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• **✅ Sᴜccᴇss:** `{count}`\n"
                        + f"• **❌ Fᴀɪʟᴇᴅ:** `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await sleep(e.seconds)
    end_ = datetime.now()
    b_info = "🔊 Successfully broadcasted message to ➡️ <b>{} users.</b>".format(count)
    if len(blocked_users) != 0:
        b_info += f"\n🚫 <b>{len(blocked_users)} users</b> blocked your {BOT_USERNAME} recently, so have been removed."
    b_info += "⏱ <code>Process took: {}</code>.".format(
        time_formatter((end_ - start_).seconds)
    )
    await br_cast.edit(b_info, parse_mode="html")


@doge.bot_cmd(
    pattern="botusers$",
    command=("botusers", plugin_category),
    info={
        "header": "To get users list who started bot.",
        "description": "To get compelete list of users who started your bot.",
        "usage": "{tr}botusers",
    },
)
async def ban_starters(event):
    "To get users list who started bot."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edl(
            event, "**ℹ️ No one started your {} yet.**".format(BOT_USERNAME)
        )

    msg = f"**🐾 The list of users who started your {BOT_USERNAME} are:\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.user_id)}\
                \n   **🆔 User ID:** `{user.user_id}`\
                \n   **ℹ️ Username:** @{user.username}\
                \n   **📅 Date:** __{user.date}__\n\n"
    await eor(event, msg)


@doge.shiba_cmd(pattern="^/ban\\s+([\\s\\S]*)", from_users=OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id,
            "Sorry! I couldn't find this user in my database",
            reply_to=reply_to,
        )

    if not reason:
        return await event.client.send_message(
            event.chat_id,
            "**🚨 To ban the user provide reason first!**",
            reply_to=reply_to,
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**🚨 Eʀʀoʀ:**\n➡️ `{e}`")

    if user_id == OWNER_ID:
        return await event.reply("**🚨 I can't ban you master.**")

    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #ALREADY_BANNED\
            \n➡️ User already exists in my banned users list.\
            \n**📅 Date:** `{check.date}`\
            \n**⛓ Reason:** `{check.reason}`",
        )

    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.shiba_cmd(pattern="^/unban(?:\\s|$)([\\s\\S]*)", from_users=OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**🚨 I couldn't find user.", reply_to=reply_to
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**🚨 Eʀʀoʀ:**\n➡️ `{e}`")

    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #USER_NOTBANNED\
            \n👤 {_format.mentionuser(user.first_name, user.id)} doesn't exist in my banned users list.",
        )

    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.bot_cmd(
    pattern="botbans$",
    command=("botbans", plugin_category),
    info={
        "header": "To get users list who are banned in bot.",
        "description": "To get list of users who are banned in bot.",
        "usage": "{tr}botbans",
    },
)
async def ban_starters(event):
    "To get users list who are banned in bot."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edl(event, f"**ℹ️ No one is banned in your {BOT_USERNAME} yet.**")

    msg = f"**🐾 The list of users who are banned in your {BOT_USERNAME} are:\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.chat_id)}\
                \n   **🆔 User ID:** `{user.chat_id}`\
                \n   **ℹ️ Username:** @{user.username}\
                \n   **📅 Date:** __{user.date}__\
                \n   **⛓ Reason:** __{user.reason}__\n\n"
    await eor(event, msg)


@doge.bot_cmd(
    pattern="botantif (on|off)$",
    command=("botantif", plugin_category),
    info={
        "header": "To enable or disable bot antiflood.",
        "description": "If it was turned on then after 10 messages or 10 edits of same messages in less time then your bot auto locks them.",
        "usage": [
            "{tr}botantif on",
            "{tr}botantif off",
        ],
    },
)
async def ban_antiflood(event):
    "To enable or disable bot antiflood."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvar("bot_antif") is not None:
            return await edl(event, "**ℹ️ Bot AntiFlood was already enabled.**")

        sgvar("bot_antif", True)
        await edl(event, "**ℹ️ Bot AntiFlood enabled.**")
    elif input_str == "off":
        if gvar("bot_antif") is None:
            return await edl(event, "**ℹ️ Bot AntiFlood was already disabled.**")

        dgvar("bot_antif")
        await edl(event, "**ℹ️ Bot AntiFlood disabled.**")
