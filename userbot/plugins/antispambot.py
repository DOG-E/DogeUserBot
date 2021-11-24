# Credits: @sandy1709
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from requests import get
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.utils import get_display_name

from ..sql_helper.gban_sql_helper import get_gbanuser, is_gbanned
from ..utils import is_admin
from . import ANTISPAMBOT_BAN, BOTLOG, BOTLOG_CHATID, SPAMWATCH, doge, eor, lan, logging, tr

plugin_category = "admin"
LOGS = logging.getLogger(__name__)


if ANTISPAMBOT_BAN == True:

    @doge.on(ChatAction())
    async def anti_spambot(event):  # sourcery no-metrics
        if not event.user_joined and not event.user_added:
            return
        user = await event.get_user()
        dogadmin = await is_admin(event.client, event.chat_id, event.client.uid)
        if not dogadmin:
            return
        dogbanned = None
        adder = None
        ignore = None
        if event.user_added:
            try:
                adder = event.action_message.sender_id
            except AttributeError:
                return
        async for admin in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
            if admin.id == adder:
                ignore = True
                break
        if ignore:
            return
        if is_gbanned(user.id):
            doggban = get_gbanuser(user.id)
            if doggban.reason:
                hmm = await event.reply(
                    lan("antispam1").format(user.first_name, user.id, doggban.reason)
                )
            else:
                hmm = await event.reply(
                    lan("anntispam2").format(user.first_name, user.id)
                )
            try:
                await event.client.edit_permissions(
                    event.chat_id, user.id, view_messages=False
                )
                dogbanned = True
            except Exception as e:
                LOGS.info(e)
        if SPAMWATCH and not dogbanned:
            ban = SPAMWATCH.get_ban(user.id)
            if ban:
                hmm = await event.reply(
                lan("antispam3").format(user.first_name, user.id, ban.reason)    
                )
                try:
                    await event.client.edit_permissions(
                        event.chat_id, user.id, view_messages=False
                    )
                    dogbanned = True
                except Exception as e:
                    LOGS.info(e)
        if not dogbanned:
            try:
                casurl = "https://api.cas.chat/check?user_id={}".format(user.id)
                data = get(casurl).json()
            except Exception as e:
                LOGS.info(e)
                data = None
            if data and data["ok"]:
                reason = (
                    lan("antispam4").format(user.id)
                )
                hmm = await event.reply(
                    lan("antispam5").format(user.first_name, user.id, reason)
                )
                try:
                    await event.client.edit_permissions(
                        event.chat_id, user.id, view_messages=False
                    )
                    dogbanned = True
                except Exception as e:
                    LOGS.info(e)
        if BOTLOG and dogbanned:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#ANTISPAMBOT\n"
                f"**{lan('userx')}:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**{lan('chat')}:** {get_display_name(await event.get_chat())} (`{event.chat_id}`)\n"
                f"**{lan('reason')}:** {hmm.text}",
            )


@doge.bot_cmd(
    pattern="casc$",
    command=("casc", plugin_category),
    info={
        "header": lan("casc1"),
        "description": lan("casc2"),
        "usage": "{tr}casc",
    },
    groups_only=True,
)
async def caschecker(event):
    lan("casc3")
    dogevent = await eor(
        event,
        lan("casc4"),
    )
    text = ""
    try:
        info = await event.client.get_entity(event.chat_id)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in event.client.iter_participants(info.id):
            if banchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"{lan('casc5')}`{user.id}`\n"
            members_count += 1
        text = lan("casc6").format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = lan("casc7")
    except ChatAdminRequiredError:
        await dogevent.edit(lan("casc8"))
        return
    except BaseException:
        await dogevent.edit(lan("casc9"))
        return
    await dogevent.edit(text)


@doge.bot_cmd(
    pattern="spamc$",
    command=("spamc", plugin_category),
    info={
        "header": lan("spam1"),
        "description": lan("spam2"),
        "usage": "{tr}spamc",
    },
    groups_only=True,
)
async def caschecker(event):
    lan("spam3")
    text = ""
    dogevent = await eor(
        event,
        lan("spam4"),
    )
    try:
        info = await event.client.get_entity(event.chat_id)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in event.client.iter_participants(info.id):
            if spamchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"{lan('casc5')} `{user.id}`\n"
            members_count += 1
        text = lan("spam5").format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = lan("spam6")
    except ChatAdminRequiredError:
        await dogevent.edit(lan("spam7"))
        return
    except BaseException:
        await dogevent.edit(lan("spam8"))
        return
    await dogevent.edit(text)


def banchecker(user_id):
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    return bool(data and data["ok"])


def spamchecker(user_id):
    ban = SPAMWATCH.get_ban(user_id) if SPAMWATCH else None
    return bool(ban)
