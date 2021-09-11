# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import makedirs
from os import path as osp

from heroku3 import from_key
from requests import get
from spamwatch import Client as spamwclient
from validators.url import url as validatorsurl

from .. import *
from ..Config import Config
from ..core.logger import logging
from ..core.managers import edl, eor
from ..core.session import doge, tgbot
from ..helpers import *
from ..helpers.utils import _dogetools, _dogeutils, _format, install_pip, reply_id
from ..languages import constants, lan

LOGS = logging.getLogger(__name__)
bot = doge


# OWNER:
ALIVE_NAME = gvar("ALIVE_NAME")
AUTONAME = gvar("AUTONAME")

BIO_PREFIX = gvar("BIO_PREFIX")
DEFAULT_BIO = gvar("DEFAULT_BIO") or "🐶 @DogeUserBot 🐾"

USERID = doge.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
mention = f"[{gvar('ALIVE_NAME')}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{gvar('ALIVE_NAME')}</a>"

TELEGRAPH_SHORT_NAME = Config.TELEGRAPH_SHORT_NAME


# VARIABLES:
CHANGE_TIME = int(gvar("CHANGE_TIME")) or int(60)


# ASSISTANT BOT:
BOT_USERNAME = Config.BOT_USERNAME


# API VARS:
ANTISPAMBOT_BAN = gvar("ANTISPAMBOT_BAN")

CURRENCY_API = gvar("CURRENCY_API")

DEEPAI_API = gvar("DEEPAI_API")

FBAN_GROUP_ID = (
    int(gvar("FBAN_GROUP_ID")) if gvar("FBAN_GROUP_ID") is not None else BOTLOG_CHATID
)

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

PRIVATE_CHANNEL_ID = int(gvar("PRIVATE_CHANNEL_ID"))

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

WEATHER_API = gvar("WEATHER_API") or "6fded1e1c5ef3f394283e3013a597879"
WEATHER_CITY = gvar("WEATHER_CITY") or "Istanbul"


# PM:
PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD


# HEROKU:
Heroku = from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


# DIRECTORIES:
TEMP_DIR = Config.TEMP_DIR
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY

if not osp.isdir(TMP_DOWNLOAD_DIRECTORY):
    makedirs(TMP_DOWNLOAD_DIRECTORY)

thumb_image_path = osp.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

if Config.THUMB_IMAGE is not None:
    check = validatorsurl(Config.THUMB_IMAGE)
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(get(Config.THUMB_IMAGE).content)
        except Exception as e:
            LOGS.info(str(e))
