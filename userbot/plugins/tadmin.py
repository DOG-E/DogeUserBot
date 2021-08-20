"""
idea from lynda and rose bot
made by @mrconfused
"""
from telethon.errors import BadRequestError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    S_NOPERM,
    _format,
    doge,
    eor,
    extract_time,
    get_user_from_event,
)

plugin_category = "admin"


@doge.bot_cmd(
    pattern="tmute(?:\s|$)([\s\S]*)",
    command=("tmute", plugin_category),
    info={
        "header": "To stop sending messages permission for that user",
        "description": "Temporary mutes the user for given time.",
        "Time units": {
            "s": "seconds",
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tmute <userid/username/reply> <time>",
            "{tr}tmute <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tmute 2d to test muting for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tmuter(event):  # sourcery no-metrics
    "To mute a person for specific time"
    dogevent = await eor(event, "`muting....`")
    user, reason = await get_user_from_event(event, dogevent)
    if not user:
        return
    if not reason:
        return await dogevent.edit("You haven't mentioned time, check `.doge tmute`")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    dogtime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(dogevent, dogtime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await dogevent.edit("Sorry, I can't mute myself")
    try:
        await dogevent.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, send_messages=True),
            )
        )
        # Announce that the function is done
        if reason:
            await dogevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {get_display_name(await event.get_chat())}\n"
                f"**Muted for: **{dogtime}\n"
                f"**Reason: **__{reason}__"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User: **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat: **{get_display_name(await event.get_chat())}(`{event.chat_id}`)\n"
                    f"**Muted for: **`{dogtime}`\n"
                    f"**Reason: **`{reason}``",
                )
        else:
            await dogevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)} was muted in {get_display_name(await event.get_chat())}\n"
                f"Muted for {dogtime}\n"
            )
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#TMUTE\n"
                    f"**User: **[{user.first_name}](tg://user?id={user.id})\n"
                    f"**Chat: **{get_display_name(await event.get_chat())}(`{event.chat_id}`)\n"
                    f"**Muted for: **`{dogtime}`",
                )
        # Announce to logging group
    except UserIdInvalidError:
        return await dogevent.edit("`Uh oh my mute logic broke!`")
    except UserAdminInvalidError:
        return await dogevent.edit(
            "`Either you're not an admin or you tried to mute an admin that you didn't promote`"
        )
    except Exception as e:
        return await dogevent.edit(f"`{e}`")


@doge.bot_cmd(
    pattern="tban(?:\s|$)([\s\S]*)",
    command=("tban", plugin_category),
    info={
        "header": "To remove a user from the group for specified time.",
        "description": "Temporary bans the user for given time.",
        "Time units": {
            "s": "seconds",
            "m": "minutes",
            "h": "Hours",
            "d": "days",
            "w": "weeks",
        },
        "usage": [
            "{tr}tban <userid/username/reply> <time>",
            "{tr}tban <userid/username/reply> <time> <reason>",
        ],
        "examples": ["{tr}tban 2d to test baning for 2 days"],
    },
    groups_only=True,
    require_admin=True,
)
async def tban(event):  # sourcery no-metrics
    "To ban a person for specific time"
    dogevent = await eor(event, "`banning....`")
    user, reason = await get_user_from_event(event, dogevent)
    if not user:
        return
    if not reason:
        return await dogevent.edit("you haven't mentioned time, check `.doge tban`")
    reason = reason.split(" ", 1)
    hmm = len(reason)
    dogtime = reason[0].strip()
    reason = "".join(reason[1:]) if hmm > 1 else None
    ctime = await extract_time(dogevent, dogtime)
    if not ctime:
        return
    if user.id == event.client.uid:
        return await dogevent.edit("Sorry, I can't ban myself")
    await dogevent.edit("`Whacking the pest!`")
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user.id,
                ChatBannedRights(until_date=ctime, view_messages=True),
            )
        )
    except UserAdminInvalidError:
        return await dogevent.edit(
            "`Either you're not an admin or you tried to ban an admin that you didn't promote`"
        )
    except BadRequestError:
        return await dogevent.edit(S_NOPERM)
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await dogevent.edit(
            "`I don't have message nuking rights! But still he was banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {get_display_name(await event.get_chat())}\n"
            f"banned for {dogtime}\n"
            f"Reason:`{reason}`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User: **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat: **{get_display_name(await event.get_chat())}(`{event.chat_id}`)\n"
                f"**Banned untill: **`{dogtime}`\n"
                f"**Reason: **__{reason}__",
            )
    else:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} was banned in {get_display_name(await event.get_chat())}\n"
            f"banned for {dogtime}\n"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#TBAN\n"
                f"**User: **[{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat: **{get_display_name(await event.get_chat())}(`{event.chat_id}`)\n"
                f"**Banned untill: **`{dogtime}`",
            )
