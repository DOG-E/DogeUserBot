# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from collections import defaultdict
from datetime import datetime
from re import compile
from typing import Optional, Union

from telethon import Button
from telethon.errors import UserIsBlockedError
from telethon.events import CallbackQuery, MessageDeleted, StopPropagation
from telethon.tl.functions.contacts import UnblockRequest
from telethon.utils import get_display_name

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
        notification = f"👤 {_format.mentionuser(user.first_name, user.id)} **Beni başlattı.**\
                \n**🆔  Kullanıcı ID'is:** `{user.id}`\
                \n**ℹ️ İsim:** {get_display_name(user)}"
    else:
        start_date = check.date
        notification = f"👤 {_format.mentionuser(user.first_name, user.id)} **has restarted me.**\
                \n**🆔 Kullanıcı ID'si:** `{user.id}`\
                \n**ℹ️ İsim:** {get_display_name(user)}"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    if PM_LOGGER_GROUP_ID != -100:
        await doge.bot.send_message(PM_LOGGER_GROUP_ID, notification)
    elif BOTLOG:
        await doge.bot.send_message(BOTLOG_CHATID, notification)


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
            start_msg = str(
                "**🐶 Wow!**\
            \n🐾 Selam {}!\n\
            \n**🐶 Ben {}'in sadık köpeğiyim.**\
            \n💭 Ustamla buradan iletişime geçebilirsiniz.".format(
                    mention, my_mention
                )
            )
        buttons = [
            (Button.url(f"📣 Kᴀɴᴀʟ ", "https://t.me/DogeUserBot"),),
            (
                Button.url(f"💬 Sᴜᴘᴘᴏʀᴛ ", "https://t.me/DogeSup"),
                Button.url(f"🧩 Pʟᴜɢɪɴ ", "https://t.me/DogePlugin"),
            ),
        ]
    else:
        start_msg = "**🐶 Wow!\
        \n🐾 Merhaba {}!\n\
        \n💬 Sana nasıl yardımcı olabilirim?**".format(
            my_mention
        )
        buttons = [
            (Button.inline(f"🐕‍🦺 ʏᴀʀᴅɪᴍ", data="mainmenu"),),
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
                f"**🚨 Hᴀᴛᴀ:**\n`ℹ️ Kullanıcı botunuzu başlatırken bir hata oluştu.`\
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
            LOGS.error(f"🚨 {str(e)}")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**🚨 Hᴀᴛᴀ:**\n`ℹ️ Mesaj detaylarını veritabanında saklarken bir hata oluştu.`\
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
                return await event.reply(f"**🚨 Hᴀᴛᴀ:**\n➡️ `{e}`")
            try:
                add_user_to_db(
                    reply_to, user_name, user_id, reply_msg, event.id, msg.id
                )
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**🚨 Hᴀᴛᴀ:**\n`ℹ️ Mesaj detaylarını veritabanında saklarken bir hata oluştu.`\
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
                "**⬆️ Bu mesaj şu kullanıcı tarafından düzenlendi.** {} :\n".format(
                    _format.mentionuser(get_display_name(chat), chat.id)
                ),
                reply_to=reply_msg,
            )
            msg = await event.forward_to(OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**🚨 Hᴀᴛᴀ:**\n__ℹ️ Mesaj detaylarını veritabanında saklarken bir hata oluştu.__\
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
                    LOGS.error(f"🚨 {str(e)}")


@doge.bot.on(MessageDeleted)
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
                    LOGS.error(f"🚨 {str(e)}")
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
                        "**⬆️ Bu mesaj, şu kullanıcı tarafından silindi.** {}.".format(
                            _format.mentionuser(user_name, user_id)
                        ),
                        reply_to=reply_msg,
                    )
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")


