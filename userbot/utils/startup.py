# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio.tasks import sleep
from datetime import timedelta
from glob import glob
from os import environ, execle, remove
from pathlib import Path
from random import randint
from sys import executable as sysexecutable
from sys import exit

from pylists import *
from telethon import Button
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.functions.help import GetConfigRequest
from telethon.tl.types import InputMessagesFilterPhotos, User
from telethon.utils import get_peer_id

from .. import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID, tr
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
from .tools import create_channel, create_supergroup

LOGS = logging.getLogger("DogeUserBot")


async def setup_bot():
    try:
        await doge.connect()
        async for o in await doge(GetConfigRequest()).dc_options:
            if o.ip_address == doge.session.server_address:
                if doge.session.dc_id != o.id:
                    LOGS.warn(f"🛠️ Oturumdaki DC kimliği {doge.session.dc_id} ➡️ {o.id} olarak düzenlendi.")
                doge.session.set_dc(o.id, o.ip_address, o.port)
                doge.session.save()
                break
    except Exception as e:
        LOGS.error(f"🚨 [STRING_SESSION] - {e}")
        dgvar("OWNER_ID")
        exit()


async def checkid_setme():
    doge.me = await doge.get_me()
    doge.uid = get_peer_id(doge.me)
    if gvar("OWNER_ID") is None:
        try:
            async for msg in doge.iter_messages("DogeStatus", limit=1, filter=InputMessagesFilterPhotos):
                stat = str(str(msg.text).split("@DogeUserBot Kurulumu: ")[1]).split("\n")
            if "`Açık`" in stat:
                sgvar("CACHE_OWNER_ID", int(doge.uid))
            elif "`Kapalı`" in stat:
                exit()
        except Exception as e:
            LOGS.error(f"🚨 {e}")
            exit()
        await sleep(0.5)
    try:
        await sleep(3)
        sgvar("OWNER_ID", int(doge.uid))
        await sleep(0.5)
    except Exception as e:
        LOGS.error(f"🚨 {e}")
    if gvar("CACHE_OWNER_ID") != gvar("OWNER_ID"):
        dgvar("OWNER_ID")
        dgvar("CACHE_OWNER_ID")
        dgvar("ALIVE_NAME")
        dgvar("CACHE_ALIVE_NAME")
        dgvar("BOT_TOKEN")
        dgvar("BOT_USERNAME")
        dgvar("PRIVATE_GROUP_BOT_API_ID")
        dgvar("PM_LOGGER_GROUP_ID")
        dgvar("TAG_LOGGER_GROUP_ID")
        dgvar("PLUGIN_CHANNEL")
        dgvar("FBAN_GROUP_ID")
        dgvar("PRIVATE_CHANNEL_ID")
        dgvar("HLOGGER_ID")
        dgvar("TG_2STEP_VERIFICATION_CODE")
        dgvar("hmention")
        dgvar("mention")
        LOGS.error(
            "🚨 Kullanıcı değişikliği algıladım.\
            \n🔃 Kurulumu yeniden başlatıyorum..."
        )
        executable = sysexecutable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        execle(executable, *args, environ)
        exit(0)
    if gvar("OWNER_ID") in G_YS:
        f = "https://telegra.ph/file/b7e740bbda31d43d510ab.jpg"
        await doge.send_message("me", constants.sndmsgg_ys, file=f)
        LOGS.error(constants.l_gmsgg_ys)
        await doge.disconnect()
        exit()

    if gvar("ALIVE_NAME") is None:
        if Config.ALIVE_NAME:
            sgvar("ALIVE_NAME", str(Config.ALIVE_NAME))
            sgvar("CACHE_ALIVE_NAME", str(Config.ALIVE_NAME))
        else:
            sgvar("ALIVE_NAME", str(doge.me.first_name))
            sgvar("CACHE_ALIVE_NAME", str(doge.me.first_name))
    if (
        gvar("hmention") is None
        or gvar("mention") is None
        or gvar("CACHE_ALIVE_NAME") != gvar("ALIVE_NAME")
    ):
        hmention = (
            f"<a href = tg://user?id={int(gvar('OWNER_ID'))}>{gvar('ALIVE_NAME')}</a>"
        )
        mention = f"[{gvar('ALIVE_NAME')}](tg://user?id={int(gvar('OWNER_ID'))})"
        sgvar("hmention", str(hmention))
        sgvar("mention", str(mention))


