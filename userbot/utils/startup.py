# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
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
from telethon.tl.functions.channels import EditAdminRequest, InviteToChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.help import GetConfigRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import ChatAdminRights

from .. import (
    BOT_USERNAME,
    BOTLOG,
    BOTLOG_CHATID,
    PLUGIN_CHANNEL,
    PM_LOGGER_GROUP_ID,
    tr,
)
from ..Config import Config
from ..core.logger import logging
from ..core.session import doge
from ..helpers.resources import constants
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import dgvar, gvar, sgvar
from .pluginmanager import load_module
from .tools import autobotlog, autopluginch, autopmlog, checkingpmlog

LOGS = logging.getLogger("DogeUserBot")


async def setup_bot():
    """
    Oturuma bağlanır
    """
    try:
        await doge.connect()
        config = await doge(GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == doge.session.server_address:
                if doge.session.dc_id != option.id:
                    LOGS.warning(
                        f"🛠️ Oturumdaki sabit DC Kimliği {doge.session.dc_id}\
                        \n➡️ {option.id}'a düzenlendi.",
                    )
                doge.session.set_dc(option.id, option.ip_address, option.port)
                doge.session.save()
                break
    except Exception as e:
        LOGS.error(f"🚨 [STRING_SESSION] - {e}")
        dgvar("OWNER_ID")
        exit()


async def checking_id():
    """
    Kullanıcı kimliği kontrolü
    """
    doge.me = await doge.get_me()
    doge.uid = doge.me.id
    if gvar("OWNER_ID") is None:
        sgvar("OWNER_ID", str(doge.uid))
    if gvar("OWNER_ID") != doge.uid and gvar("OWNER_ID") is not None:
        LOGS.error(
            "🚨 Kullanıcı değişikliği algıladım. 🔃 Kurulumu yeniden başlatıyorum..."
        )
        dgvar("OWNER_ID")
        dgvar("ALIVE_NAME")
        dgvar("BOT_TOKEN")
        dgvar("PRIVATE_GROUP_BOT_API_ID")
        dgvar("PM_LOGGER_GROUP_ID")
        dgvar("PLUGIN_CHANNEL")
        dgvar("FBAN_GROUP_ID")
        dgvar("PRIVATE_CHANNEL_ID")
        dgvar("TG_2STEP_VERIFICATION_CODE")
        exit()
    if gvar("OWNER_ID") in G_YS:
        f = "https://telegra.ph/file/b7e740bbda31d43d510ab.jpg"
        await doge.send_message("me", constants.sndmsgg_ys, file=f)
        LOGS.error(constants.l_gmsgg_ys)
        await doge.disconnect()
        exit()


async def setup_assistantbot():
    """
    Otoomatik asistan bot kurulumu
    """
    if gvar("BOT_TOKEN"):
        return
    if Config.BOT_TOKEN:
        sgvar("BOT_TOKEN", str(Config.BOT_TOKEN))
        return
    LOGS.info("🦴 Sizin için @BotFather'dan asistan bot oluşturuyorum.")
    if Config.ALIVE_NAME:
        botname = f"🐶 {Config.ALIVE_NAME} Asɪsᴛᴀɴ Boᴛ"
    else:
        botname = f"🐶 {doge.me.first_name} Asɪsᴛᴀɴ Boᴛ"
    if doge.me.username:
        botusername = doge.me.username + "Bot"
    else:
        botusername = "Doge_" + (str(doge.me.id))[5:] + "_Bot"
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
        LOGS.error(
            "🚨 @BotFather ile bir bot oluşturun ve BOT_TOKEN değişkenine ayar yapın ve beni yeniden başlatın."
        )
        exit()

    await doge.send_message(bf, botname)
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    if not is_ok.startswith("Good."):
        await doge.send_message(bf, "🐶 Dᴏɢᴇ Asɪsᴛᴀɴıᴍ")
        await sleep(1)
        is_ok = (await doge.get_messages(bf, limit=1))[0].text
        if not is_ok.startswith("Good."):
            LOGS.error(
                "🚨 @BotFather ile bir bot oluşturun ve BOT_TOKEN değişkenine ayar yapın ve beni yeniden başlatın"
            )
            exit()

    await doge.send_message(bf, botusername)
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    await doge.send_read_acknowledge(bf)
    if is_ok.startswith("Sorry,"):
        ran = randint(1, 100)
        botusername = "Doge_" + (str(doge.uid))[6:] + str(ran) + "_Bot"
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
            await doge.send_message(bf, "🐶 Keşfet...")
            LOGS.info(
                f"✅ Başarılı! @{botusername} Telegram asistanı botunuzu başarıyla oluşturdum!"
            )
        else:
            LOGS.error(
                "🚨 Lütfen @BotFather'dan botlarınızı silin veya bir botun belirteci ile BOT_TOKEN'i ayarlayın."
            )
            exit()

    elif is_ok.startswith("Done!"):
        bottoken = is_ok.split("`")[1]
        sgvar("BOT_TOKEN", bottoken)
        await doge.send_message(bf, "/setinline")
        await sleep(1)
        await doge.send_message(bf, f"@{botusername}")
        await sleep(1)
        await doge.send_message(bf, "🐶 keşfet...")
        LOGS.info(
            f"✅ Başarılı! @{botusername} Telegram asistanı botunuzu başarıyla oluşturdum!"
        )
    else:
        LOGS.error(
            "🚨 Lütfen @BotFather'dan botlarınızı silin veya bir botun belirteci ile BOT_TOKEN'i ayarlayın."
        )
        exit()


async def setup_me_bot():
    """
    Gerekli bazı verileri ayarlar
    """
    if gvar("ALIVE_NAME") is None:
        if Config.ALIVE_NAME:
            sgvar("ALIVE_NAME", str(Config.ALIVE_NAME))
        else:
            sgvar("ALIVE_NAME", str(doge.me.first_name))

    try:
        await doge.tgbot.start(bot_token=gvar("BOT_TOKEN"))
    except Exception as boter:
        LOGS.error(f"🚨 {boter}")
        dgvar("BOT_TOKEN")
        exit()
    doge.tgbot.me = await doge.tgbot.get_me()
    Config.BOT_USERNAME = f"@{doge.tgbot.me.username}"


async def ipchange():
    """
    IP'nin değişip değişmeyeceğini kontrol eder
    """
    newip = (get("https://httpbin.org/ip").json())["origin"]
    if gvar("ipaddress") is None:
        sgvar("ipaddress", newip)
        return None
    oldip = gvar("ipaddress")
    if oldip != newip:
        dgvar("ipaddress")
        LOGS.info("🔄 IP değişimi tespit edildi!")
        try:
            await doge.disconnect()
        except (ConnectionError, CancelledError):
            pass
        return "ip change"


async def load_plugins(folder):
    """
    Eklentileri belirtilen klasörden yükler
    """
    path = f"userbot/{folder}/*.py"
    files = sorted(glob(path))
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
                LOGS.error(str(f"🚨 {e} hatası nedeniyle {shortname} yüklenemedi."))


async def verifyLoggerGroup():
    """
    Kanal ve logger gruplarını doğrular
    """
    flag = False
    a_ = await autobotlog(BOTLOG, BOTLOG_CHATID, Config, doge)
    if a_:
        flag = True

    b_ = await autopmlog(PM_LOGGER_GROUP_ID, Config, doge)
    if b_:
        flag = True

    await checkingpmlog(PM_LOGGER_GROUP_ID, doge)

    c_ = await autopluginch(PLUGIN_CHANNEL, Config, doge)
    if c_:
        flag = True

    if flag:
        executable = sysexecutable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        execle(executable, *args, environ)
        exit(0)


async def add_bot_to_logger_group(chat_id):
    """
    Asistan botu log gruplarına ekler
    """
    try:
        await doge(
            AddChatUserRequest(
                chat_id=chat_id,
                user_id=BOT_USERNAME,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await doge(
                InviteToChannelRequest(
                    channel=chat_id,
                    users=[BOT_USERNAME],
                )
            )
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    try:
        await doge(EditAdminRequest(chat_id, BOT_USERNAME, rights, "Doge"))
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")


async def startupmessage():
    """
    Telegram log grubuna botun başladığına dair mesaj gönderir
    """
    try:
        if BOTLOG:
            Config.DOGELOGO = await doge.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg",
                caption="**🧡 Dᴏɢᴇ UsᴇʀBᴏᴛ Kᴜʟʟᴀɴıᴍᴀ Hᴀᴢıʀ 🧡**",
                buttons=[
                    (Button.inline("🐕‍🦺 Yᴀʀᴅıᴍ", data="mainmenu"),),
                    (Button.inline("🌍 Dɪʟ Dᴇɢ̆ɪşᴛɪʀ", data="lang_menu"),),
                    (Button.url("💬 Dᴇsᴛᴇᴋ", "https://t.me/DogeSup"),),
                    (Button.url("🧩 Pʟᴜɢɪɴ", "https://t.me/DogePlugin"),),
                ],
            )
    except Exception as e:
        LOGS.error(f"🚨 {e}")
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(f"🚨 {e}")
        return None
    try:
        if msg_details:
            await doge.check_testcases()
            message = await doge.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**🐶 Dᴏɢᴇ UsᴇʀBoᴛ Tüᴍ Hızıʏʟᴀ Çᴀʟışıʏoʀ! ⚡️**"
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
        LOGS.error(f"🚨 {e}")
        return None


async def customize_assistantbot():
    """
    Asistanı kişiselleştirir
    """
    try:
        bot = await doge.get_entity(BOT_USERNAME)
        bf = "BotFather"
        if bot.photo is None:
            LOGS.info("🎨 Telegram asistan botunuzu @BotFather ile özelleştiriyorum.")
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
            await doge.send_message(bf, BOT_USERNAME)
            await sleep(1)
            await doge.send_file(bf, "userbot/helpers/resources/DogeAssistant.jpg")
            await sleep(2)
            await doge.send_message(bf, "/setabouttext")
            await sleep(1)
            await doge.send_message(bf, BOT_USERNAME)
            await sleep(1)
            await doge.send_message(
                bf,
                f"🧡 {master}'ᴜɴ Asɪsᴛᴀɴ Boᴛᴜʏᴜᴍ\n\
                \n🐶 @DogeUserBot'ᴛᴀɴ ❤️ İʟᴇ Oʟᴜşᴛᴜʀᴜʟᴅᴜ 🐾",
            )
            await sleep(1.5)
            await doge.send_message(bf, "/setdescription")
            await sleep(1)
            await doge.send_message(bf, BOT_USERNAME)
            await sleep(1)
            await doge.send_message(
                bf,
                f"🐕‍🦺 Doɢᴇ UsᴇʀBoᴛ Asɪsᴛᴀɴ Boᴛᴜ\
                \n🧡 Sᴀʜɪᴘ: {master}\n\
                \n🐶 @DogeUserBot'ᴛᴀɴ ❤️ İʟᴇ Oʟᴜşᴛᴜʀᴜʟᴅᴜ 🐾",
            )
            await sleep(1.5)
            await doge.send_message(bf, "/setcommands")
            await sleep(1)
            await doge.send_message(bf, BOT_USERNAME)
            await sleep(1)
            await doge.send_message(
                bf,
                "start - 🐶 Botunuzu Başlatın\
                \nyardim - 🐾 Yardım Menüsü\
                \nkbilgi - ℹ️ Botu kullanan kişilerin bilgileri\
                \nyasakla - ⛔ Kullanıcıyı bottan yasaklama\
                \nyasakac - 🔰 Kullanıcının yasağını kaldırma\
                \nyayin - 📣 Kullanıcılara yayın yapın",
            )
            LOGS.info(
                f"✅ Başarılı! {BOT_USERNAME} Telegramda asistan botunuzu özelleştirdim!"
            )
    except Exception as e:
        LOGS.warning(f"🚨 {str(e)}")
