# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from sys import argv

import userbot
from userbot import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID, tr

from .core.logger import logging
from .core.session import doge
from .sql_helper.globals import dgvar
from .utils import add_bot_to_logger_group  # checking_id,
from .utils import (
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
    LOGS.info("⏳ DOGE USERBOT BAŞLATILIYOR 🐾")
    doge.loop.run_until_complete(setup_bot())
    LOGS.info("🐶 DOGE USERBOT BAŞLATILIYOR 🐾")
except Exception as e:
    LOGS.error(f"🚨 {e}")


try:
    # doge.loop.run_until_complete(checking_id())
    doge.loop.run_until_complete(setup_assistantbot())
    doge.loop.run_until_complete(setup_me_bot())
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
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    print(userbot.__copyright__)
    print(userbot.__license__ + " ile korunmaktadır.")
    print(
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
