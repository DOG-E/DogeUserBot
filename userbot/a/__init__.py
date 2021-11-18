# @DogeUserBot - < https://t.me/DogeUserBot >

from .. import *
from ..helpers import *

USERID = doge.uid if Config.OWNER_ID == 0 else Config.OWNER_ID
mention = f"[{gvar('ALIVE_NAME')}](tg://user?id={USERID})"
hmention = f"<a href = tg://user?id={USERID}>{gvar('ALIVE_NAME')}</a>"

# ASSISTANT BOT:
BOT_USERNAME = Config.BOT_USERNAME

TMP_DOWNLOAD_DIRECTORY = Config.TMP_DOWNLOAD_DIRECTORY
