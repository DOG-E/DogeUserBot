# Credits: @sandy1709
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from requests import get
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.utils import get_display_name

from ..sql_helper.gban_sql_helper import get_gbanuser, is_gbanned
from ..utils import is_admin
from . import BOTLOG, BOTLOG_CHATID, SPAMWATCH, doge, eor, gvar, logging

plugin_category = "admin"
LOGS = logging.getLogger(__name__)


if gvar("ANTISPAMBOT_BAN") == "True":

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
                    f"[{user.first_name}](tg://user?id={user.id}) `{doggban.reason}` nedeniyle gban olarak yasaklandın."
                )
            else:
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) gban olarak yasaklandın."
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
                    f"[{user.first_name}](tg://user?id={user.id}) `{ban.reason}` nedeniyle SpamWatch tarafından yasaklandı."
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
                reason = f"[Combot anti-spam servisi (CAS)](https://cas.chat/query?u={user.id})"
                hmm = await event.reply(
                    f"[{user.first_name}](tg://user?id={user.id}) {reason} tarafından yasaklandın."
                )
                try:
                    await event.client.edit_permissions(
                        event.chat_id, user.id, view_messages=False
                    )
                    dogbanned = True
                except Exception as e:
                    LOGS.info(e)
        if BOTLOG and dogbanned:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "#ANTISPAMBOT\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Sohbet:** {get_display_name(await event.get_chat())} (`{event.chat_id}`)\n"
                f"**Nedeni:** {hmm.text}",
            )


@doge.bot_cmd(
    pattern="casc$",
    command=("casc", plugin_category),
    info={
        "h": "CAS'ta yasaklanan kullanıcıları kontrol eder.",
        "d": "Bu komutu kullandığınız gruptaki her kullanıcıyı kontrol eder.",
        "u": "{tr}casc",
    },
    groups_only=True,
)
async def caschecker(event):
    "CAS'ta yasaklanan kullanıcıları kontrol eder."
    dogevent = await eor(
        event,
        "`CAS'den (combot antispam servisi) yasaklananları kontrol ediyorum.\
        \nLütfen bekleyin, bu biraz zaman alabilir...`",
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
                    banned_users += f"Silinen hesap `{user.id}`\n"
            members_count += 1
        text = "**Uyarı!** `{}` kullanıcının `{}` tanesi CAS'den yasaklanmış:\n".format(
            members_count,
            cas_count,
        )
        text += banned_users
        if not cas_count:
            text = "Hiçbir kullanıcı CAS'den yasaklanmamış durumda!"
    except ChatAdminRequiredError:
        return await dogevent.edit(
            "`CAS kontrolü yaparken hatayla karşılaştım: Yönetici yetkileri gereklidir!`"
        )
    except BaseException:
        return await dogevent.edit("`CAS kontrolü yaparken hatayla karşılaştım!`")
    await dogevent.edit(text)


@doge.bot_cmd(
    pattern="spamc$",
    command=("spamc", plugin_category),
    info={
        "h": "SpamWatch'ta yasaklanan kullanıcıları kontrol eder.",
        "d": "Bu komutu kullandığınız gruptaki her kullanıcıyı kontrol eder.",
        "u": "{tr}spamc",
    },
    groups_only=True,
)
async def caschecker(event):
    "SpamWatch'ta yasaklanan kullanıcıları kontrol eder."
    text = ""
    dogevent = await eor(
        event,
        "`SpamWatch'dan yasaklananları kontrol ediyorum.\
        \nLütfen bekleyin, bu biraz zaman alabilir...`",
    )
    try:
        info = await event.client.get_entity(event.chat_id)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in event.client.iter_participants(info.id):
            if spamchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"{user.first_name}-`{user.id}`\n"
                else:
                    banned_users += f"Silinen hesap `{user.id}`\n"
            members_count += 1
        text = "**Uyarı!** `{}` kullanıcının `{}` tanesi SpamWatch'dan yasaklanmış:\n".format(
            members_count,
            cas_count,
        )
        text += banned_users
        if not cas_count:
            text = "Hiçbir kullanıcı SpamWatch'dan yasaklanmamış durumda!"
    except ChatAdminRequiredError:
        return await dogevent.edit(
            "`SpamWatch kontrolü yaparken hatayla karşılaştım: Yönetici yetkileri gereklidir!`"
        )
    except BaseException:
        return await dogevent.edit("`SpamWatch kontrolü yaparken hatayla karşılaştım!`")
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
