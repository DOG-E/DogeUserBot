# Credits: TeamUltroid - github.com/teamultroid
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import listdir, path
from typing import Any, Dict, List, Union

from googletrans import Translator
from yaml import safe_load

from ..sql_helper.globals import gvar

languages = {}
languages_folder = path.join(path.dirname(path.realpath(__file__)), "languages")
Translate = Translator()


for file in listdir(languages_folder):
    if file.endswith(".yml"):
        code = file[:-4]
        languages[code] = safe_load(
            open(path.join(languages_folder, file), encoding="UTF-8"),
        )


def lan(key: str) -> Any:
    try:
        return languages[(gvar("DOGELANG") or "en")][key]

    except KeyError:
        try:
            return Translate.translate(languages["en"][key], dest=gvar("DOGELANG")).text

        except KeyError:
            return f"🚧 WARNING: Couldn't load any language with the key {key}"


def lngs() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }
