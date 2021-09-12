# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from typing import List, Optional, Sequence, Union

from telethon import events
from telethon.hints import (
    DateLike,
    EntityLike,
    FileLike,
    MarkupLike,
    MessageIDLike,
    MessageLike,
    ProgressCallback,
)
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    InputPeerChannel,
    InputPeerChat,
    InputPeerUser,
    Message,
    MessageMediaWebPage,
    PeerUser,
    TypeDocumentAttribute,
    TypeMessageEntity,
    UpdateEditChannelMessage,
    UpdateEditMessage,
)

from ..Config import Config
from ..sql_helper.globals import gvar
from . import lan
from .managers import eor


@events.common.name_inner_event
class NewMessage(events.NewMessage):
    def __init__(self, require_admin: bool = None, inline: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.require_admin = require_admin
        self.inline = inline

    def filter(self, event):
        _event = super().filter(event)
        if not _event:
            return

        if self.inline is not None and bool(self.inline) != bool(
            event.message.via_bot_id
        ):
            return

        if self.require_admin and not isinstance(event._chat_peer, PeerUser):
            is_creator = False
            is_admin = False
            creator = hasattr(event.chat, "creator")
            admin_rights = hasattr(event.chat, "admin_rights")
            flag = None
            if not creator and not admin_rights:
                try:
                    event.chat = event._client.loop.create_task(event.get_chat())
                except AttributeError:
                    flag = "Null"

            if self.incoming:
                try:
                    p = event._client.loop.create_task(
                        event._client.get_permissions(event.chat_id, event.sender_id)
                    )
                    participant = p.participant
                except Exception:
                    participant = None
                if isinstance(participant, ChannelParticipantCreator):
                    is_creator = True
                if isinstance(participant, ChannelParticipantAdmin):
                    is_admin = True
            elif flag:
                is_admin = True
                is_creator = False
            else:
                is_creator = event.chat.creator
                is_admin = event.chat.admin_rights

            if not is_creator and not is_admin:
                text = f"**🚨 {lan('needadmin')}**"

                event._client.loop.create_task(eor(event, text))
                return

        return event


@events.common.name_inner_event
class MessageEdited(NewMessage):
    @classmethod
    def build(cls, update, others=None, self_id=None):
        if isinstance(update, UpdateEditMessage):
            return cls.Event(update.message)
        if isinstance(update, UpdateEditChannelMessage):
            if (
                update.message.edit_date
                and update.message.is_channel
                and not update.message.is_group
            ):
                return
            return cls.Event(update.message)

    class Event(NewMessage.Event):
        pass


async def safe_check_text(msg):  # sourcery no-metrics
    if not msg:
        return False
    msg = str(msg)
    if gvar("BOT_TOKEN") is None:
        return bool(
            (
                (Config.STRING_SESSION in msg)
                or (Config.API_HASH in msg)
                or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg)
                or (gvar("CURRENCY_API") and gvar("CURRENCY_API") in msg)
                or (gvar("DEEPAI_API") and gvar("DEEPAI_API") in msg)
                or (gvar("G_DRIVE_CLIENT_ID") and gvar("G_DRIVE_CLIENT_ID") in msg)
                or (
                    gvar("G_DRIVE_CLIENT_SECRET")
                    and gvar("G_DRIVE_CLIENT_SECRET") in msg
                )
                or (gvar("G_DRIVE_DATA") and gvar("G_DRIVE_DATA") in msg)
                or (gvar("GENIUS_API") and gvar("GENIUS_API") in msg)
                or (gvar("GITHUB_ACCESS_TOKEN") and gvar("GITHUB_ACCESS_TOKEN") in msg)
                or (
                    gvar("IBM_WATSON_CRED_PASSWORD")
                    and gvar("IBM_WATSON_CRED_PASSWORD") in msg
                )
                or (gvar("IBM_WATSON_CRED_URL") and gvar("IBM_WATSON_CRED_URL") in msg)
                or (gvar("IPDATA_API") and gvar("IPDATA_API") in msg)
                or (gvar("LASTFM_API") and gvar("LASTFM_API") in msg)
                or (
                    gvar("LASTFM_PASSWORD_PLAIN")
                    and gvar("LASTFM_PASSWORD_PLAIN") in msg
                )
                or (gvar("LASTFM_SECRET") and gvar("LASTFM_SECRET") in msg)
                or (gvar("OCRSPACE_API") and gvar("OCRSPACE_API") in msg)
                or (gvar("RANDOMSTUFF_API") and gvar("RANDOMSTUFF_API") in msg)
                or (gvar("REMOVEBG_API") and gvar("REMOVEBG_API") in msg)
                or (gvar("SPAMWATCH_API") and gvar("SPAMWATCH_API") in msg)
                or (gvar("SPOTIFY_DC") and gvar("SPOTIFY_DC") in msg)
                or (gvar("SPOTIFY_KEY") and gvar("SPOTIFY_KEY") in msg)
                or (gvar("SS_API") and gvar("SS_API") in msg)
                or (
                    gvar("TG_2STEP_VERIFICATION_CODE")
                    and gvar("TG_2STEP_VERIFICATION_CODE") in msg
                )
                or (gvar("WEATHER_API") and gvar("WEATHER_API") in msg)
            )
        )
    else:
        return bool(
            (
                (Config.STRING_SESSION in msg)
                or (Config.API_HASH in msg)
                or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg)
                or (gvar("BOT_TOKEN") in msg)
                or (gvar("CURRENCY_API") and gvar("CURRENCY_API") in msg)
                or (gvar("DEEPAI_API") and gvar("DEEPAI_API") in msg)
                or (gvar("G_DRIVE_CLIENT_ID") and gvar("G_DRIVE_CLIENT_ID") in msg)
                or (
                    gvar("G_DRIVE_CLIENT_SECRET")
                    and gvar("G_DRIVE_CLIENT_SECRET") in msg
                )
                or (gvar("G_DRIVE_DATA") and gvar("G_DRIVE_DATA") in msg)
                or (gvar("GENIUS_API") and gvar("GENIUS_API") in msg)
                or (gvar("GITHUB_ACCESS_TOKEN") and gvar("GITHUB_ACCESS_TOKEN") in msg)
                or (
                    gvar("IBM_WATSON_CRED_PASSWORD")
                    and gvar("IBM_WATSON_CRED_PASSWORD") in msg
                )
                or (gvar("IBM_WATSON_CRED_URL") and gvar("IBM_WATSON_CRED_URL") in msg)
                or (gvar("IPDATA_API") and gvar("IPDATA_API") in msg)
                or (gvar("LASTFM_API") and gvar("LASTFM_API") in msg)
                or (
                    gvar("LASTFM_PASSWORD_PLAIN")
                    and gvar("LASTFM_PASSWORD_PLAIN") in msg
                )
                or (gvar("LASTFM_SECRET") and gvar("LASTFM_SECRET") in msg)
                or (gvar("OCRSPACE_API") and gvar("OCRSPACE_API") in msg)
                or (gvar("RANDOMSTUFF_API") and gvar("RANDOMSTUFF_API") in msg)
                or (gvar("REMOVEBG_API") and gvar("REMOVEBG_API") in msg)
                or (gvar("SPAMWATCH_API") and gvar("SPAMWATCH_API") in msg)
                or (gvar("SPOTIFY_DC") and gvar("SPOTIFY_DC") in msg)
                or (gvar("SPOTIFY_KEY") and gvar("SPOTIFY_KEY") in msg)
                or (gvar("SS_API") and gvar("SS_API") in msg)
                or (
                    gvar("TG_2STEP_VERIFICATION_CODE")
                    and gvar("TG_2STEP_VERIFICATION_CODE") in msg
                )
                or (gvar("WEATHER_API") and gvar("WEATHER_API") in msg)
            )
        )


