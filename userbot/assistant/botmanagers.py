# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from math import floor

from telethon.utils import get_display_name

from ..sql_helper.bot_blacklists import add_user_to_bl, rem_user_from_bl
from ..sql_helper.bot_pms_sql import get_user_id
from . import BOTLOG, BOTLOG_CHATID, Config, _format, doge, logging, reply_id

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


async def get_user_and_reason(event):
    id_reason = event.pattern_match.group(1)
    replied = await reply_id(event)
    user_id, reason = None, None
    if replied:
        users = get_user_id(replied)
        if users is not None:
            for usr in users:
                user_id = int(usr.chat_id)
                break
            reason = id_reason
    elif id_reason:
        data = id_reason.split(maxsplit=1)
        if len(data) == 2:
            user, reason = data
        elif len(data) == 1:
            user = data[0]
        if user.isdigit():
            user_id = int(user)
        if user.startswith("@"):
            user_id = user
    return user_id, reason


# Taken from https://github.com/code-rgb/USERGE-X/blob/f95766027ef95854d05e523b42cd158c2e8cdbd0/userge/plugins/bot/bot_forwards.py#L420
def progress_str(total: int, current: int) -> str:
    percentage = current * 100 / total
    prog_arg = "**ℹ️ {}:** `{}%`\n" "```[{}{}]```"
    return prog_arg.format(
        "Progress",
        percentage,
        "".join((Config.FINISHED_PROGRESS_STR for i in range(floor(percentage / 5)))),
        "".join(
            (Config.UNFINISHED_PROGRESS_STR for i in range(20 - floor(percentage / 5)))
        ),
    )


async def ban_user_from_bot(user, reason, reply_to=None):
    try:
        date = str(datetime.now().strftime("%B %d, %Y"))
        add_user_to_bl(user.id, get_display_name(user), user.username, reason, date)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = f"**🚫 You have been banned forever from using this bot.\
        \n⛓ Reason:** {reason}"
    await doge.tgbot.send_message(user.id, banned_msg)
    info = f"**⚠️ #BANNED_BOT_PM_USER**\
            \n\n👤 {_format.mentionuser(get_display_name(user), user.id)}\
            \n**ℹ️ First Name:** {user.first_name}\
            \n**🆔 User ID:** `{user.id}`\
            \n**⛓ Reason:** `{reason}`"
    if BOTLOG:
        await doge.send_message(BOTLOG_CHATID, info)
    return info


async def unban_user_from_bot(user, reason, reply_to=None):
    try:
        rem_user_from_bl(user.id)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = f"**👀 You have been unbanned from this bot.\
        \nℹ️ From now on you can send messages here to contact my master.**"
    if reason is not None:
        banned_msg += f"\n**⛓ Reason:** `{reason}`"
    await doge.tgbot.send_message(user.id, banned_msg)
    info = f"**⚠️ #UNBANNED_BOT_PM_USER**\
            \n\n👤 {_format.mentionuser(get_display_name(user), user.id)}\
            \n**ℹ️ First Name:** {user.first_name}\
            \n**🆔 User ID:** `{user.id}`"
    if BOTLOG:
        await doge.send_message(BOTLOG_CHATID, info)
    return info
