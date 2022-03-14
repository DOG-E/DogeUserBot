# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import os
from signal import SIGTERM, signal
from sys import exit
from time import time

from heroku3 import from_key
from requests import get as request_get
from validators.url import url as validatorsurl

from .Config import Config
from .core.logger import logging
from .core.session import doge
from .helpers.utils.utils import runasync
from .sql_helper.globals import dgvar, gvar, sgvar

__version__ = "1.0"
__license__ = "🔐 GNU Affero Genel Kamu Lisansı v3.0"
__author__ = "DOG-E < https://github.com/DOG-E/DogeUserBot >"
__copyright__ = f"©️ Copyright 2021, {__author__}"

doge.version = __version__
if gvar("BOT_TOKEN"):
    doge.bot.version = __version__

LOGS = logging.getLogger("DogeUserBot")

StartTime = time()
dogeversion = "1.0"


def close_connection(*_):
    LOGS.info("🙁 Doge kapanıyor...")
    runasync(doge.disconnect())
    exit(143)


signal(SIGTERM, close_connection)


UPSTREAM_REPO_URL = Config.UPSTREAM_REPO


if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    if gvar("PRIVATE_GROUP_BOT_API_ID") is None:
        Config.BOTLOG = False
        Config.BOTLOG_CHATID = "me"
    else:
        Config.BOTLOG_CHATID = int(gvar("PRIVATE_GROUP_BOT_API_ID"))
        Config.PRIVATE_GROUP_BOT_API_ID = int(gvar("PRIVATE_GROUP_BOT_API_ID"))
        Config.BOTLOG = True
else:
    if str(Config.PRIVATE_GROUP_BOT_API_ID)[0] != "-":
        Config.BOTLOG_CHATID = int(f"-{str(Config.PRIVATE_GROUP_BOT_API_ID)}")
    else:
        Config.BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
    Config.BOTLOG = True


if Config.PM_LOGGER_GROUP_ID == 0:
    if gvar("PM_LOGGER_GROUP_ID") is None:
        Config.PM_LOGGER_GROUP_ID = -100
    else:
        Config.PM_LOGGER_GROUP_ID = int(gvar("PM_LOGGER_GROUP_ID"))
elif str(Config.PM_LOGGER_GROUP_ID)[0] != "-":
    Config.PM_LOGGER_GROUP_ID = int(f"-{str(Config.PM_LOGGER_GROUP_ID)}")


TAG_LOGGER_GROUP = gvar("TAG_LOGGER_GROUP_ID") or Config.PM_LOGGER_GROUP_ID


# HEROKU:
try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = from_key(Config.HEROKU_API_KEY).apps()[Config.HEROKU_APP_NAME]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None

HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME


# GLOBALS:
CMD_HELP = {}
CMD_LIST = {}
LOAD_PLUG = {}
SUDO_LIST = {}


# VARIABLES:
tr = gvar("CMDSET") or "."


# CHANNEL & GROUP IDS:
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
PM_LOGGER_GROUP_ID = Config.PM_LOGGER_GROUP_ID


# DIRECTORIES:
TEMP_DIR = Config.TEMP_DIR
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(TMP_DOWNLOAD_DIRECTORY)

thumb_image_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

if gvar("THUMB_PIC") is not None:
    check = validatorsurl(
        (gvar("THUMB_PIC") or "https://telegra.ph/file/6086da8c041f5de3227ed.jpg")
    )
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(request_get(gvar("THUMB_PIC")).content)
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
