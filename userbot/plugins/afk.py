# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from datetime import datetime

from telethon import Button
from telethon.tl.functions.account import GetPrivacyRequest, UpdateProfileRequest
from telethon.tl.types import InputPrivacyKeyStatusTimestamp, PrivacyValueAllowAll

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    DOGEAFK,
    PM_LOGGER_GROUP_ID,
    _format,
    doge,
    edl,
    gvar,
    logging,
    media_type,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)


class AFK:
    def __init__(self):
        self.USERAFK_ON = {}
        self.afk_time = None
        self.last_afk_message = {}
        self.afk_star = {}
        self.afk_end = {}
        self.reason = None
        self.msg_link = False
        self.afk_type = None
        self.media_afk = None
        self.afk_on = False


AFK_ = AFK()


@doge.bot_cmd(
    pattern="afk(?:\s|$)([\s\S]*)",
    command=("afk", plugin_category),
    info={
        "h": "Enables afk for your account",
        "d": "When you're in afk if any one tags you then your bot will reply as he is offline.\
        AFK mean away from keyboard.",
        "o": "If you want AFK reason with hyperlink use [ ; ] after reason, then paste the media link.",
        "u": [
            "{tr}afk <reason>",
            "{tr}afk <reason> ; <link>",
            "{tr}afk <reply>",
        ],
        "e": "{tr}afk Let Me Sleep",
        "note": "Switches off AFK when you type back anything, anywhere. You can use #afk in message to continue in afk without breaking it",
    },
)
async def afksetter(event):
    "To mark yourself as afk i.e. Away from keyboard"
    reply = await event.get_reply_message()
    media_t = media_type(reply)
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    start_1 = datetime.now()
    AFK_.afk_on = True
    AFK_.afk_star = start_1.replace(microsecond=0)
    if not media_t:
        AFK_.afk_type = "text"
        if not AFK_.USERAFK_ON:
            input_str = event.pattern_match.group(1)
            if ";" in input_str:
                msg, mlink = input_str.split(";", 1)
                AFK_.reason = f"[{msg.strip()}]({mlink.strip()})"
                AFK_.msg_link = True
            else:
                AFK_.reason = input_str
                AFK_.msg_link = False
            last_seen_status = await event.client(
                GetPrivacyRequest(InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, PrivacyValueAllowAll):
                AFK_.afk_time = datetime.now()
            AFK_.USERAFK_ON = f"on: {AFK_.reason}"
            if gvar("AFKBIO"):
                try:
                    await event.client(UpdateProfileRequest(about=f"{gvar('AFKBIO')}"))
                except BaseException:
                    pass
            if AFK_.reason:
                await edl(event, f"`I'm going afk! because ~` {AFK_.reason}", 5)
            else:
                await edl(event, "`I'm going afk! `", 5)
            if BOTLOG:
                if AFK_.reason:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"#AFKTRUE \nSet AFK mode to True, and Reason is {AFK_.reason}",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#AFKTRUE \nSet AFK mode to True, and Reason is Not Mentioned",
                    )
    elif media_t != "Sticker" and media_t:
        if not BOTLOG:
            return await edl(
                event,
                "`To use media afk you need to set PRIVATE_GROUP_BOT_API_ID config`",
            )

        AFK_.media_afk = None
        AFK_.afk_type = "media"
        if not AFK_.USERAFK_ON:
            input_str = event.pattern_match.group(1)
            AFK_.reason = input_str
            last_seen_status = await event.client(
                GetPrivacyRequest(InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, PrivacyValueAllowAll):
                AFK_.afk_time = datetime.now()
            AFK_.USERAFK_ON = f"on: {AFK_.reason}"
            if gvar("AFKBIO"):
                try:
                    await event.client(UpdateProfileRequest(about=f"{gvar('AFKBIO')}"))
                except BaseException:
                    pass
            if AFK_.reason:
                await edl(event, f"`I'm going afk! because ~` {AFK_.reason}", 5)
            else:
                await edl(event, "`I'm going afk! `", 5)
            AFK_.media_afk = await reply.forward_to(BOTLOG_CHATID)
            if AFK_.reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \nSet AFK mode to True, and Reason is {AFK_.reason}",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#AFKTRUE \nSet AFK mode to True, and Reason is Not Mentioned",
                )


