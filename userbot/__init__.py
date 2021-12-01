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
    doge.tgbot.version = __version__

LOGS = logging.getLogger("DogeUserBot")
bot = doge

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
ALIVE_NAME = gvar("ALIVE_NAME")
AUTONAME = gvar("AUTONAME")

BIO_PREFIX = gvar("BIO_PREFIX")
DEFAULT_BIO = (gvar("DEFAULT_BIO") or "🐶 @DogeUserBot 🐾")

OWNER_ID = (gvar("OWNER_ID") or doge.uid)
mention = f"[{gvar('ALIVE_NAME')}](tg://user?id={OWNER_ID})"
hmention = f"<a href = tg://user?id={OWNER_ID}>{gvar('ALIVE_NAME')}</a>"

TELEGRAPH_SHORT_NAME = (gvar("TELEGRAPH_SHORT_NAME") or "@DogeUserBot")


# VARIABLES:
CHANGE_TIME = (gvar("CHANGE_TIME") or "60")
tr = (gvar("CMDSET") or ".")


# ASSISTANT BOT:
BOT_USERNAME = Config.BOT_USERNAME


# CHANNEL & GROUP IDS:
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
FBAN_GROUP_ID = (
    gvar("FBAN_GROUP_ID") if gvar("FBAN_GROUP_ID") is not None else BOTLOG_CHATID
)
PLUGIN_CHANNEL = gvar("PLUGIN_CHANNEL")
PM_LOGGER_GROUP_ID = gvar("PM_LOGGER_GROUP_ID")
PRIVATE_CHANNEL_ID = (gvar("PRIVATE_CHANNEL_ID") or "me")


# API VARS:
ANTISPAMBOT_BAN = gvar("ANTISPAMBOT_BAN")

CURRENCY_API = gvar("CURRENCY_API")

DEEPAI_API = gvar("DEEPAI_API")

G_DRIVE_CLIENT_ID = gvar("G_DRIVE_CLIENT_ID")
G_DRIVE_CLIENT_SECRET = gvar("G_DRIVE_CLIENT_SECRET")
G_DRIVE_DATA = gvar("G_DRIVE_DATA")
G_DRIVE_FOLDER_ID = gvar("G_DRIVE_FOLDER_ID")
G_DRIVE_INDEX_LINK = gvar("G_DRIVE_INDEX_LINK")

GENIUS_API = gvar("GENIUS_API")

GITHUB_ACCESS_TOKEN = gvar("GITHUB_ACCESS_TOKEN")
GIT_REPO_NAME = gvar("GIT_REPO_NAME")

IBM_WATSON_CRED_URL = gvar("IBM_WATSON_CRED_URL")
IBM_WATSON_CRED_PASSWORD = gvar("IBM_WATSON_CRED_PASSWORD")

IPDATA_API = gvar("IPDATA_API")

LASTFM_API = gvar("LASTFM_API")
LASTFM_SECRET = gvar("LASTFM_SECRET")
LASTFM_USERNAME = gvar("LASTFM_USERNAME")
LASTFM_PASSWORD_PLAIN = gvar("LASTFM_PASSWORD_PLAIN")

OCRSPACE_API = gvar("OCRSPACE_API")

RANDOMSTUFF_API = gvar("RANDOMSTUFF_API")

REMOVEBG_API = gvar("REMOVEBG_API")

if gvar("SPAMWATCH_API"):
    token = gvar("SPAMWATCH_API")
    SPAMWATCH = spamwclient(token)
else:
    SPAMWATCH = None

SPOTIFY_DC = gvar("SPOTIFY_DC")
SPOTIFY_KEY = gvar("SPOTIFY_KEY")

SS_API = gvar("SS_API")

TG_2STEP_VERIFICATION_CODE = gvar("TG_2STEP_VERIFICATION_CODE")

WATCH_COUNTRY = gvar("WATCH_COUNTRY")

WEATHER_API = (gvar("WEATHER_API") or "6fded1e1c5ef3f394283e3013a597879")
WEATHER_CITY = (gvar("WEATHER_CITY") or "Istanbul")


# PM:
PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD


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

if gvar("THUMB_IMAGE") is not None:
    check = validatorsurl((gvar("THUMB_IMAGE") or "https://telegra.ph/file/6086da8c041f5de3227ed.jpg"))
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(request_get(gvar("THUMB_IMAGE")).content)
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
