from . import doge, edl, eor, fonts

plugin_category = "misc"


@doge.bot_cmd(
    pattern="[Ff]1(?:\s|$)([\s\S]*)",
    command=("f1", plugin_category),
    info={
        "header": "៣ ⩏ ន ɨ ¢ ♬ ɭ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f1 <text>",
            "{tr}f1 reply this command to text message",
        ],
        "examples": "{tr}f1 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            musicalcharacter = fonts.musicalfont[
                fonts.normalfont.index(normalfontcharacter)
            ]
            string = string.replace(normalfontcharacter, musicalcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]2(?:\s|$)([\s\S]*)",
    command=("f2", plugin_category),
    info={
        "header": "ꍏ ꈤ ꉓ ꀤ ꍟ ꈤ ꓄ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f2 <text>",
            "{tr}f2 reply this command to text message",
        ],
        "examples": "{tr}f2 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normalfontcharacter in string:
        if normalfontcharacter in fonts.normalfont:
            ancientcharacter = fonts.ancientfont[
                fonts.normalfont.index(normalfontcharacter)
            ]
            string = string.replace(normalfontcharacter, ancientcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]3(?:\s|$)([\s\S]*)",
    command=("f3", plugin_category),
    info={
        "header": "ｖａｐｏｒ Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f3 <text>", "{tr}f3 reply this command to text message"],
        "examples": "{tr}f3 DogeUserBot",
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
        await edl(event, "`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await eor(event, "".join(reply_text))


@doge.bot_cmd(
    pattern="[Ff]4(?:\s|$)([\s\S]*)",
    command=("f4", plugin_category),
    info={
        "header": "sᴍᴀʟʟᴄᴀᴘs Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f4 <text>",
            "{tr}f4 reply this command to text message",
        ],
        "examples": "{tr}f4 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = "".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smallcapscharacter = fonts.smallcapsfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, smallcapscharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]5(?:\s|$)([\s\S]*)",
    command=("f5", plugin_category),
    info={
        "header": "🅑 🅛 🅐 🅒 🅚 🅑 🅕 Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f5 <text>",
            "{tr}f5 reply this command to text message",
        ],
        "examples": "{tr}f5 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblesblackcharacter = fonts.bubblesblackfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, bubblesblackcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]6(?:\s|$)([\s\S]*)",
    command=("f6", plugin_category),
    info={
        "header": "Ⓑ Ⓤ Ⓑ Ⓑ Ⓛ Ⓔ Ⓢ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f6 <text>",
            "{tr}f6 reply this command to text message",
        ],
        "examples": "{tr}f6 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            bubblescharacter = fonts.bubblesfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, bubblescharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]7(?:\s|$)([\s\S]*)",
    command=("f7", plugin_category),
    info={
        "header": "Ꮏ Ꭿ Ꮑ Ꮄ Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f7 <text>", "{tr}f7 reply this command to text message"],
        "examples": "{tr}f7 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            tantextcharacter = fonts.tantextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, tantextcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]8(?:\s|$)([\s\S]*)",
    command=("f8", plugin_category),
    info={
        "header": "🄱 🄾 🅇 🄵 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f8 <text>", "{tr}f8 reply this command to text message"],
        "examples": "{tr}f8 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            littleboxtextcharacter = fonts.littleboxtextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, littleboxtextcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]9(?:\s|$)([\s\S]*)",
    command=("f9", plugin_category),
    info={
        "header": "ᔑ ᗰ ᝪ ᝪ Ꭲ ᕼ Ꭲ ᗴ ᙭ Ꭲ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f9 <text>",
            "{tr}f9 reply this command to text message",
        ],
        "examples": "{tr}f9 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            smothtextcharacter = fonts.smothtextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, smothtextcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]10(?:\s|$)([\s\S]*)",
    command=("f10", plugin_category),
    info={
        "header": "є ﻮ א ק t Ŧ Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f10 <text>", "{tr}f10 reply this command to text message"],
        "examples": "{tr}f10 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            egyptfontcharacter = fonts.egyptfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, egyptfontcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]11(?:\s|$)([\s\S]*)",
    command=("f11", plugin_category),
    info={
        "header": "𝖒𝖆𝖗𝖊𝖋 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f11 <text>", "{tr}f11 reply this command to text message"],
        "examples": "{tr}f11 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = "".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            nightmarecharacter = fonts.nightmarefont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, nightmarecharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]12(?:\s|$)([\s\S]*)",
    command=("f12", plugin_category),
    info={
        "header": "𝓗 𝓐 𝓝 𝓓 𝓒 𝓕 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f12 <text>", "{tr}f12 reply this command to text message"],
        "examples": "{tr}f12 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwcapitalcharacter = fonts.hwcapitalfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, hwcapitalcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]13(?:\s|$)([\s\S]*)",
    command=("f13", plugin_category),
    info={
        "header": "ⅅ Ꮎ U ℬ ℒ ℰ ℱ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f13 <text>",
            "{tr}f13 reply this command to text message",
        ],
        "examples": "{tr}f13 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            doubletextcharacter = fonts.doubletextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, doubletextcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]14(?:\s|$)([\s\S]*)",
    command=("f14", plugin_category),
    info={
        "header": "𝕲 𝕳 𝕺 𝕾 𝕿 𝕱 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f14 <text>", "{tr}f14 reply this command to text message"],
        "examples": "{tr}f14 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            ghostfontcharacter = fonts.ghostfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, ghostfontcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]15(?:\s|$)([\s\S]*)",
    command=("f15", plugin_category),
    info={
        "header": "𝒽 𝒶 𝓃 𝒹 𝓈 𝒻 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f15 <text>", "{tr}f15 reply this command to text message"],
        "examples": "{tr}f15 DogeUserBot",
    },
)
async def stylish_generator(event):
    "Changes font style of the given text"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwslcharacter = fonts.hwslfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, hwslcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]16(?:\s|$)([\s\S]*)",
    command=("f16", plugin_category),
    info={
        "header": "ˢ ᵘ ᵖ ᵉ ʳ ˢ ᶜ ʳ ᶦ ᵖ ᵗ Font style command.(Changes font style of the given text)",
        "usage": [
            "{tr}f16 <text>",
            "{tr}f16 reply this command to text message",
        ],
        "examples": "{tr}f16 DogeUserBot",
    },
)
async def stylish_generator(event):
    "chages given text into superscript"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "What I am Supposed to change give text")
        return
    string = " ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            superscriptcharacter = fonts.superscriptfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, superscriptcharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="[Ff]17(?:\s|$)([\s\S]*)",
    command=("f17", plugin_category),
    info={
        "header": "山 乇 乇 乃 Font style command.(Changes font style of the given text)",
        "usage": ["{tr}f17 <text>", "{tr}f17 reply this command to text message"],
        "examples": "{tr}f17 DogeUserBot",
    },
)
async def weebify(event):
    "chages given text into some funny way"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edl(event, "`What I am Supposed to Weebify `")
        return
    string = " ".join(args).lower()
    for normiecharacter in string:
        if normiecharacter in fonts.normiefont:
            weebycharacter = fonts.weebyfont[fonts.normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)
    await eor(event, string)
