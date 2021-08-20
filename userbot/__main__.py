from sys import argv, exit

import userbot
from userbot import (
    BOTLOG_CHATID,
    HEROKU_APP,
    PM_LOGGER_GROUP_ID,
)
from .core.logger import logging
from .core.session import doge
from .languages.constants import (
    STARTEDUPDOGE,
    STARTINGDOGE,
    STARTUPDOGE,
)
from .utils import (
    add_bot_to_logger_group,
    ipchange,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)


LOGS = logging.getLogger("DogeUserBot")

print(userbot.__copyright__)
print("🔐 Licensed under the terms of the " + userbot.__license__)


try:
    LOGS.info(f"⏳ {STARTINGDOGE} 🐾")
    doge.loop.run_until_complete(setup_bot())
    LOGS.info(f"✅ {STARTUPDOGE} 🐾")
except Exception as e:
    LOGS.error(f"{e}")
    exit()


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
    LOGS.info(STARTEDUPDOGE)
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Dogcheck.sucess = True
    return


doge.loop.run_until_complete(startup_process())


if len(argv) not in (1, 3, 4):
    doge.disconnect()
elif not Dogcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        doge.run_until_disconnected()
    except ConnectionError:
        pass