async def setup_assistantbot():
    if gvar("BOT_TOKEN"):
        return
    if Config.BOT_TOKEN:
        sgvar("BOT_TOKEN", str(Config.BOT_TOKEN))
        return
    LOGS.info("🦴 Sizin için @BotFather'dan asistan botu oluşturuyorum.")
    botname = f"🐶 {gvar('ALIVE_NAME')} Asɪsᴛᴀɴ Boᴛ" if gvar("ALIVE_NAME") else f"🐶 {doge.me.first_name} Asɪsᴛᴀɴ Boᴛ"
    botusername = f"{doge.me.username}Bot" if doge.me.username else f"Doge_{(str(doge.me.id))[5:]}_Bot"
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
                "🚨 @BotFather ile bir bot oluşturun ve BOT_TOKEN değişkenine ayar yapın ve beni yeniden başlatın."
            )
            exit()

    await doge.send_message(bf, botusername)
    await sleep(1)
    is_ok = (await doge.get_messages(bf, limit=1))[0].text
    await doge.send_read_acknowledge(bf)
    if is_ok.startswith("Sorry,"):
        ran = randint(1, 100)
        botusername = f"Doge_{(str(doge.uid))[6:]}{str(ran)}_Bot"
        await doge.send_message(bf, botusername)
        await sleep(1)
        now_ok = (await doge.get_messages(bf, limit=1))[0].text
        if now_ok.startswith("Done!"):
            bottoken = now_ok.split("`")[1]
            bun = f"@{botusername}"
            sgvar("BOT_TOKEN", bottoken)
            await doge.send_message(bf, "/setinline")
            await sleep(1)
            await doge.send_message(bf, bun)
            await sleep(1)
            await doge.send_message(bf, "🐶 Keşfet...")
            await doge.send_read_acknowledge(bf)
            sgvar("BOT_USERNAME", bun)
            LOGS.info(f"✅ Başarılı! {bun} asistan botunuzu oluşturdum!")
        else:
            LOGS.error(
                "🚨 Lütfen @BotFather'dan botlarınızı silin veya bir botun belirteci ile BOT_TOKEN'i ayarlayın."
            )
            exit()

    elif is_ok.startswith("Done!"):
        bottoken = is_ok.split("`")[1]
        bun = f"@{botusername}"
        sgvar("BOT_TOKEN", bottoken)
        await doge.send_message(bf, "/setinline")
        await sleep(1)
        await doge.send_message(bf, bun)
        await sleep(1)
        await doge.send_message(bf, "🐶 Keşfet...")
        await doge.send_read_acknowledge(bf)
        sgvar("BOT_USERNAME", bun)
        LOGS.info(f"✅ Başarılı! {bun} asistan botunuzu oluşturdum!")
    else:
        LOGS.error(
            "🚨 Lütfen @BotFather'dan botlarınızı silin veya bir botun belirteci ile BOT_TOKEN'i ayarlayın."
        )
        exit()


async def start_assistantbot():
    try:
        await doge.bot.start(bot_token=gvar("BOT_TOKEN"))
    except Exception:
        try:
            if Config.BOT_TOKEN:
                sgvar("BOT_TOKEN", str(Config.BOT_TOKEN))
                await doge.bot.start(bot_token=gvar("BOT_TOKEN"))
        except Exception as e:
            LOGS.error(f"🚨 {e}")
            dgvar("BOT_TOKEN")
            executable = sysexecutable.replace(" ", "\\ ")
            args = [executable, "-m", "userbot"]
            execle(executable, *args, environ)
            exit(0)

    doge.bot.me = await doge.bot.get_me()
    if gvar("BOT_USERNAME") is None:
        sgvar("BOT_USERNAME", f"@{doge.bot.me.username}")


async def load_plugins(folder):
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


