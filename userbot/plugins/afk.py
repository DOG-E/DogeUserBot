# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from os import remove
from random import randint
from time import time

from telethon.events import NewMessage, StopPropagation
from telethon.tl.custom.button import Button
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from ..sql_helper.global_msg import gmsg
from ..sql_helper.no_log_pms_sql import is_approved
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    DOGEAFK,
    PM_LOGGER_GROUP_ID,
    _format,
    afk_time,
    dgvar,
    doge,
    edl,
    gvar,
    logging,
    media_type,
    sgvar,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

CMSG = {}
MSG = {"AFK": f"{DOGEAFK}"}
for msg in ["AFK"]:
    delmsg = gmsg(msg)
    if delmsg == False:
        CMSG[msg] = MSG[msg]
    else:
        if delmsg.startswith("MEDIA_"):
            md = int(delmsg.split("MEDIA_")[1])
            md = doge.get_messages(int(gvar("PLUGIN_CHANNEL")), ids=md)
            CMSG[msg] = md
        else:
            CMSG[msg] = delmsg

AFKREASON = None
AFKMEDIA = None
COUNT_MSG = 0
USERS = {}
LAST_SEEN = 0


@doge.bot_cmd(
    pattern="afk(?:\s|$)([\s\S]*)",
    command=("afk", plugin_category),
    info={
        "h": "AFK olduğunuzu belirtir.",
        "d": "AFK'dayken, eğer biri sizi etiketlerse, Doge sizin için cevap verecektir. AFK, 'klavyeden uzaktayım, şu an burada değilim' anlamına gelir.",
        "u": [
            "{tr}afk <sebep>",
            "{tr}afk <yanıt>",
        ],
        "e": "{tr}afk Uyuyorum",
        "note": "Herhangi bir sohbete bir şey yazdığınızda AFK'dan çıkarsınız. AFK'dan çıkmadan sohbete devam etmek için mesajınıza #afk yazabilirsiniz.",
    },
)
async def set_afk(event):
    "AFK olduğunuzu belirtir."
    if gvar("ISAFK") == "True":
        return

    string = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    media_t = media_type(reply)
    global AFKREASON
    global AFKMEDIA
    global LAST_SEEN
    if gvar("ISAFK") is None:
        if not media_t:
            AFKMEDIA = None
        elif media_t != "Sticker" and media_t:
            if not BOTLOG:
                return await edl(
                    event,
                    "Medya ile birlikte AFK kullanmak için `PRIVATE_GROUP_BOT_API_ID` değişkenini ayarlamalısınız.",
                )
            AFKMEDIA = await reply.forward_to(BOTLOG_CHATID)
        if string:
            AFKREASON = string
            await edl(event, f"`AFK'yım!`\n**Nedeni:** {string}")
        else:
            await edl(event, "`AFK'yım!`")
        LAST_SEEN = time()
        if gvar("AFKBIOSET") != "False":
            try:
                full = await event.client(GetFullUserRequest(int(gvar("OWNER_ID"))))
                bio = full.about
                if bio:
                    sgvar("AFKBIO", bio)
                    await event.client(
                        UpdateProfileRequest(about=f"{gvar('AFK_BIO')} @DogeUserBot")
                    )
                else:
                    await event.client(
                        UpdateProfileRequest(about="🐶 @DogeUserBot sadık köpeğiniz! 🐾")
                    )
            except BaseException:
                pass
        if BOTLOG:
            if string:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFK\nAFK modundasınız.\n**Nedeni:** `{string}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#AFK\nAFK modundasınız.\nNedenini belirtmediniz.",
                )
        sgvar("ISAFK", "True")
        raise StopPropagation


async def mention_afk(mention):
    global LAST_SEEN
    global USERS
    global COUNT_MSG
    if "afk" in mention.text.lower():
        return

    if mention.message.mentioned and not (await mention.get_sender()).bot:
        from_user = await mention.get_sender()
        if from_user.username:
            username = "@" + from_user.username
        else:
            if from_user.last_name:
                username = f"[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})"
            else:
                username = f"[{from_user.first_name}](tg://user?id={from_user.id})"
        mention_format = f"[{from_user.first_name}](tg://user?id={from_user.id})"
        first_name = from_user.first_name
        if from_user.last_name:
            last_name = from_user.last_name
        else:
            last_name = ""
        last_seen_seconds = round(time() - LAST_SEEN)
        last_seen = afk_time(last_seen_seconds)
        last_seen_long = afk_time(last_seen_seconds, False)
        if mention.sender_id not in USERS:
            if AFKREASON:
                if type(CMSG["AFK"]) is str:
                    afkmsg = (
                        CMSG["AFK"].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        + f"\n\n**🐾 Nedeni:** {AFKREASON}"
                    )
                    if AFKMEDIA is None:
                        await mention.reply(afkmsg)
                    elif AFKMEDIA:
                        await mention.reply(afkmsg, file=AFKMEDIA.media)
                else:
                    afkmsg = await mention.reply(CMSG["AFK"])
                    if AFKMEDIA is None:
                        await afkmsg.reply(f"**🐾 Nedeni:** {AFKREASON}")
                    elif AFKMEDIA:
                        await afkmsg.reply(
                            f"**🐾 Nedeni:** {AFKREASON}", file=AFKMEDIA.media
                        )
            else:
                if not isinstance(CMSG["AFK"], str):
                    CMSG["AFK"].text = CMSG["AFK"].text.format(
                        username=username,
                        mention=mention_format,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long,
                    )
                    afkmsg = CMSG["AFK"]
                    if AFKMEDIA is None:
                        await mention.reply(afkmsg)
                    elif AFKMEDIA:
                        await mention.reply(afkmsg, file=AFKMEDIA.media)
                else:
                    afkmsg = CMSG["AFK"].format(
                        username=username,
                        mention=mention_format,
                        first_name=first_name,
                        last_name=last_name,
                        last_seen_seconds=last_seen_seconds,
                        last_seen=last_seen,
                        last_seen_long=last_seen_long,
                    )
                    if AFKMEDIA is None:
                        await mention.reply(afkmsg)
                    elif AFKMEDIA:
                        await mention.reply(afkmsg, file=AFKMEDIA.media)
            USERS.update({mention.sender_id: 1})
            COUNT_MSG = COUNT_MSG + 1
        elif mention.sender_id in USERS:
            if USERS[mention.sender_id] % randint(2, 4) == 0:
                if AFKREASON:
                    if CMSG["AFK"] is str:
                        afkmsg = (
                            CMSG["AFK"].format(
                                username=username,
                                mention=mention_format,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long,
                            )
                            + f"\n\n**🐾 Nedeni:** {AFKREASON}"
                        )
                        if AFKMEDIA is None:
                            await mention.reply(afkmsg)
                        elif AFKMEDIA:
                            await mention.reply(afkmsg, file=AFKMEDIA.media)
                    else:
                        afkmsg = await mention.reply(CMSG["AFK"])
                        if AFKMEDIA is None:
                            await afkmsg.reply(f"**🐾 Nedeni:** {AFKREASON}")
                        elif AFKMEDIA:
                            await afkmsg.reply(
                                f"**🐾 Nedeni:** {AFKREASON}", file=AFKMEDIA.media
                            )
                else:
                    if not isinstance(CMSG["AFK"], str):
                        CMSG["AFK"].text = CMSG["AFK"].text.format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        afkmsg = CMSG["AFK"]
                        if AFKMEDIA is None:
                            await mention.reply(afkmsg)
                        elif AFKMEDIA:
                            await mention.reply(afkmsg, file=AFKMEDIA.media)
                    else:
                        afkmsg = CMSG["AFK"].format(
                            username=username,
                            mention=mention_format,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        if AFKMEDIA is None:
                            await mention.reply(afkmsg)
                        elif AFKMEDIA:
                            await mention.reply(afkmsg, file=AFKMEDIA.media)
                USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                COUNT_MSG = COUNT_MSG + 1
            else:
                USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                COUNT_MSG = COUNT_MSG + 1
        hmm = await mention.get_chat()
        if PM_LOGGER_GROUP_ID == -100:
            return
        full = None
        try:
            full = await mention.client.get_entity(mention.message.from_id)
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
        messaget = media_type(mention)
        resalt = f"💤 #AFK_TAG\n<b>👥 Grup: {hmm.title}</b>"
        if full is not None:
            resalt += f"\n<b>👤 Kimden: </b>{_format.htmlmentionuser(full.first_name, full.id)}"
        if messaget is not None:
            resalt += f"\n<b>🔅 Mesaj Türü: </b>{messaget}"
        else:
            resalt += f"\n<b>🔹 Mesaj: </b><code>{mention.message.message}</code>"
        button = [
            (Button.url("👁‍🗨 Mᴇsᴀᴊ", f"https://t.me/c/{hmm.id}/{mention.message.id}"))
        ]
        if not mention.is_private:
            if messaget is None:
                await doge.bot.send_message(
                    PM_LOGGER_GROUP_ID,
                    resalt,
                    parse_mode="html",
                    link_preview=False,
                    buttons=button,
                )
            else:
                try:
                    media = await mention.download_media()
                    await doge.bot.send_message(
                        PM_LOGGER_GROUP_ID,
                        resalt,
                        parse_mode="html",
                        link_preview=False,
                        file=media,
                        buttons=button,
                    )
                    if messaget == "Sticker":
                        await doge.bot.send_message(
                            PM_LOGGER_GROUP_ID,
                            resalt,
                            parse_mode="html",
                            link_preview=False,
                            buttons=button,
                        )
                    return remove(media)
                except Exception as er:
                    LOGS.error(er)


async def pm_afk(sender):
    global USERS
    global COUNT_MSG
    if "afk" in sender.text.lower():
        return

    if (
        sender.is_private
        and sender.sender_id != 777000
        and not (await sender.get_sender()).bot
    ):
        try:
            apprv = is_approved(sender.sender_id)
        except AttributeError:
            apprv = True
        else:
            apprv = True
        from_user = await sender.get_sender()
        if from_user.username:
            username = "@" + from_user.username
        else:
            if from_user.last_name:
                username = f"[{from_user.first_name} {from_user.last_name}](tg://user?id={from_user.id})"
            else:
                username = f"[{from_user.first_name}](tg://user?id={from_user.id})"
        mention = f"[{from_user.first_name}](tg://user?id={from_user.id})"
        first_name = from_user.first_name
        if from_user.last_name:
            last_name = from_user.last_name
        else:
            last_name = ""
        last_seen_seconds = round(time() - LAST_SEEN)
        last_seen = afk_time(last_seen_seconds)
        last_seen_long = afk_time(last_seen_seconds, False)
        if apprv:
            if sender.sender_id not in USERS:
                if AFKREASON:
                    afkmsg = (
                        CMSG["AFK"].format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        + f"\n\n**🐾 Nedeni:** {AFKREASON}"
                    )
                    if AFKMEDIA is None:
                        await sender.reply(afkmsg)
                    elif AFKMEDIA:
                        await sender.reply(afkmsg, file=AFKMEDIA.media)
                else:
                    if not isinstance(CMSG["AFK"], str):
                        CMSG["AFK"].text = CMSG["AFK"].text.format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        afkmsg = CMSG["AFK"]
                        if AFKMEDIA is None:
                            await sender.reply(afkmsg)
                        elif AFKMEDIA:
                            await sender.reply(afkmsg, file=AFKMEDIA.media)
                    else:
                        afkmsg = CMSG["AFK"].format(
                            username=username,
                            mention=mention,
                            first_name=first_name,
                            last_name=last_name,
                            last_seen_seconds=last_seen_seconds,
                            last_seen=last_seen,
                            last_seen_long=last_seen_long,
                        )
                        if AFKMEDIA is None:
                            await sender.reply(afkmsg)
                        elif AFKMEDIA:
                            await sender.reply(afkmsg, file=AFKMEDIA.media)
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        if type(CMSG["AFK"]) is str:
                            afkmsg = (
                                CMSG["AFK"].format(
                                    username=username,
                                    mention=mention,
                                    first_name=first_name,
                                    last_name=last_name,
                                    last_seen_seconds=last_seen_seconds,
                                    last_seen=last_seen,
                                    last_seen_long=last_seen_long,
                                )
                                + f"\n\n**🐾 Nedeni:** {AFKREASON}"
                            )
                            if AFKMEDIA is None:
                                await sender.reply(afkmsg)
                            elif AFKMEDIA:
                                await sender.reply(afkmsg, file=AFKMEDIA.media)
                        else:
                            afkmsg = await sender.reply(CMSG["AFK"])
                            if AFKMEDIA is None:
                                await afkmsg.reply(f"**🐾 Nedeni:** {AFKREASON}")
                            elif AFKMEDIA:
                                await afkmsg.reply(
                                    f"**🐾 Nedeni:** {AFKREASON}", file=AFKMEDIA.media
                                )
                    else:
                        if not isinstance(CMSG["AFK"], str):
                            CMSG["AFK"].text = CMSG["AFK"].text.format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long,
                            )
                            afkmsg = CMSG["AFK"]
                            if AFKMEDIA is None:
                                await sender.reply(afkmsg)
                            elif AFKMEDIA:
                                await sender.reply(afkmsg, file=AFKMEDIA.media)
                        else:
                            afkmsg = CMSG["AFK"].format(
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name,
                                last_seen_seconds=last_seen_seconds,
                                last_seen=last_seen,
                                last_seen_long=last_seen_long,
                            )
                            if AFKMEDIA is None:
                                await sender.reply(afkmsg)
                            elif AFKMEDIA:
                                await sender.reply(afkmsg, file=AFKMEDIA.media)
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


async def setnot_afk(notafk):
    global COUNT_MSG
    global USERS
    global AFKMEDIA
    global AFKREASON
    global LAST_SEEN
    if "afk" in notafk.text.lower():
        return

    dgvar("ISAFK")
    endtime_seconds = round(time() - LAST_SEEN)
    endtime = afk_time(endtime_seconds, False)
    await notafk.respond(
        "Artık AFK değilim.\n\nŞu kadar süredir AFK'yım: `" + endtime + "`"
    )
    await sleep(2)
    if gvar("AFKBIOSET") != "False":
        try:
            await notafk.client(UpdateProfileRequest(about=f"{gvar('AFKBIO')}"))
        except Exception:
            pass
    if BOTLOG:
        await notafk.client.send_message(
            BOTLOG_CHATID,
            "AFK'dan çıktınız.\n\n"
            + "Şu kadar süredir AFK'ydınız: `"
            + endtime
            + "`"
            + "Siz AFK iken **"
            + str(len(USERS))
            + "** kullanıcı **"
            + str(COUNT_MSG)
            + "** mesaj gönderdi.",
        )
    COUNT_MSG = 0
    USERS = {}
    AFKMEDIA = None
    AFKREASON = None
    LAST_SEEN = 0


if gvar("ISAFK") == "True":
    doge.add_event_handler(setnot_afk, NewMessage(outgoing=True, edited=False))
    doge.add_event_handler(
        mention_afk, NewMessage(incoming=True, func=lambda e: e.mentioned, edited=False)
    )
    doge.add_event_handler(
        pm_afk, NewMessage(incoming=True, func=lambda e: e.is_private, edited=False)
    )
