# @sandy1709
from requests import get
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.utils import get_display_name

from ..sql_helper.gban_sql_helper import get_gbanuser, is_gbanned
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID, Config, doge, eor, logging, spamwatch

plugin_category = "admin"
LOGS = logging.getLogger(__name__)


if Config.ANTISPAMBOT_BAN:

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
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you for the reason `{doggban.reason}`"
                )
            else:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was gbanned by you"
                )
            try:
                await event.client.edit_permissions(
                    event.chat_id, user.id, view_messages=False
                )
                dogbanned = True
            except Exception as e:
                LOGS.info(e)
        if spamwatch and not dogbanned:
            ban = spamwatch.get_ban(user.id)
            if ban:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by spamwatch for the reason `{ban.reason}`"
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
                    f"[Banned by Combot Anti Spam](https://cas.chat/query?u={user.id})"
                )
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) was banned by Combat anti-spam service(CAS) for the reason check {reason}"
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
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())} (`{event.chat_id}`)\n"
                f"**Reason :** {hmm.text}",
            )


@doge.bot_cmd(
    pattern="casc$",
    command=("casc", plugin_category),
    info={
        "header": "To check the users who are banned in cas",
        "description": "When you use this cmd it will check every user in the group where you used whether \
        he is banned in cas (combat antispam service) and will show there names if they are flagged in cas",
        "usage": "{tr}casc",
    },
    groups_only=True,
)
async def caschecker(event):
    "Searches for cas(combot antispam service) banned users in group and shows you the list"
    dogevent = await eor(
        event,
        "`checking any cas(combot antispam service) banned users here, this may take several minutes too......`",
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
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning!** Found `{}` of `{}` users are CAS Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No CAS Banned users found!"
    except ChatAdminRequiredError:
        await dogevent.edit("`CAS check failed: Admin privileges are required`")
        return
    except BaseException:
        await dogevent.edit("`CAS check failed`")
        return
    await dogevent.edit(text)


@doge.bot_cmd(
    pattern="spamc$",
    command=("spamc", plugin_category),
    info={
        "header": "To check the users who are banned in spamwatch",
        "description": "When you use this command it will check every user in the group where you used whether \
        he is banned in spamwatch federation and will show there names if they are banned in spamwatch federation",
        "usage": "{tr}spamc",
    },
    groups_only=True,
)
async def caschecker(event):
    "Searches for spamwatch federation banned users in group and shows you the list"
    text = ""
    dogevent = await eor(
        event,
        "`checking any spamwatch banned users here, this may take several minutes too......`",
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
                    banned_users += f"Deleted Account `{user.id}`\n"
            members_count += 1
        text = "**Warning! **Found `{}` of `{}` users are spamwatch Banned:\n".format(
            cas_count, members_count
        )
        text += banned_users
        if not cas_count:
            text = "No spamwatch Banned users found!"
    except ChatAdminRequiredError:
        await dogevent.edit("`spamwatch check failed: Admin privileges are required`")
        return
    except BaseException:
        await dogevent.edit("`spamwatch check failed`")
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
    ban = spamwatch.get_ban(user_id) if spamwatch else None
    return bool(ban)
