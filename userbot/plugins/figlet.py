import pyfiglet

from ..helpers.utils import _format
from . import _format, deEmojify, doge, edl, eor

plugin_category = "extra"

CMD_FIG = {
    "slant": "slant",
    "3D": "3-d",
    "5line": "5lineoblique",
    "alpha": "alphabet",
    "banner": "banner3-D",
    "doh": "doh",
    "basic": "basic",
    "binary": "binary",
    "iso": "isometric1",
    "letter": "letters",
    "allig": "alligator",
    "dotm": "dotmatrix",
    "bubble": "bubble",
    "bulb": "bulbhead",
    "digi": "digital",
}


@doge.bot_cmd(
    pattern="figlet(?:\s|$)([\s\S]*)",
    command=("figlet", plugin_category),
    info={
        "header": "Changes the given text into the given style",
        "usage": ["{tr}figlet <style> ; <text>", "{tr}figlet <text>"],
        "examples": ["{tr}figlet digi ; hello", "{tr}figlet hello"],
        "styles": [
            "slant",
            "3D",
            "5line",
            "alpha",
            "banner",
            "doh",
            "iso",
            "letter",
            "allig",
            "dotm",
            "bubble",
            "bulb",
            "digi",
            "binary",
            "basic",
        ],
    },
)
async def figlet(event):
    "Changes the given text into the given style"
    input_str = event.pattern_match.group(1)
    if ";" in input_str:
        cmd, text = input_str.split(";", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await eor(event, "`Give some text to change it`")
        return
    style = cmd
    text = text.strip()
    if style is not None:
        try:
            font = CMD_FIG[style.strip()]
        except KeyError:
            return await edl(
                event, "**Invalid style selected**, __Check__ `.info figlet`."
            )
        result = pyfiglet.figlet_format(deEmojify(text), font=font)
    else:
        result = pyfiglet.figlet_format(deEmojify(text))
    await eor(event, result, parse_mode=_format.parse_pre)
