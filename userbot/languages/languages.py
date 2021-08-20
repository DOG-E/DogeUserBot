# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
from os import listdir, path
from typing import Any, Dict, List, Union

from googletrans import Translator
from yaml import safe_load

from .. import gvarstatus

languages = {}
Trs = Translator()
languages_folder = path.join(path.dirname(path.realpath(__file__)), "languages")


for file in listdir(languages_folder):
    if file.endswith(".yml"):
        code = file[:-4]
        languages[code] = safe_load(
            open(path.join(languages_folder, file), encoding="UTF-8"),
        )


def lan(key: str) -> Any:
    try:
        return languages[(gvarstatus("DOGELANG") or "en")][key]
    except KeyError:
        try:
            return Trs.translate(languages["en"][key], dest=gvarstatus("DOGELANG")).text
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
