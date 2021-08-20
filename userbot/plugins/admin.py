from asyncio import sleep

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name

from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    _format,
    doge,
    edl,
    eor,
    get_user_from_event,
    lan,
    logging,
    media_type,
    tr,
    wowmydev,
)

# =================== STRINGS ============
plugin_category = "admin"
LOGS = logging.getLogger(__name__)

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_PERM = lan("noperm")
CHAT_PP_CHANGED = "`Chat Picture Changed`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@doge.bot_cmd(
    pattern="gpic( -s| -d)$",
    command=("gpic", plugin_category),
    info={
        "header": "For changing group display pic or deleting display pic",
        "description": "Reply to Image for changing display picture",
        "flags": {
            "-s": "To set group pic",
            "-d": "To delete group pic",
        },
        "usage": [
            "{tr}gpic -s <reply to image>",
            "{tr}gpic -d",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edl(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edl(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edl(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edl(event, PP_ERROR)
            except Exception as e:
                return await edl(event, f"**Error: **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edl(event, f"**Error: **`{e}`")
        process = "deleted"
        await edl(event, "```Successfully group profile pic deleted.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GROUPPIC\n"
            f"Group profile pic {process} successfully "
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", plugin_category),
    info={
        "header": "To give admin rights for a person",
        "description": "Provides admin rights to the person in the chat\
            \nNote : You need proper rights for this",
        "usage": [
            "{tr}promote <userid/username/reply>",
            "{tr}promote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "To promote a person in chat"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    dogevent = await eor(event, "`Promoting...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    await dogevent.edit("`Promoted Successfully! Now gib Party`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PROMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", plugin_category),
    info={
        "header": "To remove a person from admin list",
        "description": "Removes all admin rights for that peron in that chat\
            \nNote : You need proper rights for this and also u must be owner or admin who promoted that guy",
        "usage": [
            "{tr}demote <userid/username/reply>",
            "{tr}demote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "To demote a person in group"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "`Demoting...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    await dogevent.edit("`Demoted Successfully! Betterluck next time`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#DEMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", plugin_category),
    info={
        "header": "Will ban the guy in the group where you used this command.",
        "description": "Permanently will remove him from this group and he can't join back\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}ban <userid/username/reply>",
            "{tr}ban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "To ban a person in group"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, "__You can't ban yourself.__")
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "`Whacking the pest!`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user_id, BANNED_RIGHTS))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await dogevent.edit(
            "`I don't have message nuking rights! But still he is banned!`"
        )
    if reason:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}` is banned !!`\n**Reason : **`{reason}`"
        )
    else:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)} `is banned !!`"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user_id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nREASON : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user_id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", plugin_category),
    info={
        "header": "Will unban the guy in the group where you used this command.",
        "description": "Removes the user account from the banned list of the group\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unban <userid/username/reply>",
            "{tr}unban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "To unban a person"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    dogevent = await eor(event, "`Unbanning...`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `is Unbanned Successfully. Granting another chance.`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await dogevent.edit("`Uh oh my unban logic broke!`")
    except Exception as e:
        await dogevent.edit(f"**Error :**\n`{e}`")


@doge.bot_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@doge.bot_cmd(
    pattern="mute(?:\s|$)([\s\S]*)",
    command=("mute", plugin_category),
    info={
        "header": "To stop sending messages from that user",
        "description": "If is is not admin then changes his permission in group,\
            if he is admin or if you try in personal chat then his messages will be deleted\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}mute <userid/username/reply>",
            "{tr}mute <userid/username/reply> <reason>",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`This user is already muted in this chat ~~lmfao sed rip~~`"
            )
        if event.chat_id == doge.uid:
            return await edl(event, "`You can't mute yourself`")
        flag = await wowmydev(replied_user, event)
        if flag:
            return
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error:**\n`{e}`")
        else:
            await event.edit("`Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"**User :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(
                event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        user_id = user.id
        if user_id == doge.uid:
            return await eor(event, "`Sorry, I can't mute myself`")
        flag = await wowmydev(user_id, event)
        if flag:
            return
        if is_muted(user_id, event.chat_id):
            return await eor(
                event, "`This user is already muted in this chat ~~lmfao sed rip~~`"
            )
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await eor(
                    event,
                    "`This user is already muted in this chat ~~lmfao sed rip~~`",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await eor(event, f"**Error: **`{e}`")
        try:
            await event.client(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await eor(
                        event,
                        "`You can't mute a person if you don't have delete messages permission. ಥ﹏ಥ`",
                    )
            elif "creator" not in vars(chat):
                return await eor(
                    event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
                )
            mute(user_id, event.chat_id)
        except Exception as e:
            return await eor(event, f"**Error: **`{e}`")
        if reason:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user_id)} `is muted in {get_display_name(await event.get_chat())}`\n"
                f"`Reason:`{reason}",
            )
        else:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user_id)} `is muted in {get_display_name(await event.get_chat())}`\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user_id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", plugin_category),
    info={
        "header": "To allow user to send messages again",
        "description": "Will change user permissions ingroup to send messages again.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unmute <userid/username/reply>",
            "{tr}unmute <userid/username/reply> <reason>",
        ],
    },
)
async def endmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）`"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error:**\n`{e}`")
        else:
            await event.edit(
                "`Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"**User:** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await eor(
                event,
                "`This user can already speak freely in this chat ~~lmfao sed rip~~`",
            )
        except Exception as e:
            return await eor(event, f"**Error: **`{e}`")
        await eor(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `is unmuted in {get_display_name(await event.get_chat())}\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", plugin_category),
    info={
        "header": "To kick a person from the group",
        "description": "Will kick the user from the group so he can join back.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}kick <userid/username/reply>",
            "{tr}kick <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "use this to kick a user from chat"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "`Kicking...`")
    try:
        await event.client.kick_participant(event.chat_id, user_id)
    except Exception as e:
        return await dogevent.edit(NO_PERM + f"\n{e}")
    if reason:
        await dogevent.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user_id})`!`\nReason: {reason}"
        )
    else:
        await dogevent.edit(f"`Kicked` [{user.first_name}](tg://user?id={user_id})`!`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user_id})\n"
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@doge.bot_cmd(
    pattern="pin( l|$)",
    command=("pin", plugin_category),
    info={
        "header": "For pining messages in chat",
        "description": "reply to a message to pin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"l": "To notify everyone without this.it will pin silently"},
        "usage": [
            "{tr}pin <reply>",
            "{tr}pin l <reply>",
        ],
    },
)
async def pin(event):
    "To pin a message in chat"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edl(event, "`Reply to a message to pin it.`", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, "`Pinned Successfully!`", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PIN\
                \n__Successfully pinned a message in chat__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nLOUD: {is_silent}",
        )


@doge.bot_cmd(
    pattern="unpin(all|$)",
    command=("unpin", plugin_category),
    info={
        "header": "For unpining messages in chat",
        "description": "reply to a message to unpin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"all": "To unpin all messages in the chat"},
        "usage": [
            "{tr}unpin <reply>",
            "{tr}unpinall",
        ],
    },
)
async def pin(event):
    "To unpin message(s) in the group"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edl(
            event,
            "__Reply to a message to unpin it or use __`.unpin all`__ to unpin all__",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edl(
                event, f"`Reply to a message to unpin it or use {tr}unpinall`", 5
            )
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, "`Unpinned successfully!`", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UNPIN\
                \n__Successfully unpinned message(s) in chat__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="undlt( .u)?(?: |$)(\d*)?",
    command=("undlt", plugin_category),
    info={
        "header": "To get recent deleted messages in group",
        "description": "To check recent deleted messages in group, by default will show 5. you can get 1 to 15 messages.",
        "flags": {
            "m": "use this flag to upload media to chat else will just show as media."
        },
        "usage": [
            "{tr}undlt <count>",
            "{tr}undlt .m <count>",
        ],
        "examples": [
            "{tr}undlt 7",
            "{tr}undlt .m 7 (this will reply all 7 messages to this message",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "To check recent deleted messages in group"
    dogevent = await eor(event, "`Searching recent actions .....`")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**Recent {lim} Deleted message(s) in this group are :**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await eor(dogevent, deleted_msg)
    else:
        main_msg = await eor(dogevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**Sent by** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
