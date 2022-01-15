# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import os
from time import time

from heroku3 import from_key
from requests import get as request_get
from spamwatch import Client as spamwclient
from validators.url import url as validatorsurl

from .Config import Config
from .core.logger import logging
from .core.session import doge
from .sql_helper.globals import dgvar, gvar, sgvar

__version__ = "1.0"
__license__ = "🔐 GNU Affero Genel Kamu Lisansı v3.0"
__author__ = "DOG-E < https://github.com/DOG-E/DogeUserBot >"
__copyright__ = "©️ Copyright 2021, " + __author__

doge.version = __version__
if gvar("BOT_TOKEN"):
    doge.bot.version = __version__

LOGS = logging.getLogger("DogeUserBot")

StartTime = time()
dogeversion = "1.0"


if Config.UPSTREAM_REPO == "DOGE-TR":
    UPSTREAM_REPO_URL = "https://github.com/DOG-E/DogeUserBot"
else:
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
        Config.BOTLOG_CHATID = int("-" + str(Config.PRIVATE_GROUP_BOT_API_ID))
    else:
        Config.BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
    Config.BOTLOG = True


if Config.PM_LOGGER_GROUP_ID == 0:
    if gvar("PM_LOGGER_GROUP_ID") is None:
        Config.PM_LOGGER_GROUP_ID = -100
    else:
        Config.PM_LOGGER_GROUP_ID = int(gvar("PM_LOGGER_GROUP_ID"))
elif str(Config.PM_LOGGER_GROUP_ID)[0] != "-":
    Config.PM_LOGGER_GROUP_ID = int("-" + str(Config.PM_LOGGER_GROUP_ID))


if gvar("TAG_LOGGER_GROUP_ID"):
    TAG_LOGGER_GROUP = gvar("TAG_LOGGER_GROUP_ID")
else:
    TAG_LOGGER_GROUP = Config.PM_LOGGER_GROUP_ID


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = from_key(Config.HEROKU_API_KEY).apps()[Config.HEROKU_APP_NAME]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# GLOBALS:
CMD_HELP = {}
CMD_LIST = {}
LOAD_PLUG = {}
SUDO_LIST = {}


# OWNER:
hmention = f"<a href = tg://user?id={int(gvar('OWNER_ID'))}>{gvar('ALIVE_NAME')}</a>"
mention = f"[{gvar('ALIVE_NAME')}](tg://user?id={int(gvar('OWNER_ID'))})"


# VARIABLES:
tr = gvar("CMDSET") or "."


# CHANNEL & GROUP IDS:
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
PM_LOGGER_GROUP_ID = Config.PM_LOGGER_GROUP_ID


# API VARS:
G_DRIVE_FOLDER_ID = gvar("G_DRIVE_FOLDER_ID")

if gvar("SPAMWATCH_API"):
    token = gvar("SPAMWATCH_API")
    SPAMWATCH = spamwclient(token)
else:
    SPAMWATCH = None


# HEROKU:
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
Heroku = from_key(HEROKU_API_KEY)


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
