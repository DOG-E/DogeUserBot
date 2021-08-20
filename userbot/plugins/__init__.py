from os import path as osp, makedirs

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
from ..languages import lan
from ..languages.constants import *


LOGS = logging.getLogger(__name__)
bot = doge
ALIVE_NAME = Config.ALIVE_NAME
AUTONAME = Config.AUTONAME
BIO_PREFIX = Config.BIO_PREFIX
DEFAULT_BIO = Config.DEFAULT_BIO

# Heroku
Heroku = from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


# Mention user
USERID = doge.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
mention = f"[{Config.ALIVE_NAME}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{Config.ALIVE_NAME}</a>"

PM_START = []
PMMESSAGE_CACHE = {}
PMMENU = "pmpermit_menu" not in Config.NO_LOAD


# Gdrive
G_DRIVE_CLIENT_ID = Config.G_DRIVE_CLIENT_ID
G_DRIVE_CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
G_DRIVE_DATA = Config.G_DRIVE_DATA
G_DRIVE_FOLDER_ID = Config.G_DRIVE_FOLDER_ID
TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY


if not osp.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


# Spamwatch support
if Config.SPAMWATCH_API:
    token = Config.SPAMWATCH_API
    spamwatch = spamwclient(token)
else:
    spamwatch = None


# Thumb image
thumb_image_path = osp.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
if Config.THUMB_IMAGE is not None:
    check = validatorsurl(Config.THUMB_IMAGE)
    if check:
        try:
            with open(thumb_image_path, "wb") as f:
                f.write(get(Config.THUMB_IMAGE).content)
        except Exception as e:
            LOGS.info(str(e))
