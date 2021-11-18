# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# /help
# /broadcast
# /ban
# /unban
# botusers
# botbans
# botantif
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
    lan,
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
        f"""{lan('botcmdhead')}:
**{lan('note')}:** __{lan('botcmdnote')}:__ {BOT_USERNAME}

• **{lan('cmd')}:** /uinfo <{lan('replymsg')}>
• **{lan('info')}:** __{lan('botcmdinfo1')}__
• **{lan('note')}:** __{lan('botcmdnote1')}__

• **{lan('cmd')}:** /ban <{lan('username')}> <{lan('reason')}>
• **{lan('info')}:** __{lan('botcmdinfo2')}__
• **{lan('note')}:** __{lan('botcmdnote2')}__

• **{lan('cmd')}:** /unban <{lan('username')}> <{lan('reason')}>
• **{lan('info')}:** __{lan('botcmdinfo3')}__
• **{lan('note')}:** `{tr}botbans` __{lan('botcmdnote3')}__

• **{lan('cmd')}:** /broadcast
• **{lan('info')}:** `{tr}botusers` __{lan('botcmdinfo4')}__
• **{lan('note')}:** __{lan('botcmdnote4')}__
"""
    )


@doge.shiba_cmd(pattern="^/broadcast$", from_users=OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply(lan("shldreplymsg"))

    start_ = datetime.now()
    br_cast = await replied.reply(lan("broadcasting"))
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply(lan("nostartedbc").format(BOT_USERNAME))

    users = get_all_starters()
    if users is None:
        return await event.reply(f"{lan('errr')}\n`➡️ {lan('errrfetchusers')}`")

    for user in users:
        try:
            await event.client.send_message(int(user.user_id), lan("notifbc"))
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
                    BOTLOG_CHATID, f"{lan('errr')}\n`ℹ️ {lan('errrbcing')}`\n➡️ `{e}`"
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        f"{lan('broadcasting')}\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• {lan('success')} `{count}`\n"
                        + f"• {lan('failed')} `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await sleep(e.seconds)
    end_ = datetime.now()
    b_info = lan("succ_bc").format(count)
    if len(blocked_users) != 0:
        b_info += f"\n🚫 {lan('blockedbc').format(len(blocked_users), BOT_USERNAME)}"
    b_info += lan("bcprocesstook").format(time_formatter((end_ - start_).seconds))
    await br_cast.edit(b_info, parse_mode="html")


@doge.bot_cmd(
    pattern="botusers$",
    command=("botusers", plugin_category),
    info={
        "header": lan("head_botusers"),
        "description": lan("desc_botusers"),
        "usage": "{tr}botusers",
    },
)
async def ban_starters(event):
    f"{lan('head_botusers')}"
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edl(event, lan("nostartedbot").format(BOT_USERNAME))

    msg = f"**🐾 {lan('liststartedbotu').format(BOT_USERNAME)}\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.user_id)}\
                \n   **🆔 {lan('userx')} ID:** `{user.user_id}`\
                \n   **ℹ️ {lan('user_name')}:** @{user.username}\
                \n   {lan('date')} __{user.date}__\n\n"
    await eor(event, msg)


@doge.shiba_cmd(pattern="^/ban\\s+([\\s\\S]*)", from_users=OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, lan("errrfinduser"), reply_to=reply_to
        )

    if not reason:
        return await event.client.send_message(
            event.chat_id,
            lan("shldreasontoban"),
            reply_to=reply_to,
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"{lan('errr')}\n➡️ `{e}`")

    if user_id == OWNER_ID:
        return await event.reply(lan("errrbanmaster"))

    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #ALREADY_BANNED\
            \n➡️ {lan('alreadybanned')}\
            \n{lan('date')} `{check.date}`\
            \n**⛓ {lan('reason').title()}:** `{check.reason}`",
        )

    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.shiba_cmd(pattern="^/unban(?:\\s|$)([\\s\\S]*)", from_users=OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, lan("errrfinduser"), reply_to=reply_to
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"{lan('errr')}\n➡️ `{e}`")

    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #USER_NOTBANNED\
            \n👤 {lan('unotbanned').format(_format.mentionuser(user.first_name, user.id))}",
        )

    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.bot_cmd(
    pattern="botbans$",
    command=("botbans", plugin_category),
    info={
        "header": lan("head_botbans"),
        "description": lan("desc_botbans"),
        "usage": "{tr}botbans",
    },
)
async def ban_starters(event):
    f"{lan('head_botbans')}"
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edl(event, lan("nobannedbot"))

    msg = f"**🐾 {lan('listbannedbotu').format(BOT_USERNAME)}\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.chat_id)}\
                \n   **🆔 {lan('userx')} ID:** `{user.chat_id}`\
                \n   **ℹ️ {lan('user_name')}:** @{user.username}\
                \n     {lan('date')} __{user.date}__\
                \n   **⛓ {lan('reason').title()}:** __{user.reason}__\n\n"
    await eor(event, msg)


@doge.bot_cmd(
    pattern="botantif (on|off)$",
    command=("botantif", plugin_category),
    info={
        "header": lan("head_botantif"),
        "description": lan("desc_botantif"),
        "usage": [
            "{tr}botantif on",
            "{tr}botantif off",
        ],
    },
)
async def ban_antiflood(event):
    f"{lan('head_botantif')}"
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvar("bot_antif") is not None:
            return await edl(event, lan("alreadyafloodenb"))

        sgvar("bot_antif", True)
        await edl(event, lan("afloodenabled"))
    elif input_str == "off":
        if gvar("bot_antif") is None:
            return await edl(event, lan("alreadyaflooddsb"))

        dgvar("bot_antif")
        await edl(event, lan("aflooddisabled"))
