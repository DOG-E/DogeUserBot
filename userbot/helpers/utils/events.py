# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from pylists import *
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import MessageEntityMentionName

from ...Config import Config
from ...core.logger import logging
from ...core.managers import edl
from ..resources.constants import *

LOGS = logging.getLogger(__name__)


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def get_user_from_event(
    event, dogevent=None, secondgroup=None, nogroup=False, noedits=False
):  # sourcery no-metrics
    if dogevent is None:
        dogevent = event
    if nogroup is False:
        if secondgroup:
            args = event.pattern_match.group(2).split(" ", 1)
        else:
            args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    try:
        if args:
            user = args[0]
            if len(args) > 1:
                extra = "".join(args[1:])
            if user.isnumeric() or (user.startswith("-") and user[1:].isnumeric()):
                user = int(user)
            if event.message.entities:
                probable_user_mention_entity = event.message.entities[0]
                if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                    user_id = probable_user_mention_entity.user_id
                    user_obj = await event.client.get_entity(user_id)
                    return user_obj, extra
            if isinstance(user, int) or user.startswith("@"):
                user_obj = await event.client.get_entity(user)
                return user_obj, extra
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    try:
        if nogroup is False:
            if secondgroup:
                extra = event.pattern_match.group(2)
            else:
                extra = event.pattern_match.group(1)
        if event.is_private:
            user_obj = await event.get_chat()
            return user_obj, extra
        if event.reply_to_msg_id:
            previous_message = await event.get_reply_message()
            if previous_message.from_id is None:
                if not noedits:
                    await edl(dogevent, "`🐾 Bu anonim bir yönetici!`")
                return None, None
            user_obj = await event.client.get_entity(previous_message.sender_id)
            return user_obj, extra
        if not args:
            if not noedits:
                await edl(dogevent, "`ℹ️ Kullanıcının kullanıcı adını, kimliğini veya cevabını iletin`")
            return None, None
    except Exception as e:
        LOGS.error(f"🚨 Kullanıcı verisi çekilmeye çalışılırken bir hata oluştu: {str(e)}")
    if not noedits:
        await edl(dogevent, "__Couldn't fetch user to proceed further.__")
    return None, None


def inline_mention(user):
    full_name = user_full_name(user) or "No name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


async def checking(doge):
    try:
        c = JoinChannelRequest(C_G_[0])
        await doge(c)
    except BaseException:
        pass
    try:
        g = JoinChannelRequest(C_G_[1])
        await doge(g)
    except BaseException:
        pass


async def wowmygroup(event, msg):
    if str(event.chat_id) in GR__PS:
        await edl(
            event,
            msg,
            300,
        )
        return True
    return False


async def wowmydev(user, event):
    if str(user) in M_ST_RS:
        await edl(
            event,
            hm_st_rd_v,
            30,
        )
        return True
    return False


async def wowcmydev(user):
    if user in M_ST_RS:
        return m_st_rd_v


async def wowcg_y(user):
    if user in G_YS:
        return b_ng_y


async def get_chatinfo(event, dogevent):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await dogevent.edit("`🚨 Geçersiz kanal / grup!`")
            return None
        except ChannelPrivateError:
            await dogevent.edit(
                "`🚨 Bu kanal/grup gizli ya da orada yasaklıyım.`"
            )
            return None
        except ChannelPublicGroupNaError:
            await dogevent.edit("`🚨 Kanal veya grup mevcut değil!`")
            return None
        except (TypeError, ValueError) as err:
            LOGS.info(f"Yürütülen işlem için kanal veya grup ID mevcut değil! HATA: {err}")
            await edl(dogevent, f"**🚨 HATA:**\n`ℹ️ Sohbeti alamadım!`")
            return None
    return chat_info
