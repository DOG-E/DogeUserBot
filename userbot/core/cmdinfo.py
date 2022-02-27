# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from typing import Dict, List, Union

from ..helpers.utils.extdl import install_pip

try:
    from urlextract import URLExtract
except ModuleNotFoundError:
    install_pip("urlextract")
    from urlextract import URLExtract

from ..Config import Config

extractor = URLExtract()


def get_data(about, ktype):
    data = about[ktype]
    urls = extractor.find_urls(data)
    if len(urls) > 0:
        return data
    return data.capitalize()


def _format_about(
    about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
) -> str:  # sourcery no-metrics
    if not isinstance(about, dict):
        return about

    tmp_chelp = ""
    if "h" in about and isinstance(about["h"], str):
        tmp_chelp += f"__{about['h'].title()}__"
        del about["h"]

    if "d" in about and isinstance(about["d"], str):
        tmp_chelp += f"\n\n**🐾 Açıᴋʟᴀᴍᴀ:**\n" f"__{get_data(about, 'd')}__"
        del about["d"]

    if "f" in about:
        tmp_chelp += "\\n\\n**🐾 Aʏᴀʀ:**"
        if isinstance(about["f"], dict):
            for f_n, f_d in about["f"].items():
                tmp_chelp += f"\n    ▫️ `{f_n}`: __{f_d.lower()}__"
        else:
            tmp_chelp += f"\n    {about['f']}"
        del about["f"]

    if "o" in about:
        tmp_chelp += "\\n\\n**🐾 Sᴇçᴇɴᴇᴋʟᴇʀ:**"
        if isinstance(about["o"], dict):
            for o_n, o_d in about["o"].items():
                tmp_chelp += f"\n    ▫️ `{o_n}`: __{o_d.lower()}__"
        else:
            tmp_chelp += f"\n    __{about['o']}__"
        del about["o"]

    if "t" in about:
        tmp_chelp += "\\n\\n**🐾 Dᴇsᴛᴇᴋʟᴇɴᴇɴ Tüʀʟᴇʀ:**"
        if isinstance(about["t"], list):
            for _opt in about["t"]:
                tmp_chelp += f"\n    `{_opt}` ,"
        else:
            tmp_chelp += f"\n    __{about['t']}__"
        del about["t"]

    if "u" in about:
        tmp_chelp += "\\n\\n**🐾 Kᴜʟʟᴀɴıᴍ:**"
        if isinstance(about["u"], list):
            for ex_ in about["u"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['u']}`"
        del about["u"]

    if "e" in about:
        tmp_chelp += "\\n\\n**🐾 Öʀɴᴇᴋ:**"
        if isinstance(about["e"], list):
            for ex_ in about["e"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['e']}`"
        del about["e"]

    if "ot" in about:
        tmp_chelp += f"\n\n**🐾 Dɪɢ̆ᴇʀ:**\n__{get_data(about, 'ot')}__"
        del about["ot"]

    if about:
        for t_n, t_d in about.items():
            tmp_chelp += f"\n\n**🐾 {t_n.title()}:**\n"
            if isinstance(t_d, dict):
                for o_n, o_d in t_d.items():
                    tmp_chelp += f"    ▫️ `{o_n}`: __{get_data(t_d, o_n)}__\n"
            elif isinstance(t_d, list):
                for _opt in t_d:
                    tmp_chelp += f"    `{_opt}`,"
                tmp_chelp += "\n"
            else:
                tmp_chelp += f"__{get_data(about ,t_n)}__"
                tmp_chelp += "\n"

    return tmp_chelp.replace("{tr}", Config.CMDSET)
