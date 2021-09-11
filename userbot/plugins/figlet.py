# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from random import choice

from pyfiglet import figlet_format

from . import _format, deEmojify, doge, edl, eor, tr

plugin_category = "fun"

CMD_FIG = {
    "1": "slant",
    "2": "3-d",
    "3": "5lineoblique",
    "4": "alphabet",
    "5": "banner3-D",
    "6": "doh",
    "7": "basic",
    "8": "binary",
    "9": "isometric1",
    "10": "letters",
    "11": "alligator",
    "12": "dotmatrix",
    "13": "bubble",
    "14": "bulbhead",
    "15": "digital",
}
CMDFIG = [
    "slant",
    "3-d",
    "5lineoblique",
    "alphabet",
    "banner3-D",
    "doh",
    "basic",
    "binary",
    "isometric1",
    "letters",
    "alligator",
    "dotmatrix",
    "bubble",
    "bulbhead",
    "digital",
]


@doge.bot_cmd(
    pattern="fg(?:\s|$)([\s\S]*)",
    command=("fg", plugin_category),
    info={
        "header": "Changes the given text into the given style",
        "usage": ["{tr}fg <style>.<text>", "{tr}fg <text>"],
        "examples": ["{tr}fg digi.hello", "{tr}fg hello"],
        "styles": CMD_FIG,
    },
)
async def figlet(event):
    "Changes the given text into the given style"
    input_str = event.pattern_match.group(1)
    if "." in input_str:
        cmd, text = input_str.split(".", maxsplit=1)
    elif input_str:
        cmd = None
        text = input_str
    else:
        return await eor(event, "`Give some text to change it`")

    style = cmd
    text = text.strip()
    if style:
        try:
            font = CMD_FIG[style.strip()]
        except KeyError:
            return await edl(
                event, f"**Invalid style selected!** __Check__ `{tr}doge figlet`."
            )

        result = figlet_format(deEmojify(text), font=font)
    else:
        font = choice(CMDFIG)
        result = figlet_format(deEmojify(text), font=font)
    await eor(event, f"ㅤ \n{result}", parse_mode=_format.parse_pre)
