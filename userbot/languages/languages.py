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

from google_trans_new import google_translator
from yaml import safe_load

from ..sql_helper.globals import gvar

language = [gvar("DOGELANG") or "en"]
listlangs = {}

Trs = google_translator()

languages_folder = path.join(path.dirname(path.realpath(__file__)), "languages")

for file in listdir(languages_folder):
    if file.endswith(".yml"):
        code = file[:-4]
        listlangs[code] = safe_load(
            open(path.join(languages_folder, file), encoding="UTF-8"),
        )


def lan(key: str) -> Any:
    lang = language[0]
    try:
        return listlangs[lang][key]
    except KeyError:
        try:
            trt = Trs.translate(listlangs["en"][key], lang_tgt=lang)
            if listlangs.get(lang):
                listlangs[lang][key] = trt
            else:
                listlangs.update({lang: {key: trt}})
            return trt
        except KeyError:
            return f"🚧 WARNING: Couldn't load any language with the key `{key}`"


def lngs() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": listlangs[code]["name"],
            "natively": listlangs[code]["natively"],
            "authors": listlangs[code]["authors"],
        }
        for code in listlangs
    }
