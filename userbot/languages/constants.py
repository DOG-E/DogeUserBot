# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from random import choice

from .languages import lan

# BASIS:

MONTHS = {
    "Jan": lan("jan"),
    "Feb": lan("feb"),
    "Mar": lan("mar"),
    "Apr": lan("apr"),
    "May": lan("may"),
    "Jun": lan("jun"),
    "Jul": lan("jul"),
    "Aug": lan("aug"),
    "Sep": lan("sep"),
    "Oct": lan("oct"),
    "Nov": lan("nov"),
    "Dec": lan("dec"),
}


# AFK:
DEF_AFKS = [
    lan("def_afk1"),
    lan("def_afk2"),
    lan("def_afk3"),
    lan("def_afk4"),
    lan("def_afk5"),
    lan("def_afk6"),
    lan("def_afk7"),
    lan("def_afk8"),
    lan("def_afk9"),
    lan("def_afk10"),
    lan("def_afk11"),
    lan("def_afk12"),
    lan("def_afk13"),
]
DOGEAFK = f"{str(choice(DEF_AFKS))}"


# GROUP:
DEF_KICKMES = [
    lan("def_kickme1"),
    lan("def_kickme2"),
    lan("def_kickme3"),
]
DOGEKICKME = f"{str(choice(DEF_KICKMES))}"


# STICKERS:
DEF_KANGS = [
    lan("def_kang1"),
    lan("def_kang2"),
    lan("def_kang3"),
    lan("def_kang4"),
    lan("def_kang5"),
    lan("def_kang6"),
    lan("def_kang7"),
    lan("def_kang8"),
    lan("def_kang9"),
]
DOGEKANG = f"{str(choice(DEF_KANGS))}"