@doge.shiba_cmd(pattern="^/uinfo$", from_users=OWNER_ID)
async def bot_start(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply(
            "**ℹ️ Mesaj bilgisi almak için bir mesajı yanıtlayın.**"
        )
    info_msg = await event.client.send_message(
        event.chat_id,
        "`🔎 Bu kullanıcıyı veritabanımda arıyorum...`",
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit(
            f"**🚨 Hᴀᴛᴀ:**\n🙁 'Üzgünüm! Bu kullanıcıyı veritabanımda bulamadım.`"
        )
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        break
    if user_id is None:
        return await info_msg.edit(
            f"**🚨 Hᴀᴛᴀ:**\n🙁 'Üzgünüm! Bu kullanıcıyı veritabanımda bulamadım.`"
        )
    uinfo = f"**👤 Bu mesaj şu kişi tarafından gönderildi:** {_format.mentionuser(user_name, user_id)}\
            \n**ℹ️ Kullanıcı İsmi:** {user_name}\
            \n**🆔 Kullanıcı ID'si:** `{user_id}`"
    await info_msg.edit(uinfo)


async def send_flood_alert(user_) -> None:
    # sourcery no-metrics
    buttons = [
        (
            Button.inline(f"🚫 Bᴀɴ", data=f"bot_pm_ban_{user_.id}"),
            Button.inline(
                f"➖ Boᴛ AɴᴛɪFʟooᴅ'ᴜ Kᴀᴘᴀᴛ",
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
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    f"**🚨 Hᴀᴛᴀ:**\nℹ️ Flood sayısı güncellenirken hata oluştu.\
                    \n➡️ `{e}`",
                )
        flood_count = FloodConfig.ALERT[user_.id]["count"]
    else:
        flood_count = FloodConfig.ALERT[user_.id]["count"] = 1

    flood_msg = (
        r"**⚠️️ #FLOOD_WARNING**"
        "\n\n"
        f"**🆔 Kullanıcı ID'si:** `{user_.id}`\n"
        f"**ℹ️ İsim:** {get_display_name(user_)}\n"
        f"**👤 Kullanıcı:** {_format.mentionuser(get_display_name(user_), user_.id)}"
        f"\n\n**🐾 Botunuz {BOT_USERNAME}'da spam yapıyor! -> [ Flood Atılan Mesajlar ({flood_count}) ]**\n"
        f"__💡 Hızlı Eylem__: Kullanıcı bir süreliğine bot tarafından göz ardı edildi."
    )

    if found:
        if flood_count >= FloodConfig.AUTOBAN:
            if user_.id in Config.SUDO_USERS:
                sudo_spam = (
                    f"**👤 Sudo Kullanıcı** {_format.mentionuser(user_.first_name, user_.id)}\
                    \n**🆔 Kullanıcı ID'si:** `{user_.id}`\n\n"
                    f"**🐾 Botunuz {BOT_USERNAME}'da spam yapıyor!**\
                    \n\nℹ️ `{tr}doge rmsudo` komutunu kontrol edin. İsterseniz bu kullanıcıyı __Sudo Kullanıcılar__'dan kaldırabilirsiniz."
                )
                if BOTLOG:
                    await doge.bot.send_message(BOTLOG_CHATID, sudo_spam)
            else:
                await ban_user_from_bot(
                    user_,
                    f"**⛔Yapılan Flood {BOT_USERNAME} tarafından otomatik oalrak engellendi.[Flood sınırı aşıldı: ({FloodConfig.AUTOBAN})]**",
                )
                FloodConfig.USERS[user_.id].clear()
                FloodConfig.ALERT[user_.id].clear()
                FloodConfig.BANNED_USERS.remove(user_.id)
            return
        fa_id = FloodConfig.ALERT[user_.id].get("fa_id")
        if not fa_id:
            return
        try:
            msg_ = await doge.bot.get_messages(BOTLOG_CHATID, fa_id)
            if msg_.text != flood_msg:
                await msg_.edit(flood_msg, buttons=buttons)
        except Exception as fa_id_err:
            LOGS.debug(fa_id_err)
            return
    else:
        if BOTLOG:
            fa_msg = await doge.bot.send_message(
                BOTLOG_CHATID,
                flood_msg,
                buttons=buttons,
            )
        try:
            chat = await doge.bot.get_entity(BOTLOG_CHATID)
            await doge.bot.send_message(
                OWNER_ID,
                f"**⚠️️ [{BOT_USERNAME} Flood Uyarısı!](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
        except UserIsBlockedError:
            await doge(UnblockRequest(BOT_USERNAME))
            chat = await doge.bot.get_entity(BOTLOG_CHATID)
            await doge.bot.send_message(
                OWNER_ID,
                f"**⚠️️ [{BOT_USERNAME} Flood Uyarısı!](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
    if FloodConfig.ALERT[user_.id].get("fa_id") is None and fa_msg:
        FloodConfig.ALERT[user_.id]["fa_id"] = fa_msg.id


@doge.bot.on(CallbackQuery(data=compile(b"bot_pm_ban_([0-9]+)")))
@check_owner
async def bot_pm_ban_cb(c_q: CallbackQuery):
    user_id = int(c_q.pattern_match.group(1))
    try:
        user = await doge.get_entity(user_id)
    except Exception as e:
        await c_q.answer(f"**🚨 Hᴀᴛᴀ:**\n➡️ `{e}`")
    else:
        await c_q.answer(
            f"*__⏳ Kullanıcı yasaklanıyor...__ **-> Kullanıcı ID'si:** `{user_id}`",
            alert=False,
        )
        await ban_user_from_bot(user, "Spamming Bot")
        await c_q.edit(f"**✅ Yasaklandı!\n🆔 Kullanıcı ID'si:** `{user_id}`")


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


@doge.bot.on(CallbackQuery(data=compile(b"toggle_bot-antiflood_off$")))
@check_owner
async def settings_toggle(c_q: CallbackQuery):
    if gvar("bot_antif") is None:
        return await c_q.answer("**ℹ️ Bot AntiFlood'u zaten kapalı.**", alert=False)
    dgvar("bot_antif")
    await c_q.answer("**ℹ️ Bot AntiFlood'u devre dışı bırakıldı.**", alert=False)
    await c_q.edit("**ℹ️ Bot AntiFlood'u devre dışı bırakıldı.**")


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
