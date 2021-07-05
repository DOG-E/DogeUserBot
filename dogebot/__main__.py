# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import sys

from . import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID, __copyright__, __license__

from .Config import Config
from .core.logger import logging
from .core.session import doge
from .utils import (
    add_bot_to_logger_group,
    ipchange,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("DogeUserbot")

print(__copyright__)
print("Licensed under the terms of the " + __license__)

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("Doge is waiking up...")
    doge.loop.run_until_complete(setup_bot())
    LOGS.info("Doge lives!")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()


class CheckDoge:
    def __init__(self):
        self.sucess = True


checkDoge = CheckDoge()


async def startup_process():
    check = await ipchange()
    if check is not None:
        checkDoge.sucess = False
        return
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print("Woof Woof! Doge is living!!!")
    print(
        f"Congratulation, now type {cmdhr}alive to see message if doge is live\
        \nIf you need assistance, come to https://t.me/DogeSup"
    )
    print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    checkDoge.sucess = True
    return


doge.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    doge.disconnect()
elif not checkDoge.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        doge.run_until_disconnected()
    except ConnectionError:
        pass
