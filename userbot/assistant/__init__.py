# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from .. import *
from ..Config import Config
from ..core.decorators import check_owner
from ..core.inlinebot import *
from ..core.logger import logging
from ..core.managers import edl, eor
from ..core.session import doge
from ..helpers import *
from ..helpers.utils import _dogetools, _dogeutils, _format, install_pip, reply_id
from ..plugins import mention
from ..sql_helper.globals import dgvar, gvar, sgvar

# OWNER:
OWNER_ID = Config.OWNER_ID


# ASSISTANT BOT:
BOT_USERNAME = Config.BOT_USERNAME


# DIRECTORIES:
TEMP_DIR = Config.TEMP_DIR
