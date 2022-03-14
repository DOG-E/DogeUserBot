# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from typing import Union

from pylists import *
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import (
    Channel,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    Chat,
    MessageEntityMentionName,
    User,
)
from telethon.utils import get_display_name

from ...Config import Config
from ...core.events import NewMessage
from ...core.logger import logging
from ...core.managers import edl
from ..resources.constants import *

LOGS = logging.getLogger(__name__)


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
                await edl(
                    dogevent,
                    "`ℹ️ Kullanıcının kullanıcı adını, kimliğini veya cevabını iletin`",
                )
            return None, None
    except Exception as e:
        LOGS.error(
            f"🚨 Kullanıcı verisi çekilmeye çalışılırken bir hata oluştu: {str(e)}"
        )
    if not noedits:
        await edl(dogevent, "__Couldn't fetch user to proceed further.__")
    return None, None


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
            await dogevent.edit("`🚨 Geçersiz kanal veya grup!`")
            return None
        except ChannelPrivateError:
            await dogevent.edit("`🚨 Bu kanal veya grup gizli ya da orada yasaklıyım.`")
            return None
        except ChannelPublicGroupNaError:
            await dogevent.edit("`🚨 Kanal veya grup mevcut değil!`")
            return None
        except (TypeError, ValueError) as err:
            LOGS.info(
                f"Yürütülen işlem için kanal veya grup ID mevcut değil! HATA: {err}"
            )
            await edl(dogevent, "**🚨 HATA:**\n`ℹ️ Sohbeti alamadım!`")
            return None
    return chat_info


async def get_chat_link(
    arg: Union[User, Chat, Channel, NewMessage.Event], reply=None
) -> str:
    if isinstance(arg, (User, Chat, Channel)):
        entity = arg
    else:
        entity = await arg.get_chat()

    if isinstance(entity, User):
        if entity.is_self:
            name = '"Kayıtlı Mesajlar"ında'
        else:
            name = get_display_name(entity) or "Silinen Hesap?"
        extra = f"[{name}](tg://user?id={entity.id})"
    else:
        if hasattr(entity, "username") and entity.username is not None:
            username = f"@{entity.username}"
        else:
            username = entity.id
        if reply is not None:
            if isinstance(username, str) and username.startswith("@"):
                username = username[1:]
            else:
                username = f"c/{username}"
            extra = f"[{entity.title}](https://t.me/{username}/{reply})"
        elif isinstance(username, int):
            username = f"`{username}`"
            extra = f"{entity.title} ( {username} )"
        else:
            extra = f"[{entity.title}](tg://resolve?domain={username})"
    return extra


async def get_message_link(client, event):
    chat = await event.get_chat()
    if event.is_private:
        return f"tg://openmessage?user_id={chat.id}&message_id={event.id}"
    return f"https://t.me/c/{chat.id}/{event.id}"


async def reply_id(event):
    reply_to_id = None
    if event.sender_id in Config.SUDO_USERS:
        reply_to_id = event.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    return reply_to_id


async def is_admin(doge, chat_id, userid):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        req_jo = await doge.get_permissions(chat_id, userid)
        chat_participant = req_jo.participant
        if isinstance(
            chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
        ):
            return True
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
        return False
    else:
        return False


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


def wowcmydev(user):
    if user in M_ST_RS:
        return m_st_rd_v


def wowcg_y(user):
    if user in G_YS:
        return b_ng_y


def inline_mention(user):
    full_name = user_full_name(user) or "Adsız"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


def printUser(entity: User) -> None:
    user = get_display_name(entity)
    LOGS.warning("{0} başarıyla giriş yapıldı.".format(user))