async def send_message(
    client,
    entity: "EntityLike",
    message: "MessageLike" = "",
    *,
    reply_to: "Union[int, Message]" = None,
    parse_mode: Optional[str] = (),
    formatting_entities: Optional[List[TypeMessageEntity]] = None,
    link_preview: bool = False,
    file: "Union[FileLike, Sequence[FileLike]]" = None,
    force_document: bool = False,
    clear_draft: bool = False,
    buttons: "MarkupLike" = None,
    silent: bool = None,
    schedule: "DateLike" = None,
    comment_to: "Union[int, Message]" = None,
):
    chatid = entity
    if str(chatid) in [
        str(Config.BOTLOG_CHATID),
        str(Config.PM_LOGGER_GROUP_ID),
    ]:
        return await client.sendmessage(
            entity=chatid,
            message=message,
            reply_to=reply_to,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            link_preview=link_preview,
            file=file,
            force_document=force_document,
            clear_draft=clear_draft,
            buttons=buttons,
            silent=silent,
            schedule=schedule,
            comment_to=comment_to,
        )
    msg = message
    safecheck = await safe_check_text(msg)
    if safecheck:
        if Config.BOTLOG:
            response = await client.sendmessage(
                entity=Config.BOTLOG_CHATID,
                message=msg,
                reply_to=reply_to,
                parse_mode=parse_mode,
                formatting_entities=formatting_entities,
                link_preview=link_preview,
                file=file,
                force_document=force_document,
                clear_draft=clear_draft,
                buttons=buttons,
                silent=silent,
                schedule=schedule,
                comment_to=comment_to,
            )
        msglink = await client.get_msg_link(response)
        msg = f"__🚨 {lan('errrsecuritymsg').format(msglink)}__"
        return await client.sendmessage(
            entity=chatid,
            message=msg,
            reply_to=reply_to,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            link_preview=link_preview,
            file=file,
            force_document=force_document,
            clear_draft=clear_draft,
            buttons=buttons,
            silent=silent,
            schedule=schedule,
            comment_to=comment_to,
        )
    return await client.sendmessage(
        entity=chatid,
        message=msg,
        reply_to=reply_to,
        parse_mode=parse_mode,
        formatting_entities=formatting_entities,
        link_preview=link_preview,
        file=file,
        force_document=force_document,
        clear_draft=clear_draft,
        buttons=buttons,
        silent=silent,
        schedule=schedule,
        comment_to=comment_to,
    )


