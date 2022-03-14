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

from . import doge, logging, tr
from .utils import (
    checkid_setme,
    customize_assistantbot,
    load_plugins,
    setup_assistantbot,
    setup_bot,
    start_assistantbot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("DogeUserBot")


try:
    LOGS.info("🐾 %10 ~ BAŞLATILIYOR...")
    doge.loop.run_until_complete(setup_bot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %20 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(checkid_setme())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %30 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(setup_assistantbot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %40 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(start_assistantbot())
except Exception as e:
    LOGS.error(f"🚨 {e}")

try:
    LOGS.info("🐾 %50 ~ YÜKLENİYOR...")
    doge.loop.run_until_complete(customize_assistantbot())
except Exception as e:
    LOGS.error(f"🚨 {e}")


async def startup_process():
    LOGS.info("🐾 %60 ~ YÜKLENİYOR...")
    await verifyLoggerGroup()

    LOGS.info("🐾 %70 ~ PLUGINLER YÜKLENİYOR...")
    await load_plugins("plugins")

    LOGS.info("🐾 %80 ~ ASİSTAN BAŞLATILIYOR...")
    await load_plugins("assistant")

    LOGS.info("🐾 %90 ~ YÜKLENİYOR...")
    await startupmessage()
    await sleep(3)

    LOGS.info("🐶 %100 ~ DOGE USERBOT HAZIR!\n\n\n\n\n\n\n")
    LOGS.info(userbot.__copyright__)
    LOGS.info(f"{userbot.__license__} ile korunmaktadır.")
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
    return


doge.loop.run_until_complete(startup_process())


if len(argv) in {1, 3, 4}:
    try:
        doge.run_until_disconnected()
    except ConnectionError:
        pass
else:
    doge.disconnect()
