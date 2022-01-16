# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from sys import argv

import userbot

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    HEROKU_APP,
    PM_LOGGER_GROUP_ID,
    dgvar,
    doge,
    gvar,
    logging,
    tr,
)
from .utils import (
    add_bot_to_logger_group,
    checking_id,
    customize_assistantbot,
    ipchange,
    load_plugins,
    setup_assistantbot,
    setup_bot,
    setup_me_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("DogeUserBot")


try:
    LOGS.info("🐾 %5 ~ BAŞLATILIYOR...")
    doge.loop.run_until_complete(setup_bot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %10 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(checking_id())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %20 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(setup_assistantbot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %30 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(setup_me_bot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %40 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(customize_assistantbot())
except Exception as e:
    LOGS.error(f"🚨 {e}")


class DogCheck:
    def __init__(self):
        self.sucess = True


Dogcheck = DogCheck()


async def startup_process():
    check = await ipchange()
    if check is not None:
        Dogcheck.sucess = False
        return

    LOGS.info("🐾 %50 ~ YÜKLENİYOR...")
    if BOTLOG != True:
        await verifyLoggerGroup()

    LOGS.info("🐾 %60 ~ PLUGINLER YÜKLENİYOR...")
    await load_plugins("plugins")

    LOGS.info("🐾 %70 ~ ASİSTAN BAŞLATILIYOR...")
    await load_plugins("assistant")

    LOGS.info("🐾 %80 ~ YÜKLENİYOR...")
    await verifyLoggerGroup()

    LOGS.info("🐾 %90 ~ YÜKLENİYOR...")
    await add_bot_to_logger_group(doge, BOTLOG_CHATID, gvar("BOT_USERNAME"), "Doge")
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(
            doge, PM_LOGGER_GROUP_ID, gvar("BOT_USERNAME"), "Doge"
        )

    await startupmessage()
    LOGS.info("🐶 %100 ~ DOGE USERBOT HAZIR!\n\n\n\n\n\n")
    await sleep(3)

    LOGS.info(userbot.__copyright__)
    LOGS.info(userbot.__license__ + " ile korunmaktadır.")
    LOGS.info(
        f"\
        \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\
        \n🐶 Hey! Doge çalışıyor!\
        \n🐾 Doge UserBot kullanıma hazır.\
        \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\
        \n🔅 Bir sohbete {tr}alive yazarak durumunu kontrol edin.\
        \n🔅 {tr}doge yazarak komutlar hakkında bilgi alabilirsin.\
        \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\
        \n💬 Yardım için Telegram grubumuzu ziyaret edin: t.me/DogeSup\
        \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
    )

    Dogcheck.sucess = True
    return


doge.loop.run_until_complete(startup_process())


if len(argv) not in (1, 3, 4):
    dgvar("ipaddress")
    doge.disconnect()
elif not Dogcheck.sucess:
    if HEROKU_APP is not None:
        dgvar("ipaddress")
        HEROKU_APP.restart()
else:
    try:
        doge.run_until_disconnected()
    except ConnectionError:
        dgvar("ipaddress")
