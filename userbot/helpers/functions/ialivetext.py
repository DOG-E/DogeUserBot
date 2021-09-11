# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from ...Config import Config
from ...languages import lan

tr = Config.CMDSET

def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = lan("notsetdb")
    if not Config.DB_URI:
        return is_database_working, output

    from ...sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"🚨 `{e}`"
        is_database_working = False
    else:
        output = lan("running")
        is_database_working = True
    return is_database_working, output


async def dogealive():
    return lan("ialivetext").format(tr)
