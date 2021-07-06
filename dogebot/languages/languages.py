# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Forked, developed and edited for @DogeUserbot
#
from os import listdir, path
from typing import Any, Dict, List, Union

from yaml import safe_load

from ..sql_helper.globals import gvarstatus

langs = {}
langs_folder = path.join(path.dirname(path.realpath(__file__)), "languages")


for file in listdir(langs_folder):
    if file.endswith(".yml"):
        code = file[:-4]
        langs[code] = safe_load(
            open(path.join(langs_folder, file), encoding="UTF-8"),
        )


def lang(key: str) -> Any:
    try:
        return langs[(gvarstatus("DOGELANG") or "en")][key]
    except KeyError:
        try:
            return langs["en"][key]
        except KeyError:
            return f"Warning: could not load any string with the key {key}"


def getlangs() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": langs[code]["name"],
            "natively": langs[code]["natively"],
            "authors": langs[code]["authors"],
        }
        for code in langs
    }
