# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from asyncio.exceptions import CancelledError
from datetime import timedelta
from glob import glob
from os import environ, execle, remove
from pathlib import Path
from random import randint
from sys import executable as sysexecutable
from sys import exit

from pylists import *
from requests import get
from telethon import Button
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.help import GetConfigRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import User
from telethon.utils import get_peer_id

from .. import BOTLOG, BOTLOG_CHATID, PLUGIN_CHANNEL, PM_LOGGER_GROUP_ID, tr
from ..Config import Config
from ..core.logger import logging
from ..core.session import doge
from ..helpers.utils import install_pip
from ..languages import lan
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import dgvar, gvar, sgvar
from .pluginmanager import load_module
from .tools import create_channel, create_supergroup

LOGS = logging.getLogger("DogeUserBot")


async def setup_bot():
    """
    To setup bot for userbot
    """
    try:
        await doge.connect()
        config = await doge(GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == doge.session.server_address:
                if doge.session.dc_id != option.id:
                    LOGS.warning(
                        lan("wrnnfixdcid").format(
                            doge.session.dc_id,
                            option.id,
                        )
                    )
                doge.session.set_dc(option.id, option.ip_address, option.port)
                doge.session.save()
                break
    except Exception as e:
        LOGS.error(f"[STRING_SESSION] - {e}")
        exit()

    if gvar("DOGELANG") is None:
        sgvar("DOGELANG", str(Config.DOGELANG))

    await autous()
    m_e = await doge.get_me()
    m_y_i_d = m_e.id
    if str(m_y_i_d) in G_YS:
        f = "https://telegra.ph/file/b7e740bbda31d43d510ab.jpg"
        await doge.send_message("me", lan("sendmsgg_ys"), file=f)
        LOGS.error(lan("errrg_ysuse"))
        await doge.disconnect()
        exit(1)


async def autous():
    try:
        await doge(JoinChannelRequest("@DogeUserBot"))
        if gvar("AUTOUS") is False:
            return
        else:
            try:
                await doge(JoinChannelRequest("@DogeSup"))
            except BaseException:
                pass
            try:
                await doge(JoinChannelRequest("@DogePlugin"))
            except BaseException:
                pass
    except BaseException:
        pass


async def setup_assistantbot():
    """
    To setup assistant bot
    """
    if Config.BOT_TOKEN:
        sgvar("BOT_TOKEN", str(Config.BOT_TOKEN))
        return
    if gvar("BOT_TOKEN"):
        return
    LOGS.info(lan("creatingabot"))
    my = await doge.get_me()
    botname = f"🐶 {my.first_name}{lan('_abotname')}"
    if my.username:
        botusername = my.username + "_Bot"
    else:
        botusername = "Doge_" + (str(my.id))[5:] + "_Bot"
    bf = "BotFather"
    try:
        await doge.send_message(bf, "/cancel")
    except YouBlockedUserError:
        await doge(UnblockRequest(bf))
        await doge.send_message(bf, "/cancel")
    await sleep(0.5)
    await doge.send_message(bf, "/newbot")
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    if is_ok.startswith("That I cannot do."):
        LOGS.error(lan("errrcreateabot"))
        exit(1)

    await doge.send_message(bf, botname)
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    if not is_ok.startswith("Good."):
        await doge.send_message(bf, lan("abotname"))
        await sleep(1)
        is_ok = (await doge.get_messages(bf, limit=1))[0].text
        if not is_ok.startswith("Good."):
            LOGS.error(lan("errrcreateabot"))
            exit(1)

    await doge.send_message(bf, botusername)
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    await doge.send_read_acknowledge(bf)
    if is_ok.startswith("Sorry,"):
        ran = randint(1, 100)
        botusername = "Doge_" + (str(my.id))[6:] + str(ran) + "_Bot"
        await doge.send_message(bf, botusername)
        await sleep(1)
        now_ok = (await doge.get_messages(bf, limit=1))[0].text
        if now_ok.startswith("Done!"):
            bottoken = now_ok.split("`")[1]
            sgvar("BOT_TOKEN", bottoken)
            await doge.send_message(bf, "/setinline")
            await sleep(1)
            await doge.send_message(bf, f"@{botusername}")
            await sleep(1)
            await doge.send_message(bf, lan("abotname"))
            LOGS.info(lan("succ_createabot").format(botusername))
        else:
            LOGS.error(lan("errrmostbot"))
            exit(1)

    elif is_ok.startswith("Done!"):
        bottoken = is_ok.split("`")[1]
        sgvar("BOT_TOKEN", bottoken)
        await doge.send_message(bf, "/setinline")
        await sleep(1)
        await doge.send_message(bf, f"@{botusername}")
        await sleep(1)
        await doge.send_message(bf, lan("abotname"))
        LOGS.info(lan("succ_createabot").format(botusername))
    else:
        LOGS.error(lan("errrmostbot"))
        exit(1)


async def setup_me_bot():
    """
    To setup some necessary data
    """
    doge.me = await doge.get_me()
    doge.uid = doge.me.id

    if Config.OWNER_ID == 0:
        Config.OWNER_ID = get_peer_id(doge.me)

    if gvar("ALIVE_NAME") is None:
        if Config.ALIVE_NAME:
            sgvar("ALIVE_NAME", str(Config.ALIVE_NAME))
        else:
            my_first_name = doge.me.first_name
            sgvar("ALIVE_NAME", my_first_name)

    await doge.tgbot.start(bot_token=gvar("BOT_TOKEN"))
    doge.tgbot.me = await doge.tgbot.get_me()
    bot_details = doge.tgbot.me
    Config.BOT_USERNAME = f"@{bot_details.username}"


async def ipchange():
    """
    Just to check if ip change or not
    """
    newip = (get("https://httpbin.org/ip").json())["origin"]
    if gvar("ipaddress") is None:
        sgvar("ipaddress", newip)
        return None
    oldip = gvar("ipaddress")
    if oldip != newip:
        dgvar("ipaddress")
        LOGS.info(lan("ipchanged"))
        try:
            await doge.disconnect()
        except (ConnectionError, CancelledError):
            pass
        return "ip change"


async def load_plugins(folder):
    """
    To load plugins from the mentioned folder
    """
    path = f"userbot/{folder}/*.py"
    files = glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                shortname.replace(".py", ""),
                                plugin_path=f"userbot/{folder}",
                            )
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    remove(Path(f"userbot/{folder}/{shortname}.py"))
            except Exception as e:
                remove(Path(f"userbot/{folder}/{shortname}.py"))
                LOGS.error(str(lan("errrlplugin").format(shortname, e)))


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    odogeubc = "🧡 @DogeUserBot"
    if BOTLOG:
        vinfo = "PRIVATE_GROUP_BOT_API_ID"
        try:
            entity = await doge.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.error(lan("errrglogsendmp").format(vinfo))
                if entity.default_banned_rights.invite_users:
                    LOGS.error(lan("errrglogaddup").format(vinfo))
        except ValueError:
            LOGS.error(lan("errrglogid").format(vinfo))
        except TypeError:
            LOGS.error(lan("errrglogunsup").format(vinfo))
        except Exception as e:
            LOGS.error(f"{lan('errrglog').format(vinfo)}\n{str(e)}")
    else:
        descript = f"{lan('dontdelgroup')}{lan('ifdel')}{lan('ifdelbotlog')}{odogeubc}"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        _, groupid = await create_supergroup(
            f"🐾 Doɢᴇ Boᴛ {lan('_log')}", doge, Config.BOT_USERNAME, descript, gphoto
        )
        descmsg = f"{lan('dontdelgroupmsg')}\n\
        \n{lan('ifdel')}{lan('ifdelbotlog')}**{odogeubc}**"
        msg = await doge.send_message(groupid, descmsg)
        await msg.pin()
        sgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        vinfo = "PRIVATE_GROUP_BOT_API_ID"
        LOGS.info(lan("succ_cglog").format(vinfo))
        flag = True

    if Config.PMLOGGER:
        if PM_LOGGER_GROUP_ID != -100 or gvar("PM_LOGGER_GROUP_ID"):
            return
        descript = f"{lan('dontdelgroup')}{lan('ifdel')}{lan('ifdelpmlog')}{odogeubc}"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogePmLog.jpg")
        _, groupid = await create_supergroup(
            f"🐾 Doɢᴇ Pᴍ {lan('_log')}", doge, Config.BOT_USERNAME, descript, gphoto
        )
        descmsg = f"{lan('dontdelgroupmsg')}\n\
        \n{lan('ifdel')}{lan('ifdelpmlog')}{lan('ifdelgorc')}\
        \n`.setvar PMLOGGER False`\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(groupid, descmsg)
        await msg.pin()
        sgvar("PM_LOGGER_GROUP_ID", groupid)
        vinfo = "PM_LOGGER_GROUP_ID"
        LOGS.info(lan("succ_cglog").format(vinfo))
        flag = True

    if PM_LOGGER_GROUP_ID != -100:
        vinfo = "PM_LOGGER_GROUP_ID"
        try:
            entity = await doge.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.error(lan("errrglogsendmp").format(vinfo))
                if entity.default_banned_rights.invite_users:
                    LOGS.error(lan("errrglogaddup").format(vinfo))
        except ValueError:
            LOGS.error(lan("errrglogid").format(vinfo))
        except TypeError:
            LOGS.error(lan("errrglogunsup").format(vinfo))
        except Exception as e:
            LOGS.error(f"{lan('errrglog').format(vinfo)}\n{str(e)}")

    if Config.PLUGINS:
        if PLUGIN_CHANNEL or gvar("PLUGIN_CHANNEL"):
            return
        descript = f"{lan('dontdelgroup')}{lan('ifdel')}{lan('ifdelextrap')}{odogeubc}"
        cphoto = await doge.upload_file(
            file="userbot/helpers/resources/DogeExtraPlugin.jpg"
        )
        _, channelid = await create_channel(
            f"🐾 Doɢᴇ {lan('_extraplugins')}", doge, descript, cphoto
        )
        descmsg = f"{lan('dontdelgroupmsg')}\n\
        \n{lan('ifdel')}{lan('ifdelextrap')}{lan('ifdelgorc')}\
        \n`.setvar PLUGINS False`\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(channelid, descmsg)
        await msg.pin()
        sgvar("PLUGIN_CHANNEL", channelid)
        LOGS.info(lan("succ_cextrap"))
        flag = True

    if flag:
        executable = sysexecutable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        execle(executable, *args, environ)
        exit(0)


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await doge.tgbot.get_me()
    try:
        await doge(
            AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await doge(
                InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def startupmessage():
    """
    Start up message in Telegram logger group
    """
    try:
        if BOTLOG:
            Config.DOGELOGO = await doge.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg",
                caption=lan("dogereadyuse"),
                buttons=[
                    (Button.inline(f"🐕‍🦺 {lan('btnhelp')}", data="mainmenu")),
                    (Button.inline(f"🌍 {lan('btnchooselang')}", data="lang_menu")),
                    (
                        Button.url(
                            f"💬 {lan('btnurlsup')}",
                            "https://t.me/DogeSup",
                        ),
                        Button.url(
                            f"🧩 {lan('btnurlplugin')}",
                            "https://t.me/DogePlugin",
                        ),
                    ),
                ],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await doge.check_testcases()
            message = await doge.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + f"\n\n**🐶 Doge {lan('dogebackalive')}**"
            await doge.edit_message(msg_details[0], msg_details[1], text)
            if gvar("restartupdate") is not None:
                await doge.send_message(
                    msg_details[0],
                    f"{tr}ping",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def customize_assistantbot():
    """
    To customize assistant bot
    """
    try:
        bot = await doge.get_entity(doge.tgbot.me.username)
        bf = "BotFather"
        if bot.photo is None:
            LOGS.info(lan("customizeabot"))
            botusername = f"@{doge.tgbot.me.username}"
            if (doge.me.username) is None:
                master = doge.me.first_name
            else:
                master = f"@{doge.me.username}"
            await doge.send_message(bf, "/cancel")
            await sleep(0.5)
            await doge.send_message(bf, "/start")
            await sleep(1)
            await doge.send_message(bf, "/setuserpic")
            await sleep(1)
            await doge.send_message(bf, botusername)
            await sleep(1)
            await doge.send_file(bf, "userbot/helpers/resources/DogeAssistant.jpg")
            await sleep(2)
            await doge.send_message(bf, "/setabouttext")
            await sleep(1)
            await doge.send_message(bf, botusername)
            await sleep(1)
            await doge.send_message(bf, lan("abotabout").format(master))
            await sleep(2)
            await doge.send_message(bf, "/setdescription")
            await sleep(1)
            await doge.send_message(bf, botusername)
            await sleep(1)
            await doge.send_message(bf, lan("abotdesc").format(master))
            LOGS.info(lan("customizedabot").format(botusername))
    except Exception as e:
        LOGS.info(str(e))
