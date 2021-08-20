from asyncio.exceptions import CancelledError
from datetime import timedelta
from glob import glob
from os import environ, execle, path as osp, remove
from pathlib import Path
from sqlite3 import connect
from sys import executable as sysexecutable, exit as sysexit

from requests import get
from telethon import Button
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.help import GetConfigRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import User
from telethon.utils import get_peer_id

from .. import (
    BOTLOG,
    BOTLOG_CHATID,
    G_YS,
    M_STERS,
    PLUGIN_CHANNEL,
    PM_LOGGER_GROUP_ID,
    tr
)
from ..Config import Config
from ..core.logger import logging
from ..core.session import doge
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
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
                        f"Fixed DC ID in session from {doge.session.dc_id}"
                        f" to {option.id}"
                    )
                doge.session.set_dc(option.id, option.ip_address, option.port)
                doge.session.save()
                break
        lm_sters()
        lg_ys()

        try:
            doge(JoinChannelRequest("@DogeUserBot"))
            if gvarstatus("AUTOUS") is None:
                try: doge(JoinChannelRequest("@DogeSup"))
                except: pass
                try: doge(JoinChannelRequest("@DogePlugin"))
                except: pass
        except: pass

        bot_details = await doge.tgbot.get_me()
        Config.BOT_USERNAME = f"@{bot_details.username}"
        # await doge.start(bot_token=Config.BOT_USERNAME)
        doge.me = await doge.get_me()
        doge.uid = doge.tgbot.uid = get_peer_id(doge.me)

        if Config.OWNER_ID == 0:
            Config.OWNER_ID = get_peer_id(doge.me)

        if Config.ALIVE_NAME is None:
            Config.ALIVE_NAME = doge.me.first_name

        if Config.OWNER_ID in G_YS:
            doge.send_message(
                "me",
                f"\
                **🦮 SORRY DUDE!\
                \n💔 I won't work with you.\
                \n🐶 My admins have banned you from using @DogeUserBot!\
                \n\
                \n💡 To find out why,\
                \n🤡 Check out @DogeGays\
                \n\
                \n🌪 To appeal,\
                \n💬 You can write to my @DogeSup group.**\
                ",
                file="https://telegra.ph/file/b7e740bbda31d43d510ab.jpg",
            )
            LOGS.error("🐶 My admins have banned you from using @DogeUserBot!\n🐾 Check your saved messages!")
            doge.disconnect()
            sysexit(1)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {e}")
        sysexit()


async def ipchange():
    """
    Just to check if ip change or not
    """
    newip = (get("https://httpbin.org/ip").json())["origin"]
    if gvarstatus("ipaddress") is None:
        addgvar("ipaddress", newip)
        return None
    oldip = gvarstatus("ipaddress")
    if oldip != newip:
        delgvar("ipaddress")
        LOGS.info("IP change detected")
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
                LOGS.error(f"Unable to load {shortname} because of error {e}")


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await doge.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID can't be found. Make sure it's correct."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID is unsupported. Make sure it's correct."
            )
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = (
            "**🚧 DON'T LEAVE OR\
            \n🚧 DON'T DELETE OR\
            \n🚧 DON'T CHANGE THIS GROUP!**\n\
            \n\
            ⛔ If you change or delete group,\n\
            all your previous snips, welcome, etc. will be lost.\n\
            \n\
            **🧡 @DogeUserBot**"
        )
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        _, groupid = await create_supergroup(
            "🐾 Doɢᴇ Boᴛ Loɢ", doge, Config.BOT_USERNAME, descript, gphoto
        )
        msg = await doge.send_message(groupid, descript)
        await msg.pin()
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print(
            "Private Group for PRIVATE_GROUP_BOT_API_ID is created successfully and added to vars."
        )
        flag = True

    if PLUGIN_CHANNEL == 0:
        descript = (
            "**🚧 DON'T LEAVE OR\
            \n🚧 DON'T DELETE OR\
            \n🚧 DON'T CHANGE THIS CHANNEL!**\n\
            \n\
            ⛔ If you change or delete group,\n\
            all your installed externally plugins will be lost.\n\
            \n\
            **🧡 @DogeUserBot**"
        )
        cphoto = await doge.upload_file(file="userbot/helpers/resources/DogePlugin.jpg")
        _, channelid = await create_channel(
            "🐾 Doɢᴇ Exᴛᴇʀɴᴀʟ Pʟᴜɢɪɴs", doge, descript, cphoto
        )
        msg = await doge.send_message(channelid, descript)
        await msg.pin()
        addgvar("PLUGIN_CHANNEL", channelid)
        print(
            "Private Channel for PLUGIN_CHANNEL is created successfully and added to vars."
        )
        flag = True

    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await doge.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID can't be found. Make sure it's correct.")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID is unsupported. Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PM_LOGGER_GROUP_ID.\n"
                + str(e)
            )

    if flag:
        executable = sysexecutable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        execle(executable, *args, environ)
        sysexit(0)


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
                caption="**🧡 Doɢᴇ UsᴇʀBoᴛ Rᴇᴀᴅʏ To Usᴇ 🧡**",
                buttons=[
                    (
                        Button.inline(
                            f"🐕‍🦺 Hᴇʟᴘ",
                            data="mainmenu",
                        ),
                    ),
                    (
                        Button.inline(
                            f"🌍 Cʜoosᴇ ᴀ Lᴀɴɢᴜᴀɢᴇ",
                            data="lang_menu",
                        ),
                    ),
                    (
                        Button.url("💬 Sᴜᴘᴘoʀᴛ", "https://t.me/DogeSup"),
                        Button.url("🧩 Pʟᴜɢɪɴ", "https://t.me/DogePlugin"),
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
            text = message.text + "\n\n**🐶 Doge is back and alive.**"
            await doge.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
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


def lm_sters():
    try:
        if osp.exists('m_sters.check'):
            remove('m_sters.check')
        URL = (
            'https://raw.githubusercontent.com/MUTLCC/Doge/DOGE/m_sters.check'
        )
        with open('m_sters', 'wb') as load:
            load.write(get(URL).content)
        DB = connect('m_sters.check')
        CURSOR = DB.cursor()
        CURSOR.execute('SELECT * FROM W0W')
        ALL_ROWS = CURSOR.fetchall()
        for i in ALL_ROWS:
            M_STERS.append(i[0])
        DB.close()
    except BaseException:
        pass


def lg_ys():
    try:
        if osp.exists('g_ys.check'):
            remove('g_ys.check')
        URL = (
            'https://raw.githubusercontent.com/MUTLCC/Doge/DOGE/g_ys.check'
        )
        with open('g_ys.check', 'wb') as load:
            load.write(get(URL).content)
        DB = connect('g_ys.check')
        CURSOR = DB.cursor()
        CURSOR.execute('SELECT * FROM G4YS')
        ALL_ROWS = CURSOR.fetchall()
        for i in ALL_ROWS:
            G_YS.append(i[0])
        DB.close()
    except BaseException:
        pass
