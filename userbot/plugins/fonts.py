# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import random

from userbot import doge

from ..core.managers import edit_or_reply
from . import fonts

plugin_category = "extra"


@doge.ub(
    pattern="fmusical(?:\s|$)([\s\S]*)",
    command=("fmusical", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}fmusical <text>",
            "{tr}fmusical reply this command to text message",
        ],
        "examples": "{tr}fmusical DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            musicalcharacter = fonts.musicalfont[
                fonts.normalfont.index(normalfontcharacter)
            ]
            string = string.replace(normalfontcharacter, musicalcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="ancient(?:\s|$)([\s\S]*)",
    command=("ancient", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}ancient <text>",
            "{tr}ancient reply this command to text message",
        ],
        "examples": "{tr}ancient DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            ancientcharacter = fonts.ancientfont[
                fonts.normalfont.index(normalfontcharacter)
            ]
            string = string.replace(normalfontcharacter, ancientcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="vapor(?:\s|$)([\s\S]*)",
    command=("vapor", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}vapor <text>", "{tr}vapor reply this command to text message"],
        "examples": "{tr}vapor DogeUserBot",
    },
)
async def vapor(event):
    "Changes font style of the given text"
    reply_text = []
    textx = await event.get_reply_message()
    message = event.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(event, "`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await edit_or_reply(event, "".join(reply_text))


@doge.ub(
    pattern="smallcaps(?:\s|$)([\s\S]*)",
    command=("smallcaps", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}smallcaps <text>",
            "{tr}smallcaps reply this command to text message",
        ],
        "examples": "{tr}smallcaps DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smallcapscharacter = fonts.smallcapsfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, smallcapscharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="blackbf(?:\s|$)([\s\S]*)",
    command=("blackbf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}blackbf <text>",
            "{tr}blackbf reply this command to text message",
        ],
        "examples": "{tr}blackbf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblesblackcharacter = fonts.bubblesblackfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, bubblesblackcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="bubbles(?:\s|$)([\s\S]*)",
    command=("bubbles", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}bubbles <text>",
            "{tr}bubbles reply this command to text message",
        ],
        "examples": "{tr}bubbles DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblescharacter = fonts.bubblesfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, bubblescharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="tanf(?:\s|$)([\s\S]*)",
    command=("tanf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}tanf <text>", "{tr}tanf reply this command to text message"],
        "examples": "{tr}tanf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            tantextcharacter = fonts.tantextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, tantextcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="boxf(?:\s|$)([\s\S]*)",
    command=("boxf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}boxf <text>", "{tr}boxf reply this command to text message"],
        "examples": "{tr}boxf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            littleboxtextcharacter = fonts.littleboxtextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, littleboxtextcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="smothtext(?:\s|$)([\s\S]*)",
    command=("smothtext", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}smothtext <text>",
            "{tr}smothtext reply this command to text message",
        ],
        "examples": "{tr}smothtext DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smothtextcharacter = fonts.smothtextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, smothtextcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="egyptf(?:\s|$)([\s\S]*)",
    command=("egyptf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}egyptf <text>", "{tr}egyptf reply this command to text message"],
        "examples": "{tr}egyptf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            egyptfontcharacter = fonts.egyptfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, egyptfontcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="maref(?:\s|$)([\s\S]*)",
    command=("maref", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}maref <text>", "{tr}maref reply this command to text message"],
        "examples": "{tr}maref DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            nightmarecharacter = fonts.nightmarefont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, nightmarecharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="handcf(?:\s|$)([\s\S]*)",
    command=("handcf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}handcf <text>", "{tr}handcf reply this command to text message"],
        "examples": "{tr}handcf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwcapitalcharacter = fonts.hwcapitalfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, hwcapitalcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="doublef(?:\s|$)([\s\S]*)",
    command=("doublef", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}doublef <text>",
            "{tr}doublef reply this command to text message",
        ],
        "examples": "{tr}doublef DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            doubletextcharacter = fonts.doubletextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, doubletextcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="mock(?:\s|$)([\s\S]*)",
    command=("mock", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}mock <text>", "{tr}mock reply this command to text message"],
        "examples": "{tr}mock DogeUserBot",
    },
)
async def spongemocktext(mock):
    "Changes font style of the given text"
    reply_text = []
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(mock, "`gIvE sOMEtHInG tO MoCk!`")
        return

    for charac in message:
        if charac.isalpha() and random.randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await edit_or_reply(mock, "".join(reply_text))


@doge.ub(
    pattern="ghostf(?:\s|$)([\s\S]*)",
    command=("ghostf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}ghostf <text>", "{tr}ghostf reply this command to text message"],
        "examples": "{tr}ghostf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            ghostfontcharacter = fonts.ghostfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, ghostfontcharacter)
    await edit_or_reply(event, string)


@doge.ub(
    pattern="handsf(?:\s|$)([\s\S]*)",
    command=("handsf", plugin_category),
    info={
        "header": "Font style command.(Changes font style of the given text)",
        "usage": ["{tr}handsf <text>", "{tr}handsf reply this command to text message"],
        "examples": "{tr}handsf DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwslcharacter = fonts.hwslfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, hwslcharacter)
    await edit_or_reply(event, string)
