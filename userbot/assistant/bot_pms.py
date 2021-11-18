# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# /start
# /uinfo
#
# Callback:
# bot_pm_ban_([0-9]+)
# toggle_bot-antiflood_off$
# ================================================================
from collections import defaultdict
from datetime import datetime
from re import compile
from typing import Optional, Union

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name
from telethon.errors import UserIsBlockedError
from telethon.events import MessageDeleted, StopPropagation
from telethon.tl.functions.contacts import UnblockRequest

from ..core import pool
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from . import (
    BOT_USERNAME,
    BOTLOG,
    BOTLOG_CHATID,
    OWNER_ID,
    PM_LOGGER_GROUP_ID,
    Config,
    _format,
    check_owner,
    dgvar,
    doge,
    gvar,
    lan,
    logging,
    reply_id,
    tr,
)
from .botmanagers import ban_user_from_bot

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


class FloodConfig:
    BANNED_USERS = set()
    USERS = defaultdict(list)
    MESSAGES = 3
    SECONDS = 6
    ALERT = defaultdict(dict)
    AUTOBAN = 10


async def check_bot_started_users(user, event):
    if user.id == OWNER_ID:
        return
    check = get_starter_details(user.id)
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"👤 {_format.mentionuser(user.first_name, user.id)} **{lan('botstartedme')}.**\
                \n**🆔 {lan('userx')} ID:** `{user.id}`\
                \n**ℹ️ {lan('namex')}:** {get_display_name(user)}"
    else:
        start_date = check.date
        notification = f"👤 {_format.mentionuser(user.first_name, user.id)} **{lan('botrestartedme')}.**\
                \n**🆔 {lan('userx')} ID:** `{user.id}`\
                \n**ℹ️ {lan('namex')}:** {get_display_name(user)}"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if PM_LOGGER_GROUP_ID != -100:
        await doge.tgbot.send_message(PM_LOGGER_GROUP_ID, notification)
    elif BOTLOG:
        await doge.tgbot.send_message(BOTLOG_CHATID, notification)


@doge.shiba_cmd(
    pattern=f"^/start({BOT_USERNAME})?([\s]+)?$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start(event):
    chat = await event.get_chat()
    user = await doge.get_me()
    if check_is_black_list(chat.id):
        return
    reply_to = await reply_id(event)
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    first = chat.first_name
    last = chat.last_name if chat.last_name else ""
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = user.first_name
    my_last = user.last_name if user.last_name else ""
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    if chat.id != OWNER_ID:
        customstrmsg = gvar("START_TEXT") or None
        if customstrmsg is not None:
            start_msg = customstrmsg.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            )
        else:
            start_msg = str(lan("botodefstartmsg").format(mention, my_mention))
        buttons = [
            (Button.url(f"📣 {lan('btnurlchannel')}", "https://t.me/DogeUserBot"),),
            (
                Button.url(f"💬 {lan('btnurlsup')}", "https://t.me/DogeSup"),
                Button.url(f"🧩 {lan('btnurlplugin')}", "https://t.me/DogePlugin"),
            ),
        ]
    else:
        start_msg = lan("botdefstartmsg").format(my_mention)
        buttons = [
            (Button.inline(f"🐕‍🦺 {lan('btnhelp')}", data="mainmenu"),),
        ]
    try:
        await event.client.send_message(
            chat.id,
            start_msg,
            link_preview=False,
            buttons=buttons,
            reply_to=reply_to,
        )
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"{lan('errr')}\n`ℹ️ {lan('errrstartbot')}.`\
                \n➡️ `{e}`",
            )
    else:
        await check_bot_started_users(chat, event)


@doge.shiba_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != OWNER_ID:
        msg = await event.forward_to(OWNER_ID)
        try:
            add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"{lan('errr')}\n`ℹ️ {lan('errrstoringmsg')}`\
                    \n➡️ `{str(e)}`",
                )
    else:
        if event.text.startswith("/"):
            return
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        users = get_user_id(reply_to)
        if users is None:
            return
        for usr in users:
            user_id = int(usr.chat_id)
            reply_msg = usr.reply_id
            user_name = usr.first_name
            break
        if user_id is not None:
            try:
                if event.media:
                    msg = await event.client.send_file(
                        user_id, event.media, caption=event.text, reply_to=reply_msg
                    )
                else:
                    msg = await event.client.send_message(
                        user_id, event.text, reply_to=reply_msg, link_preview=False
                    )
            except UserIsBlockedError:
                await doge(UnblockRequest(BOT_USERNAME))
                if event.media:
                    msg = await event.client.send_file(
                        user_id, event.media, caption=event.text, reply_to=reply_msg
                    )
                else:
                    msg = await event.client.send_message(
                        user_id, event.text, reply_to=reply_msg, link_preview=False
                    )
            except Exception as e:
                return await event.reply(f"{lan('errr')}\n➡️ `{e}`")
            try:
                add_user_to_db(
                    reply_to, user_name, user_id, reply_msg, event.id, msg.id
                )
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"{lan('errr')}\n`ℹ️ {lan('errrstoringmsg')}`\
                        \n➡️ `{e}`",
                    )


