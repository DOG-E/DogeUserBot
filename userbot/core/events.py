from typing import Optional, Union, List, Sequence

from telethon import events
from telethon.hints import (
    EntityLike,
    MessageLike,
    FileLike,
    MarkupLike,
    DateLike,
    MessageIDLike,
    ProgressCallback,
)
from telethon.tl.types import (
    InputPeerChannel,
    InputPeerChat,
    InputPeerUser,
    MessageMediaWebPage,
    PeerUser,
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
    UpdateEditMessage,
    UpdateEditChannelMessage,
    TypeMessageEntity,
    TypeDocumentAttribute,
    Message,
)

from ..Config import Config
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
                text = "**🚨 I need admin rights to be able to use this command!**"

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
    return bool(
        (
            (Config.STRING_SESSION in msg)
            or (Config.API_HASH in msg)
            or (Config.BOT_TOKEN in msg)
            or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg)
            or (Config.CURRENCY_API and Config.CURRENCY_API in msg)
            or (Config.DEEP_AI and Config.DEEP_AI in msg)
            or (Config.G_DRIVE_CLIENT_ID and Config.G_DRIVE_CLIENT_ID in msg)
            or (Config.G_DRIVE_CLIENT_SECRET and Config.G_DRIVE_CLIENT_SECRET in msg)
            or (Config.G_DRIVE_DATA and Config.G_DRIVE_DATA in msg)
            or (Config.GENIUS_API and Config.GENIUS_API in msg)
            or (Config.GITHUB_ACCESS_TOKEN and Config.GITHUB_ACCESS_TOKEN in msg)
            or (Config.IBM_WATSON_CRED_PASSWORD and Config.IBM_WATSON_CRED_PASSWORD in msg)
            or (Config.IBM_WATSON_CRED_URL and Config.IBM_WATSON_CRED_URL in msg)
            or (Config.IPDATA_API and Config.IPDATA_API in msg)
            or (Config.LASTFM_API and Config.LASTFM_API in msg)
            or (Config.LASTFM_PASSWORD_PLAIN and Config.LASTFM_PASSWORD_PLAIN in msg)
            or (Config.LASTFM_SECRET and Config.LASTFM_SECRET in msg)
            or (Config.OCRSPACE_API and Config.OCRSPACE_API in msg)
            or (Config.OPEN_WEATHER_MAP_APPID and Config.OPEN_WEATHER_MAP_APPID in msg)
            or (Config.RANDOM_STUFF_API_KEY and Config.RANDOM_STUFF_API_KEY in msg)
            or (Config.RMBG_API and Config.RMBG_API in msg)
            or (Config.SCREEN_SHOT_LAYER_ACCESS_KEY and Config.SCREEN_SHOT_LAYER_ACCESS_KEY in msg)
            or (Config.SP_DC and Config.SP_DC in msg)
            or (Config.SP_KEY and Config.SP_KEY in msg)
            or (Config.SPAMWATCH_API and Config.SPAMWATCH_API in msg)
            or (Config.TG_2STEP_VERIFICATION_CODE and Config.TG_2STEP_VERIFICATION_CODE in msg)
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
        msg = f"__🚨 Sorry I can't send this message in public chats it may have some sensitive data So check in __[your BotLog group]({msglink})."
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
        msg = f"__🚨 Sorry I can't send this message in public chats it may have some sensitive data So check in __[your BotLog group]({msglink})."
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
        msg = f"__🚨 Sorry I can't send this message in public chats it may have some sensitive data So check in __[your BotLog group]({msglink})."
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