async def send_file(
    client,
    entity: "EntityLike",
    file: "Union[FileLike, Sequence[FileLike]]",
    *,
    caption: Union[str, Sequence[str]] = None,
    force_document: bool = False,
    file_size: int = None,
    clear_draft: bool = False,
    progress_callback: "ProgressCallback" = None,
    reply_to: "MessageIDLike" = None,
    attributes: "Sequence[TypeDocumentAttribute]" = None,
    thumb: "FileLike" = None,
    allow_cache: bool = True,
    parse_mode: str = (),
    formatting_entities: Optional[List[TypeMessageEntity]] = None,
    voice_note: bool = False,
    video_note: bool = False,
    buttons: "MarkupLike" = None,
    silent: bool = None,
    supports_streaming: bool = False,
    schedule: "DateLike" = None,
    comment_to: "Union[int, Message]" = None,
    **kwargs,
):
    if isinstance(file, MessageMediaWebPage):
        return await client.send_message(
            entity=entity,
            message=caption,
            reply_to=reply_to,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            link_preview=True,
            buttons=buttons,
            silent=silent,
            schedule=schedule,
            comment_to=comment_to,
        )
    chatid = entity
    if str(chatid) == str(Config.BOTLOG_CHATID):
        return await client.sendfile(
            entity=Config.BOTLOG_CHATID,
            file=file,
            caption=caption,
            force_document=force_document,
            file_size=file_size,
            clear_draft=clear_draft,
            progress_callback=progress_callback,
            reply_to=reply_to,
            attributes=attributes,
            thumb=thumb,
            allow_cache=allow_cache,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            voice_note=voice_note,
            video_note=video_note,
            buttons=buttons,
            silent=silent,
            supports_streaming=supports_streaming,
            schedule=schedule,
            comment_to=comment_to,
            **kwargs,
        )

    msg = caption
    safecheck = await safe_check_text(msg)
    try:
        with open(file) as f:
            filemsg = f.read()
    except Exception:
        filemsg = ""
    safe_file_check = await safe_check_text(filemsg)
    if safecheck or safe_file_check:
        if Config.BOTLOG:
            response = await client.sendfile(
                entity=Config.BOTLOG_CHATID,
                file=file,
                caption=msg,
                force_document=force_document,
                file_size=file_size,
                clear_draft=clear_draft,
                progress_callback=progress_callback,
                reply_to=reply_to,
                attributes=attributes,
                thumb=thumb,
                allow_cache=allow_cache,
                parse_mode=parse_mode,
                formatting_entities=formatting_entities,
                voice_note=voice_note,
                video_note=video_note,
                buttons=buttons,
                silent=silent,
                supports_streaming=supports_streaming,
                schedule=schedule,
                comment_to=comment_to,
                **kwargs,
            )
        msglink = await client.get_msg_link(response)
        msg = f"__🚨 {lan('errrsecuritymsg').format(msglink)}__"
        return await client.sendmessage(
            entity=chatid,
            message=msg,
            reply_to=reply_to,
            link_preview=False,
            silent=silent,
            schedule=schedule,
            comment_to=comment_to,
        )
    return await client.sendfile(
        entity=chatid,
        file=file,
        caption=msg,
        force_document=force_document,
        file_size=file_size,
        clear_draft=clear_draft,
        progress_callback=progress_callback,
        reply_to=reply_to,
        attributes=attributes,
        thumb=thumb,
        allow_cache=allow_cache,
        parse_mode=parse_mode,
        formatting_entities=formatting_entities,
        voice_note=voice_note,
        video_note=video_note,
        buttons=buttons,
        silent=silent,
        supports_streaming=supports_streaming,
        schedule=schedule,
        comment_to=comment_to,
        **kwargs,
    )


