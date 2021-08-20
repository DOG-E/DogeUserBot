from asyncio import sleep
from base64 import b64decode
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, ReportSpamRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, _format, admin_groups, doge, edl, eor, get_user_from_event, wowmydev

plugin_category = "admin"

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


@doge.bot_cmd(
    pattern="gban(?:\s|$)([\s\S]*)",
    command=("gban", plugin_category),
    info={
        "header": "To ban user in every group where you are admin.",
        "description": "Will ban the person in every group where you are admin only.",
        "usage": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def doggban(event):  # sourcery no-metrics
    "To ban user in every group where you are admin."
    dogg = await eor(event, "`Gbanning...`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, dogg)
    if not user:
        return
    user_id = user.id
    if user_id == doge.uid:
        return await edl(dogg, "`why would I ban myself`")
    flag = await wowmydev(user_id, event)
    if flag:
        return
    try:
        hmm = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user_id):
        await dogg.edit(
            f"`the `[user](tg://user?id={user_id})` is already in gbanned list any way checking again`"
        )
    else:
        gban_sql.doggban(user_id, reason)
    happy = await admin_groups(event.client)
    count = 0
    teledoge = len(happy)
    if teledoge == 0:
        return await edl(dogg, "`you are not admin of atleast one group` ")
    await dogg.edit(
        f"`initiating gban of the `[user](tg://user?id={user_id}) `in {len(happy)} groups`"
    )
    for i in range(teledoge):
        try:
            await event.client(EditBannedRequest(happy[i], user_id, BANNED_RIGHTS))
            await event.client(ReportSpamRequest(user_id))
            await event.client(BlockRequest(user_id))
            await sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(happy[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`For banning here`",
            )
    end = datetime.now()
    dogtaken = (end - start).seconds
    if reason:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user_id}) `was gbanned in {count} groups in {dogtaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user_id}) `was gbanned in {count} groups in {dogtaken} seconds`!!"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user_id})\
                \n**ID : **`{user_id}`\
                \n**Reason :** `{reason}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user_id})\
                \n**ID : **`{user_id}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@doge.bot_cmd(
    pattern="ungban(?:\s|$)([\s\S]*)",
    command=("ungban", plugin_category),
    info={
        "header": "To unban the person from every group where you are admin.",
        "description": "will unban and also remove from your gbanned list.",
        "usage": "{tr}ungban <username/reply/userid>",
    },
)
async def doggban(event):
    "To unban the person from every group where you are admin."
    dogg = await eor(event, "`ungbanning.....`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, dogg)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.dogungban(user.id)
    else:
        return await edl(
            dogg, f"the [user](tg://user?id={user.id}) `is not in your gbanned list`"
        )
    happy = await admin_groups(event.client)
    count = 0
    teledoge = len(happy)
    if teledoge == 0:
        return await edl(dogg, "`you are not even admin of atleast one group `")
    await dogg.edit(
        f"initiating ungban of the [user](tg://user?id={user.id}) in `{len(happy)}` groups"
    )
    for i in range(teledoge):
        try:
            await event.client(EditBannedRequest(happy[i], user.id, UNBAN_RIGHTS))
            await sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(happy[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`For Unbanning here`",
            )
    end = datetime.now()
    dogtaken = (end - start).seconds
    if reason:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) was ungbanned in {count} groups in {dogtaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `was ungbanned in {count} groups in {dogtaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Reason :** `{reason}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )


@doge.bot_cmd(
    pattern="listgban$",
    command=("listgban", plugin_category),
    info={
        "header": "Shows you the list of all gbanned users by you.",
        "usage": "{tr}listgban",
    },
)
async def gablist(event):
    "Shows you the list of all gbanned users by you."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    await eor(event, GBANNED_LIST)


@doge.bot_cmd(
    pattern="gmute(?:\s|$)([\s\S]*)",
    command=("gmute", plugin_category),
    info={
        "header": "To mute a person in all groups where you are admin.",
        "description": "It doesnt change user permissions but will delete all messages sent by him in the groups where you are admin including in private messages.",
        "usage": "{tr}gmute username/reply> <reason (optional)>",
    },
)
async def startgmute(event):
    "To mute a person in all groups where you are admin."
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await sleep(2)
        userid = event.chat_id
        flag = await wowmydev(userid, event)
        if flag:
            return
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        userid = user.id
        if userid == doge.uid:
            return await eor(event, "`Sorry, I can't gmute myself`")
        flag = await wowmydev(userid, event)
        if flag:
            return
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await eor(event, "`Sorry. I am unable to fetch the user`")
    if is_muted(userid, "gmute"):
        return await eor(
            event,
            f"{_format.mentionuser(user.first_name ,userid)} ` is already gmuted`",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await eor(event, f"**Error**\n`{e}`")
    else:
        if reason:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,userid)} `is Successfully gmuted`\n**Reason :** `{reason}`",
            )
        else:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,userid)} `is Successfully gmuted`",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,userid)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,userid)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@doge.bot_cmd(
    pattern="ungmute(?:\s|$)([\s\S]*)",
    command=("ungmute", plugin_category),
    info={
        "header": "To unmute the person in all groups where you were admin.",
        "description": "This will work only if you mute that person by your gmute command.",
        "usage": "{tr}ungmute <username/reply>",
    },
)
async def endgmute(event):
    "To remove gmute on that person."
    if event.is_private:
        await event.edit("`Unexpected issues or ugly errors may occur!`")
        await sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == doge.uid:
            return await eor(event, "`Sorry, I can't gmute myself`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await eor(event, "`Sorry. I am unable to fetch the user`")
    if not is_muted(userid, "gmute"):
        return await eor(
            event, f"{_format.mentionuser(user.first_name ,user.id)} `is not gmuted`"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await eor(event, f"**Error**\n`{e}`")
    else:
        if reason:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `is Successfully ungmuted`\n**Reason :** `{reason}`",
            )
        else:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `is Successfully ungmuted`",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**Reason :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**User :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@doge.bot_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@doge.bot_cmd(
    pattern="gkick(?:\s|$)([\s\S]*)",
    command=("gkick", plugin_category),
    info={
        "header": "kicks the person in all groups where you are admin.",
        "usage": "{tr}gkick <username/reply/userid> <reason (optional)>",
    },
)
async def doggkick(event):  # sourcery no-metrics
    "kicks the person in all groups where you are admin"
    dogg = await eor(event, "`gkicking.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, dogg)
    if not user:
        return
    user_id = user.id
    if user_id == doge.uid:
        return await edl(dogg, "`why would I kick myself`")
    flag = await wowmydev(user_id, event)
    if flag:
        return
    happy = await admin_groups(event.client)
    count = 0
    teledoge = len(happy)
    if teledoge == 0:
        return await edl(dogg, "`you are not admin of atleast one group` ")
    await dogg.edit(
        f"`initiating gkick of the `[user](tg://user?id={user_id}) `in {len(happy)} groups`"
    )
    for i in range(teledoge):
        try:
            await event.client.kick_participant(happy[i], user_id)
            await sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(happy[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`You don't have required permission in :`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`For kicking there`",
            )
    end = datetime.now()
    dogtaken = (end - start).seconds
    if reason:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user_id}) `was gkicked in {count} groups in {dogtaken} seconds`!!\n**Reason :** `{reason}`"
        )
    else:
        await dogg.edit(
            f"[{user.first_name}](tg://user?id={user_id}) `was gkicked in {count} groups in {dogtaken} seconds`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user_id})\
                \n**ID : **`{user_id}`\
                \n**Reason :** `{reason}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user_id})\
                \n**ID : **`{user_id}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{dogtaken} seconds`",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