@doge.bot_cmd(outgoing=True, edited=False)
async def set_not_afk(event):
    if AFK_.afk_on is False:
        return
    back_alive = datetime.now()
    AFK_.afk_end = back_alive.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        elif h > 0:
            endtime += f"{h}h {m}m {s}s"
        else:
            endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message = event.message.message
    if (("afk" not in current_message) or ("#afk" not in current_message)) and (
        "on" in AFK_.USERAFK_ON
    ):
        if gvar("AFKRBIO"):
            try:
                await event.client(UpdateProfileRequest(about=f"{gvar('AFKRBIO')}"))
            except BaseException:
                pass
        shite = await event.client.send_message(
            event.chat_id,
            "`Back alive! No Longer afk.\nWas afk for " + endtime + "`",
        )
        AFK_.USERAFK_ON = {}
        AFK_.afk_time = None
        await sleep(5)
        await shite.delete()
        AFK_.afk_on = False
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#AFKFALSE \n`Set AFK mode to False\n"
                + "Back alive! No Longer afk.\nWas afk for "
                + endtime
                + "`",
            )


@doge.bot_cmd(
    incoming=True, func=lambda e: bool(e.mentioned or e.is_private), edited=False
)
async def on_afk(event):  # sourcery no-metrics
    if AFK_.afk_on is False:
        return
    back_alivee = datetime.now()
    AFK_.afk_end = back_alivee.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        elif h > 0:
            endtime += f"{h}h {m}m {s}s"
        else:
            endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text or "#afk" in current_message_text:
        return False
    if not await event.get_sender():
        return
    if AFK_.USERAFK_ON and not (
        (await event.get_sender()).bot or (await event.get_sender()).verified
    ):
        msg = None
        user = None
        try:
            user = await event.client.get_entity(event.message.from_id)
        except Exception as e:
            LOGS.info(str(e))
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        first = user.first_name
        last = user.last_name if user.last_name else ""
        fullname = f"{first} {last}" if last else first
        username = f"@{user.username}" if user.username else mention
        me = await event.client.get_me()
        my_mention = f"[{me.first_name}](tg://user?id={me.id})"
        my_first = me.first_name
        my_last = me.last_name if me.last_name else ""
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        customafkmsg = gvar("AFK") or None
        if customafkmsg is not None:
            if AFK_.reason:
                dogerafk = (
                    customafkmsg.format(
                        mention=mention,
                        first=first,
                        last=last,
                        fullname=fullname,
                        username=username,
                        my_mention=my_mention,
                        my_first=my_first,
                        my_last=my_last,
                        my_fullname=my_fullname,
                        my_username=my_username,
                        afktime=endtime,
                    )
                    + f"\n\n**🐾 Reason:** {AFK_.reason}"
                )
            else:
                dogeafk = customafkmsg.format(
                    mention=mention,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    my_mention=my_mention,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    afktime=endtime,
                )
        else:
            if AFK_.reason:
                dogerafk = DOGEAFK + f"\n\n**🐾 Reason:** {AFK_.reason}"
            else:
                dogeafk = DOGEAFK

        if AFK_.afk_type == "media":
            if AFK_.reason:
                message_to_reply = dogerafk
            else:
                message_to_reply = dogeafk
            if event.chat_id:
                msg = await event.reply(message_to_reply, file=AFK_.media_afk.media)
        elif AFK_.afk_type == "text":
            if AFK_.msg_link and AFK_.reason:
                message_to_reply = dogerafk
            elif AFK_.reason:
                message_to_reply = dogerafk
            else:
                message_to_reply = dogeafk
            if event.chat_id:
                msg = await event.reply(message_to_reply)
        if event.chat_id in AFK_.last_afk_message:
            await AFK_.last_afk_message[event.chat_id].delete()
        AFK_.last_afk_message[event.chat_id] = msg
        if event.is_private:
            return
        hmm = await event.get_chat()
        if PM_LOGGER_GROUP_ID == -100:
            return
        full = None
        try:
            full = await event.client.get_entity(event.message.from_id)
        except Exception as e:
            LOGS.info(str(e))
        messaget = media_type(event)
        resalt = f"💤 #TAG_AFK\n<b>👥 Group: </b><code>{hmm.title}</code>"
        if full is not None:
            resalt += (
                f"\n<b>👤 From: </b>{_format.htmlmentionuser(full.first_name, full.id)}"
            )
        if messaget is not None:
            resalt += f"\n<b>🔅 Message Type: </b><code>{messaget}</code>"
        else:
            resalt += f"\n<b>🔹 Message: </b>{event.message.message}"
        button = [
            (Button.url("👁‍🗨 Mᴇssᴀɢᴇ", f"https://t.me/c/{hmm.id}/{event.message.id}"))
        ]
        if not event.is_private:
            await event.client.send_message(
                PM_LOGGER_GROUP_ID,
                resalt,
                parse_mode="html",
                link_preview=False,
            )
        if messaget is not None:
            await event.client.forward_messages(
                PM_LOGGER_GROUP_ID, event.message, silent=True
            )
