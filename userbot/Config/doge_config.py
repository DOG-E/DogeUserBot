# Config values will be loaded from here
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import os

ENV = bool(os.environ.get("ENV", False))

if ENV:
    from sample_config import Config  # noqa
elif os.path.exists("config.py"):
    from config import Development as Config  # noqa
