from random import choice

from pyfiglet import figlet_format

from . import _format, deEmojify, doge, edl, eor, tr

plugin_category = "fun"

CMD_FIG = {
    "slant": "slant",
    "3d": "3-d",
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
    pattern="fg(?:\s|$)([\s\S]*)",
    command=("fg", plugin_category),
    info={
        "header": "Changes the given text into the given style",
        "usage": ["{tr}fg <style> ; <text>", "{tr}fg <text>"],
        "examples": ["{tr}fg digi ; hello", "{tr}fg hello"],
        "styles": [
            "slant",
            "3d",
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
    elif input_str:
        cmd = None
        text = input_str
    else:
        await eor(event, "`Give some text to change it`")
        return
    style = cmd
    text = text.strip()
    if style is not None:
        try:
            font = choice(CMD_FIG[style.strip()])
        except KeyError:
            return await edl(
                event, f"**Invalid style selected**, __Check__ `{tr}doge figlet`."
            )
        result = figlet_format(deEmojify(text), font=font)
    else:
        result = figlet_format(deEmojify(text))
    await eor(event, f"ㅤ \n{result}", parse_mode=_format.parse_pre)
