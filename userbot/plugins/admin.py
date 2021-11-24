# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
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

PP_TOO_SMOL = lan("pptoosmol")
PP_ERROR = lan("pmerror")
NO_PERM = lan("noperm")
CHAT_PP_CHANGED = lan("chatppchanged")
INVALID_MEDIA = lan("invalidmedia")

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
    pattern="(d|)gpic$",
    command=("gpic", plugin_category),
    info={
        "header": lan("gpic1"),
        "description": lan("gpic2"),
        "flags": {
            "d": lan("gpic3"),
        },
        "usage": [
            f"{tr}gpic {lan('replyimg')}",
            "{tr}dgpic",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    lan("gpic4")
    flag = (event.pattern_match.group(1)).strip()
    if flag == "d":
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edl(event, f"{lan('errr')} `{e}`")
        process = "deleted"
        await edl(event, lan("gpic5"))
    else:
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
                return await edl(event, f"{lan('errr')}:  `{str(e)}`")
            process = "updated"
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GROUPPIC\n"
            f"{lan('gpic6').format(process)}"
            f"{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", plugin_category),
    info={
        "header": lan("pro1"),
        "description": lan("pro2"),
        "usage": [
            f"{tr}promote {lan('usrreply')}",
            f"{tr}promote {lan('usrreply')} {lan('pro3')}",
        ],
        "note": lan("pro4"),
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    lan("pro5")
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
    dogevent = await eor(event, lan("pro6"))
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    await dogevent.edit(lan("lan7"))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PROMOTE\
            \n{lan('userx')}: [{user.first_name}](tg://user?id={user.id})\
            \n{lan('chat')}: {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", plugin_category),
    info={
        "header": lan("demo1"),
        "description": lan("demo2"),
        "usage": [
            f"{tr}demote {lan('usrreply')}",
            f"{tr}demote {lan('usrreply')} {lan('demo3')}",
        ],
        "note": lan("demo4"),
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    lan("demo5")
    user, _ = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, lan("demo6"))
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
    await dogevent.edit(lan("demo7"))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#DEMOTE\
            \n{lan('userx')}: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", plugin_category),
    info={
        "header": lan("ban1"),
        "description": lan("ban2"),
        "usage": [
            f"{tr}ban {lan('ban3')}",
            f"{tr}ban {lan('usrreply')} {lan('reason')}",
        ],
        "note": lan("ban4"),
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    lan("ban5")
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, lan("ban6"))
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, lan("ban7"))
    try:
        await event.client(EditBannedRequest(event.chat_id, user_id, BANNED_RIGHTS))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await dogevent.edit(lan("ban8"))
    if reason:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}{lan('ban9')}\n**{lan('reason')}:** `{reason}`"
        )
    else:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)} {lan('ban9')}"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \n{lan('userx')}: [{user.first_name}](tg://user?id={user_id})\
                \n{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \n{lan('reason')}: {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \n{lan('userx')}: [{user.first_name}](tg://user?id={user_id})\
                \n{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", plugin_category),
    info={
        "header": lan("unban1"),
        "description": lan("unban2"),
        "usage": [
            f"{tr}unban {lan('usrreply')}",
            f"{tr}unban {lan('usrreply')} {lan('reason')}",
        ],
        "note": lan("unban3"),
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    lan("unban4")
    user, _ = await get_user_from_event(event)
    if not user:
        return
    dogevent = await eor(event, lan("unban5"))
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} {lan('unban6')}"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"{lan('userx')}: [{user.first_name}](tg://user?id={user.id})\n"
                f"{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await dogevent.edit(lan("unban7"))
    except Exception as e:
        await dogevent.edit(f"{lan('errr')}\n`{e}`")


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
        "header": lan("mute1"),
        "description": lan("mute2"),
        "usage": [
            f"{tr}mute {lan('usrreply')}",
            f"{tr}mute {lan('usrreply')} {lan('reason')}",
        ],
        "note": lan("mute3"),
    },  # sourcery no-metrics
)
async def startmute(event):
    lan("mute4")
    if event.is_private:
        await event.edit(lan("mute5"))
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(lan("mute6"))
        if event.chat_id == doge.uid:
            return await edl(event, lan("mute7"))
        flag = await wowmydev(replied_user, event)
        if flag:
            return
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"{lan('errr')}\n`{e}`")
        else:
            await event.edit(lan("mute8"))
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"{lan('userx')} [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(event, lan("mute9"))
        user, reason = await get_user_from_event(event)
        if not user:
            return
        user_id = user.id
        if user_id == doge.uid:
            return await eor(event, lan("mute10"))
        flag = await wowmydev(user_id, event)
        if flag:
            return
        if is_muted(user_id, event.chat_id):
            return await eor(event, lan("mute11"))
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await eor(
                    event,
                    lan("mute12"),
                )
        except AttributeError:
            pass
        except Exception as e:
            return await eor(event, f"{lan('errr')} `{e}`")
        try:
            await event.client(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await eor(
                        event,
                        lan("mute13"),
                    )
            elif "creator" not in vars(chat):
                return await eor(event, lan("mute14"))
            mute(user_id, event.chat_id)
        except Exception as e:
            return await eor(event, f"{lan('errr')} `{e}`")
        if reason:
            await eor(
                event,
                f"{lan('mute15').format(_format.mentionuser(user.first_name ,user_id), get_display_name(await event.get_chat()))}\n"
                f"`{lan('reason')}:`{reason}",
            )
        else:
            await eor(
                event,
                f"{lan('mute15').format(_format.mentionuser(user.first_name ,user_id), get_display_name(await event.get_chat()))}\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"{lan('userx')} [{user.first_name}](tg://user?id={user_id})\n"
                f"{lan('chat')} {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", plugin_category),
    info={
        "header": lan("unmute1"),
        "description": lan("unmute2"),
        "usage": [
            f"{tr}unmute {lan('usrreply')}",
            f"{tr}unmute {lan('usrreply')} {lan('reason')}",
        ],
        "note": lan("unmute3"),
    },
)
async def endmute(event):
    lan("unmute4")
    if event.is_private:
        await event.edit(lan("unmute5"))
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(lan("unmute6"))
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"{lan('errr')}\n`{e}`")
        else:
            await event.edit(lan("unmute7"))
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"{lan('userx')} [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
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
                lan("unmute8"),
            )
        except Exception as e:
            return await eor(event, f"{lan('errr')} `{e}`")
        await eor(
            event,
            f"{lan('unmute9').format(_format.mentionuser(user.first_name ,user_id), get_display_name(await event.get_chat()))}\n",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"{lan('userx')} [{user.first_name}](tg://user?id={user.id})\n"
                f"{lan('chat')} {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@doge.bot_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", plugin_category),
    info={
        "header": lan("kick1"),
        "description": lan("kick2"),
        "usage": [
            f"{tr}kick {lan('usrreply')}",
            f"{tr}kick {lan('usrreply')} {lan('reason')}",
        ],
        "note": lan("kick3"),
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    lan("kick4")
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, lan("kick5"))
    try:
        await event.client.kick_participant(event.chat_id, user_id)
    except Exception as e:
        return await dogevent.edit(NO_PERM + f"\n{e}")
    if reason:
        await dogevent.edit(
            f" {lan('kick6')} [{user.first_name}](tg://user?id={user_id})`!`\n**{lan('reason')}** `{reason}`"
        )
    else:
        await dogevent.edit(
            f"{lan('kick6')} [{user.first_name}](tg://user?id={user_id})`!`"
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"{lan('userx')}: [{user.first_name}](tg://user?id={user_id})\n"
            f"{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@doge.bot_cmd(
    pattern="pin( l|$)",
    command=("pin", plugin_category),
    info={
        "header": lan("pin1"),
        "description": lan("pin4"),
        "options": {"l": lan("pin2")},
        "usage": [
            f"{tr}pin {lan('replymsg')}",
            f"{tr}pin l {lan('replymsg')}",
        ],
        "note": lan("pin3"),
    },
)
async def pin(event):
    lan("pin5")
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edl(event, lan("pin6"), 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, lan("pin7"), 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PIN\
                \n{lan('pin8')}\
                \n{lan('chat')} {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \n{lan('loud')}: {is_silent}",
        )


@doge.bot_cmd(
    pattern="unpin(all|$)",
    command=("unpin", plugin_category),
    info={
        "header": lan("unpin1"),
        "description": lan("unpin2"),
        "options": {"all": lan("unpin4")},
        "usage": [
            f"{tr}unpin {lan('replymsg')}",
            "{tr}unpinall",
        ],
        "note": lan("unpin3"),
    },
)
async def pin(event):
    lan("unpin5")
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edl(
            event,
            lan("unpin6").format(tr),
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edl(event, lan("unpin7").format(tr), 5)
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, lan("unpin8"), 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UNPIN\
                \n{lan('unpin9')}\
                \n{lan('chat')}: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@doge.bot_cmd(
    pattern="undlt( .u)?(?: |$)(\d*)?",
    command=("undlt", plugin_category),
    info={
        "header": lan("undlt1"),
        "description": lan("undlt2"),
        "flags": {"m": lan("undlt3")},
        "usage": [
            f"{tr}undlt {lan('count')}",
            f"{tr}undlt .m {lan('count')}",
        ],
        "examples": [
            "{tr}undlt 7",
            f"{tr}undlt .m 7 {lan('undlt')}",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    lan("undlt5")
    dogevent = await eor(event, lan("undlt6"))
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
    deleted_msg = lan("undlt7").format(lim)
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n{lan('undlt8').format(msg.old.message, _format.mentionuser(ruser.first_name, ruser.id))}"
            else:
                deleted_msg += f"\n{lan('undlt9').format(_media_type, _format.mentionuser(ruser.first_name, ruser.id))}"
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
                    f"{lan('undlt8').format(msg.old.message, _format.mentionuser(ruser.first_name, ruser.id))}"
                )
            else:
                await main_msg.reply(
                    f"{lan('undlt8').format(msg.old.message, _format.mentionuser(ruser.first_name, ruser.id))}",
                    file=msg.old.media,
                )


# aylak
# MutlCC