async def verifyLoggerGroup():  # sourcery no-metrics
    flag = False
    odogeubc = "🧡 @DogeUserBot"
    if BOTLOG:
        vinfo = "PRIVATE_GROUP_BOT_API_ID"
        try:
            entity = await doge.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.error(
                        f"🚨 Belirtilen {vinfo} için mesaj gönderme izni yok. Lütfen kontrol edin!"
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.error(
                        f"🚨 Belirtilen {vinfo} için üye ekleme izni yok. Lütfen kontrol edin!"
                    )
        except ValueError:
            LOGS.error(f"🚨 {vinfo} değerini bulamadım. Doğruluğundan emin olun.")
        except TypeError:
            LOGS.error(f"🚨 {vinfo} desteklenmiyor. Doğruluğundan emin olun.")
        except Exception as e:
            LOGS.error(
                f"🚨 {vinfo} doğrulanmaya çalışırken bir hata oluştu.\nHATA: {str(e)}"
            )
    else:
        descript = f"🚧 BU GRUBU SİLMEYİN!\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Doge çalışmayacaktır.\n\
        \n{odogeubc}"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        await sleep(0.75)
        _, groupid = await create_supergroup(
            "🐾 Doɢᴇ Boᴛ Loɢ", doge, gvar("BOT_USERNAME"), descript, gphoto, "Doge"
        )
        await sleep(0.75)
        descmsg = f"**🚧 BU GRUBU SİLMEYİN!\
        \n🚧 BU GRUPTAN AYRILMAYIN!\
        \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Doge çalışmayacaktır!\n\
        \n**{odogeubc}**"
        msg = await doge.bot.send_message(groupid, descmsg)
        await sleep(0.25)
        await msg.pin()
        sgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        LOGS.info("✅ PRIVATE_GROUP_BOT_API_ID için özel bir grup başarıyla oluşturdum!")
        flag = True

    if gvar("PMLOGGER") is None and Config.PMLOGGER:
        sgvar("PMLOGGER", "True")
    if gvar("PMLOGGER") == "True":
        if PM_LOGGER_GROUP_ID != -100 or gvar("PM_LOGGER_GROUP_ID"):
            vinfo = "PM_LOGGER_GROUP_ID"
            try:
                entity = await doge.get_entity(PM_LOGGER_GROUP_ID)
                if not isinstance(entity, User) and not entity.creator:
                    if entity.default_banned_rights.send_messages:
                        LOGS.error(
                            f"🚨 Belirtilen {vinfo} için mesaj gönderme izni eksik. Doğruluğundan emin olun!"
                        )
                    if entity.default_banned_rights.invite_users:
                        LOGS.error(
                            f"🚨Belirtilen {vinfo} için üye ekleme izni eksik. Doğruluğundan emin olun!"
                        )
            except ValueError:
                LOGS.error(f"🚨 {vinfo} değerini bulamadım. Doğruluğundan emin olun.")
            except TypeError:
                LOGS.error(f"🚨 {vinfo} desteklenmiyor. Doğruluğundan emin olun.")
            except Exception as e:
                LOGS.error(
                    f"🚨 {vinfo} doğrulanmaya çalışırken bir hata oluştu.\nHATA: {str(e)}"
                )
        else:
            descript = f"🚧 BU GRUBU SİLMEYİN!\n\
            \n🗑 Eğer silerseniz,\
            \n🚫 PM Logger çalışmayacaktır.\n\
            \n{odogeubc}"
            gphoto = await doge.upload_file(
                file="userbot/helpers/resources/DogePmLog.jpg"
            )
            await sleep(0.75)
            _, groupid = await create_supergroup(
                "🐾 Doɢᴇ Pᴍ Loɢ", doge, gvar("BOT_USERNAME"), descript, gphoto, "Doge"
            )
            await sleep(0.75)
            descmsg = f"**🚧 BU GRUBU SİLMEYİN!\
            \n🚧 BU GRUPTAN AYRILMAYIN!\
            \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
            \n🗑 Eğer bu grubu silerseniz,\
            \n🚫 PM Logger özelliği çalışmayacaktır.\n\
            \n**🦴 EĞER GRUBU SİLMEK İSTERSENİZ,\
            \n🔅 İLK ÖNCE ŞUNU YAZIN:**\
            \n`.sdog PMLOGGER False`\n\
            \n**{odogeubc}**"
            msg = await doge.bot.send_message(groupid, descmsg)
            await sleep(0.25)
            await msg.pin()
            sgvar("PM_LOGGER_GROUP_ID", groupid)
            LOGS.info("✅ PM_LOGGER_GROUP_ID için özel bir grup başarıyla oluşturdum!")
            flag = True

    if gvar("PLUGINS") is None and Config.PLUGINS:
        sgvar("PLUGINS", "True")
    if gvar("PLUGINS") == "True" and gvar("PLUGIN_CHANNEL") is None:
        descript = f"🚧 BU KANALI SİLMEYİN!\n\
        \n🗑 Eğer bu kanalı silerseniz,\
        \n🧩 yüklenen tüm ekstra pluginler silinecektir.\n\
        \n{odogeubc}"
        cphoto = await doge.upload_file(
            file="userbot/helpers/resources/DogeExtraPlugin.jpg"
        )
        await sleep(0.75)
        _, channelid = await create_channel(
            "🐾 Doɢᴇ Eᴋsᴛʀᴀ Pʟᴜɢɪɴʟᴇʀ", doge, descript, cphoto
        )
        await sleep(0.75)
        descmsg = f"**🚧 BU KANALI SİLMEYİN!\
        \n🚧 BU KANALDAN AYRILMAYIN!\
        \n🚧 BU KANALDA DEĞİŞİKLİK YAPMAYIN!**\n\
        \n🗑 Eğer silerseniz,\
        \n🧩 yüklenen tüm ekstra pluginler silinecektir.\n\
        \n**🦴 EĞER KANALI SİLMEK İSTERSENİZ,\
        \n🔅 İLK ÖNCE ŞUNU YAZIN:**\
        \n`.sdog PLUGINS False`\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(channelid, descmsg)
        await sleep(0.25)
        await msg.pin()
        sgvar("PLUGIN_CHANNEL", channelid)
        LOGS.info("✅ PLUGIN_CHANNEL için özel bir kanal başarıyla oluşturuldum!")
        flag = True

    if flag:
        executable = sysexecutable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        execle(executable, *args, environ)
        exit(0)


async def startupmessage():
    try:
        if BOTLOG:
            Config.DOGELOGO = await doge.bot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg",
                caption="**🧡 Dᴏɢᴇ UsᴇʀBᴏᴛ Kᴜʟʟᴀɴɪᴍᴀ Hᴀᴢɪʀ 🧡**",
                buttons=[
                    (Button.inline("🐕‍🦺 Yᴀʀᴅɪᴍ", data="backmainmenu"),),
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
            await doge.edit_message(
                msg_details[0], msg_details[1], "**🐶 Dᴏɢᴇ UsᴇʀBoᴛ Gᴇʀɪ Gᴇʟᴅɪ 🐾**"
            )
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
    try:
        if doge.bot.me.photo:
            return
        DOG = gvar("BOT_USERNAME")
        LOGS.info(f"🎨 {DOG} asistan botunuzu @BotFather ile özelleştiriyorum.")
        master = doge.me.first_name if not doge.me.username else f"@{doge.me.username}"
        bf = "BotFather"
        await doge.send_message(bf, "/cancel")
        await sleep(0.5)
        await doge.send_message(bf, "/start")
        await sleep(1)
        await doge.send_message(bf, "/setuserpic")
        await sleep(1)
        await doge.send_message(bf, DOG)
        await sleep(1)
        await doge.send_file(bf, "userbot/helpers/resources/DogeAssistant.jpg")
        await sleep(2)
        await doge.send_message(bf, "/setabouttext")
        await sleep(1)
        await doge.send_message(bf, DOG)
        await sleep(1)
        await doge.send_message(
            bf,
            f"🧡 {master}'ᴜɴ Asɪsᴛᴀɴ Boᴛᴜʏᴜᴍ\n\
            \n🐶 @DogeUserBot'ᴛᴀɴ ❤️ İʟᴇ Oʟᴜşᴛᴜʀᴜʟᴅᴜ 🐾",
        )
        await sleep(1.5)
        await doge.send_message(bf, "/setdescription")
        await sleep(1)
        await doge.send_message(bf, DOG)
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
        await doge.send_message(bf, DOG)
        await sleep(1)
        await doge.send_message(
            bf,
            "start - 🐶 Botunuzu Başlatın\
            \nyardim - 🐾 Yardım Menüsü\
            \nayarlar - 🧶 Doge Ayarları\
            \nkbilgi - ℹ️ Botu kullanan kişilerin bilgileri\
            \nyasakla - ⛔ Kullanıcıyı bottan yasakla\
            \nyasakac - 🔰 Kullanıcının yasağını kaldır\
            \nyayin - 📣 Kullanıcılara yayın yapın",
        )
        await sleep(1)
        await doge.send_message(bf, "/setprivacy")
        await sleep(1)
        await doge.send_message(bf, DOG)
        await sleep(1)
        await doge.send_message(bf, "Disable")
        await doge.send_read_acknowledge(bf)
        LOGS.info(f"✅ Başarılı! {DOG} asistan botunuzu özelleştirdim!")
    except Exception as e:
        LOGS.warning(f"🚨 {str(e)}")