@doge.shiba_cmd(edited=True)
async def bot_pms_edit(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != OWNER_ID:
        users = get_user_reply(event.id)
        if users is None:
            return
        reply_msg = None
        for user in users:
            if user.chat_id == str(chat.id):
                reply_msg = user.message_id
                break
        if reply_msg:
            await event.client.send_message(
                OWNER_ID,
                lan("editedbotmsgbyuser").format(
                    _format.mentionuser(get_display_name(chat), chat.id)
                ),
                reply_to=reply_msg,
            )
            msg = await event.forward_to(OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"{lan('errr')}\n`ℹ️ {lan('errrstoringmsg')}`\
                        \n➡️ `{e}`",
                    )
    else:
        reply_to = await reply_id(event)
        if reply_to is not None:
            users = get_user_id(reply_to)
            result_id = 0
            if users is None:
                return
            for usr in users:
                if event.id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    reply_msg = usr.reply_id
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.edit_message(
                        user_id, result_id, event.text, file=event.media
                    )
                except Exception as e:
                    LOGS.error(str(e))


@doge.tgbot.on(MessageDeleted)
async def handler(event):
    for msg_id in event.deleted_ids:
        users_1 = get_user_reply(msg_id)
        users_2 = get_user_logging(msg_id)
        if users_2 is not None:
            result_id = 0
            for usr in users_2:
                if msg_id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.delete_messages(user_id, result_id)
                except Exception as e:
                    LOGS.error(str(e))
        if users_1 is not None:
            reply_msg = None
            for user in users_1:
                if user.chat_id != OWNER_ID:
                    reply_msg = user.message_id
                    break
            try:
                if reply_msg:
                    users = get_user_id(reply_msg)
                    for usr in users:
                        user_id = int(usr.chat_id)
                        user_name = usr.first_name
                        break
                    if check_is_black_list(user_id):
                        return
                    await event.client.send_message(
                        OWNER_ID,
                        lan("deletedbotmsgbyuser").format(
                            _format.mentionuser(user_name, user_id)
                        ),
                        reply_to=reply_msg,
                    )
            except Exception as e:
                LOGS.error(str(e))


@doge.shiba_cmd(pattern="^/uinfo$", from_users=OWNER_ID)
async def bot_start(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply(lan("replymsginfo"))
    info_msg = await event.client.send_message(
        event.chat_id,
        lan("search_db"),
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit(f"{lan('errr')}\n🙁 `{lan('errrfinduserdb')}.`")
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        break
    if user_id is None:
        return await info_msg.edit(f"{lan('errr')}\n🙁 `{lan('errrfinduserdb')}.`")
    uinfo = f"**👤 {lan('sentmsgby')}** {_format.mentionuser(user_name, user_id)}\
            \n**ℹ️ {lan('fnamex')}:** {user_name}\
            \n**🆔 {lan('userx')} ID:** `{user_id}`"
    await info_msg.edit(uinfo)


async def send_flood_alert(user_) -> None:
    # sourcery no-metrics
    buttons = [
        (
            Button.inline(f"🚫 {lan('btnban')}", data=f"bot_pm_ban_{user_.id}"),
            Button.inline(
                f"➖ {lan('btnafloodoff')}",
                data="toggle_bot-antiflood_off",
            ),
        )
    ]
    found = False
    if FloodConfig.ALERT and (user_.id in FloodConfig.ALERT.keys()):
        found = True
        try:
            FloodConfig.ALERT[user_.id]["count"] += 1
        except KeyError:
            found = False
            FloodConfig.ALERT[user_.id]["count"] = 1
        except Exception as e:
            if BOTLOG:
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"{lan('errr')}\nℹ️ {lan('errrupdateflood')}.\
                    \n➡️ `{e}`",
                )
        flood_count = FloodConfig.ALERT[user_.id]["count"]
    else:
        flood_count = FloodConfig.ALERT[user_.id]["count"] = 1

    flood_msg = (
        r"**⚠️️ #FLOOD_WARNING**"
        "\n\n"
        f"**🆔 {lan('userx')} ID:** `{user_.id}`\n"
        f"**ℹ️ {lan('namex')}:** {get_display_name(user_)}\n"
        f"**👤 {lan('userx')}:** {_format.mentionuser(get_display_name(user_), user_.id)}"
        f"\n\n**🐾 {lan('wrnnspammingbot').format(BOT_USERNAME, flood_count)}**\n"
        f"__💡 {lan('botquickaction')}__: {lan('botquickaction_')}."
    )

    if found:
        if flood_count >= FloodConfig.AUTOBAN:
            if user_.id in Config.SUDO_USERS:
                sudo_spam = (
                    f"**👤 Sudo {lan('userx')}** {_format.mentionuser(user_.first_name, user_.id)}\
                    \n**🆔 {lan('userx')} ID:** `{user_.id}`\n\n"
                    f"**🐾 {lan('wrnnfloodingbot').format(BOT_USERNAME)}**\
                    \n\nℹ️ {lan('infomsgrmsudo').format(tr)}"
                )
                if BOTLOG:
                    await doge.tgbot.send_message(BOTLOG_CHATID, sudo_spam)
            else:
                await ban_user_from_bot(
                    user_,
                    f"**⛔ {lan('banuserfbot').format(BOT_USERNAME, FloodConfig.AUTOBAN)}**",
                )
                FloodConfig.USERS[user_.id].clear()
                FloodConfig.ALERT[user_.id].clear()
                FloodConfig.BANNED_USERS.remove(user_.id)
            return
        fa_id = FloodConfig.ALERT[user_.id].get("fa_id")
        if not fa_id:
            return
        try:
            msg_ = await doge.tgbot.get_messages(BOTLOG_CHATID, fa_id)
            if msg_.text != flood_msg:
                await msg_.edit(flood_msg, buttons=buttons)
        except Exception as fa_id_err:
            LOGS.debug(fa_id_err)
            return
    else:
        if BOTLOG:
            fa_msg = await doge.tgbot.send_message(
                BOTLOG_CHATID,
                flood_msg,
                buttons=buttons,
            )
        try:
            chat = await doge.tgbot.get_entity(BOTLOG_CHATID)
            await doge.tgbot.send_message(
                OWNER_ID,
                f"**⚠️️ [{BOT_USERNAME} {lan('wrnnfloodwbot')}](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
        except UserIsBlockedError:
            await doge(UnblockRequest(BOT_USERNAME))
            chat = await doge.tgbot.get_entity(BOTLOG_CHATID)
            await doge.tgbot.send_message(
                OWNER_ID,
                f"**⚠️️ [{BOT_USERNAME} {lan('wrnnfloodwbot')}](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
    if FloodConfig.ALERT[user_.id].get("fa_id") is None and fa_msg:
        FloodConfig.ALERT[user_.id]["fa_id"] = fa_msg.id


@doge.tgbot.on(CallbackQuery(data=compile(b"bot_pm_ban_([0-9]+)")))
@check_owner
async def bot_pm_ban_cb(c_q: CallbackQuery):
    user_id = int(c_q.pattern_match.group(1))
    try:
        user = await doge.get_entity(user_id)
    except Exception as e:
        await c_q.answer(f"{lan('errr')}\n➡️ `{e}`")
    else:
        await c_q.answer(
            f"**⏳ {lan('userx')} ID {lan('banning')} ->** `{user_id}`**...**",
            alert=False,
        )
        await ban_user_from_bot(user, "Spamming Bot")
        await c_q.edit(f"**✅ {lan('banned')}\n🆔 {lan('userx')} ID:** `{user_id}`")


def time_now() -> Union[float, int]:
    return datetime.timestamp(datetime.now())


@pool.run_in_thread
def is_flood(uid: int) -> Optional[bool]:
    """Checks if a user is flooding"""
    FloodConfig.USERS[uid].append(time_now())
    if (
        len(
            list(
                filter(
                    lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                    FloodConfig.USERS[uid],
                )
            )
        )
        > FloodConfig.MESSAGES
    ):
        FloodConfig.USERS[uid] = list(
            filter(
                lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                FloodConfig.USERS[uid],
            )
        )
        return True


@doge.tgbot.on(CallbackQuery(data=compile(b"toggle_bot-antiflood_off$")))
@check_owner
async def settings_toggle(c_q: CallbackQuery):
    if gvar("bot_antif") is None:
        return await c_q.answer(lan("alreadyaflooddsb"), alert=False)
    dgvar("bot_antif")
    await c_q.answer(lan("aflooddisabled"), alert=False)
    await c_q.edit(lan("aflooddisabled"))


@doge.shiba_cmd(incoming=True, func=lambda e: e.is_private)
@doge.shiba_cmd(edited=True, func=lambda e: e.is_private)
async def antif_on_msg(event):
    if gvar("bot_antif") is None:
        return
    chat = await event.get_chat()
    if chat.id == OWNER_ID:
        return
    user_id = chat.id
    if check_is_black_list(user_id):
        raise StopPropagation
    if await is_flood(user_id):
        await send_flood_alert(chat)
        FloodConfig.BANNED_USERS.add(user_id)
        raise StopPropagation
    if user_id in FloodConfig.BANNED_USERS:
        FloodConfig.BANNED_USERS.remove(user_id)
