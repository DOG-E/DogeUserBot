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

from telethon import Button
from telethon.tl.functions.account import GetPrivacyRequest, UpdateProfileRequest
from telethon.tl.types import InputPrivacyKeyStatusTimestamp, PrivacyValueAllowAll

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    PM_LOGGER_GROUP_ID,
    _format,
    constants,
    doge,
    edl,
    gvar,
    lan,
    logging,
    media_type,
    tr,
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
        "header": lan("afk1"),
        "description": lan("afk2"),
        "options": lan("afk3"),
        "usage": [
            f"{tr}afk {lan('reason')}",
            f"{tr}afk {lan('reason')} ; <link>",
            f"{tr}afk {lan('replymsg')}",
        ],
        "examples": f"{tr}afk {lan('afk4')}",
        "note": lan("afk5"),
    },
)
async def afksetter(event):
    lan("afk6")
    reply = await event.get_reply_message()
    media_t = media_type(reply)
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    start_1 = datetime.now()
    AFK_.afk_on = True
    AFK_.afk_star = start_1.replace(microsecond=0)
    if media_t == "Sticker" or not media_t:
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
                await edl(event, f"{lan('afk7')} {AFK_.reason}", 5)
            else:
                await edl(event, lan("afk8"), 5)
            if BOTLOG:
                if AFK_.reason:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"#AFKTRUE \n{lan('afk9')} {AFK_.reason}",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"#AFKTRUE \n{lan('afk10')}",
                    )
    elif media_t != "Sticker" and media_t:
        if not BOTLOG:
            return await edl(
                event,
                lan("afk11"),
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
                await edl(event, f"{lan('afk7')} {AFK_.reason}", 5)
            else:
                await edl(event, lan("afk8"), 5)
            AFK_.media_afk = await reply.forward_to(BOTLOG_CHATID)
            if AFK_.reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \n{lan('afk9')} {AFK_.reason}",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \n{lan('afk10')}",
                )


@doge.bot_cmd(outgoing=True, edited=False)
async def set_not_afk(event):
    if (
        AFK_.afk_on is False
        or (await event.client.get_entity(event.message.from_id)).id
        == (await event.client.get_me()).id
    ):
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
            endtime += f"{d}{lan('days')} {h}{lan('hours')} {m}{lan('minutes')} {s}{lan('seconds')}"
        elif h > 0:
            endtime += f"{h}{lan('hours')} {m}{lan('minutes')} {s}{lan('seconds')}"
        else:
            endtime += (
                f"{m}{lan('minutes')} {s}{lan('seconds')}"
                if m > 0
                else f"{s}{lan('seconds')}"
            )
    current_message = event.message.message
    if (("afk" not in current_message) or ("#afk" not in current_message)) and (
        "on" in AFK_.USERAFK_ON
    ):
        if gvar("AFKRBIO"):
            try:
                await event.client(UpdateProfileRequest(about=f"{gvar('AFKBIO')}"))
            except BaseException:
                pass
        shite = await event.client.send_message(
            event.chat_id,
            lan("afk12") + "`" + endtime + "`",
        )
        AFK_.USERAFK_ON = {}
        AFK_.afk_time = None
        await sleep(5)
        await shite.delete()
        AFK_.afk_on = False
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#AFKFALSE \n{lan('afk13')}\n" + lan("afk14") + "`" + endtime + "`",
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
            endtime += f"{d}{lan('days')} {h}{lan('hours')} {m}{lan('minutes')} {s}{lan('seconds')}"
        elif h > 0:
            endtime += f"{h}{lan('hours')} {m}{lan('minutes')} {s}{lan('seconds')}"
        else:
            endtime += (
                f"{m}{lan('minutes')} {s}{lan('seconds')}"
                if m > 0
                else f"{s}{lan('seconds')}"
            )
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
                    + f"\n\n{lan('afkreason')} {AFK_.reason}"
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
                dogerafk = constants.DOGEAFK + f"\n\n{lan('afkreason')} {AFK_.reason}"
            else:
                dogeafk = constants.DOGEAFK

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
        resalt = f"💤 #TAG_AFK\n<b>{lan('afk15')} </b><code>{hmm.title}</code>"
        if full is not None:
            resalt += f"\n<b>{lan('afk16')} </b>{_format.htmlmentionuser(full.first_name, full.id)}"
        if messaget is not None:
            resalt += f"\n<b>{lan('afk17')} </b><code>{messaget}</code>"
        else:
            resalt += f"\n<b>{lan('afk18')} </b>{event.message.message}"
        button = [
            (
                Button.url(
                    f"{lan('afk19')}", f"https://t.me/c/{hmm.id}/{event.message.id}"
                )
            )
        ]
        if not event.is_private:
            await event.client.send_message(
                PM_LOGGER_GROUP_ID,
                resalt,
                parse_mode="html",
                link_preview=False,
                slient=True,
            )
            if messaget is not None:
                await event.client.forward_messages(
                    PM_LOGGER_GROUP_ID, event.message, silent=True
                )


# Lang By Aylak
# Copyright (C) 2021 - DOG-E - MutlCC