async def edit_message(
    client,
    entity: "Union[EntityLike, Message]",
    message: "MessageLike" = None,
    text: str = None,
    *,
    parse_mode: str = (),
    formatting_entities: Optional[List[TypeMessageEntity]] = None,
    link_preview: bool = True,
    file: "FileLike" = None,
    force_document: bool = False,
    buttons: "MarkupLike" = None,
    schedule: "DateLike" = None,
):
    chatid = entity
    if isinstance(chatid, InputPeerChannel):
        chat_id = int("-100" + str(chatid.channel_id))
    elif isinstance(chatid, InputPeerChat):
        chat_id = int("-" + str(chatid.chat_id))
    elif isinstance(chatid, InputPeerUser):
        chat_id = int(chatid.user_id)
    else:
        chat_id = chatid
    if str(chat_id) == str(Config.BOTLOG_CHATID):
        return await client.editmessage(
            entity=entity,
            message=message,
            text=text,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            link_preview=link_preview,
            file=file,
            force_document=force_document,
            buttons=buttons,
            schedule=schedule,
        )
    main_msg = text
    safecheck = await safe_check_text(main_msg)
    if safecheck:
        if Config.BOTLOG:
            response = await client.sendmessage(
                entity=Config.BOTLOG_CHATID,
                message=main_msg,
                parse_mode=parse_mode,
                formatting_entities=formatting_entities,
                link_preview=link_preview,
                file=file,
                force_document=force_document,
                buttons=buttons,
                schedule=schedule,
            )
        msglink = await client.get_msg_link(response)
        msg = f"__🚨 {lan('errrsecuritymsg').format(msglink)}__"
        return await client.editmessage(
            entity=chatid,
            message=message,
            text=msg,
            parse_mode=parse_mode,
            formatting_entities=formatting_entities,
            link_preview=link_preview,
            file=file,
            force_document=force_document,
            buttons=buttons,
            schedule=schedule,
        )
    return await client.editmessage(
        entity=chatid,
        message=message,
        text=main_msg,
        parse_mode=parse_mode,
        formatting_entities=formatting_entities,
        link_preview=link_preview,
        file=file,
        force_document=force_document,
        buttons=buttons,
        schedule=schedule,
    )
