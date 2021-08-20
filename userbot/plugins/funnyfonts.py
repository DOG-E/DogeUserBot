from random import choice, getrandbits, randint
from re import sub

from . import doge, eor, fonts

plugin_category = "fun"


@doge.bot_cmd(
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
        return await eor(mock, "`gIvE sOMEtHInG tO MoCk!`")

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)
    await eor(mock, "".join(reply_text))


@doge.bot_cmd(
    pattern="str(?:\s|$)([\s\S]*)",
    command=("str", plugin_category),
    info={
        "header": "stretches the given text",
        "usage": ["{tr}str <text>", "{tr}str reply this command to text message"],
        "examples": "{tr}str DogeUserBot",
    },
)
async def stretch(stret):
    "stretches the given text"
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(stret, "`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")

    count = randint(3, 10)
    reply_text = sub(
        r"([aeıioöuüAEIİOÖUÜａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count), message
    )
    await eor(stret, reply_text)


@doge.bot_cmd(
    pattern="zal(?:\s|$)([\s\S]*)",
    command=("zal", plugin_category),
    info={
        "header": "chages given text into some funny way",
        "usage": ["{tr}zal <text>", "{tr}zal reply this command to text message"],
        "examples": "{tr}zal DogeUserBot",
    },
)
async def zal(zgfy):
    "chages given text into some funny way"
    reply_text = []
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(
            zgfy, "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
        )

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue
        for _ in range(3):
            rand = randint(0, 2)
            if rand == 0:
                charac = charac.strip() + choice(fonts.ZALG_LIST[0]).strip()
            elif rand == 1:
                charac = charac.strip() + choice(fonts.ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + choice(fonts.ZALG_LIST[2]).strip()
        reply_text.append(charac)
    await eor(zgfy, "".join(reply_text))


@doge.bot_cmd(
    pattern="cp(?:\s|$)([\s\S]*)",
    command=("cp", plugin_category),
    info={
        "header": "chages given text into some funny way",
        "usage": ["{tr}cp <text>", "{tr}cp reply this command to text message"],
        "examples": "{tr}cp DogeUserBot",
    },
)
async def copypasta(cp_e):
    "chages given text into some funny way"
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(cp_e, "`😂🤡IvE👐sOmE👅tExT👅fOr✌️Me👌tO👐MAkE👀iT💞fUnNy!💦`")

    reply_text = choice(fonts.EMOJIS)
    # choose a random character in the message to be substituted with 🤡
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(fonts.EMOJIS)
        elif owo in fonts.EMOJIS:
            reply_text += owo
            reply_text += choice(fonts.EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🤡"
        else:
            reply_text += owo.upper() if bool(getrandbits(1)) else owo.lower()
    reply_text += choice(fonts.EMOJIS)
    await eor(cp_e, reply_text)


@doge.bot_cmd(
    pattern="downside(?:\s|$)([\s\S]*)",
    command=("downside", plugin_category),
    info={
        "header": "chages given text into upside down",
        "usage": [
            "{tr}downside <text>",
            "{tr}downside reply this command to text message",
        ],
        "examples": "{tr}downside DogeUserBot",
    },
)
async def stylish_generator(event):
    "chages given text into upside down"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        return await eor(event, "What I am Supposed to change give text")

    string = "  ".join(args).lower()
    for upsidecharacter in string:
        if upsidecharacter in fonts.upsidefont:
            downsidecharacter = fonts.downsidefont[
                fonts.upsidefont.index(upsidecharacter)
            ]
            string = string.replace(upsidecharacter, downsidecharacter)
    await eor(event, string)


@doge.bot_cmd(
    pattern="subscript(?:\s|$)([\s\S]*)",
    command=("subscript", plugin_category),
    info={
        "header": "chages given text into subscript",
        "usage": [
            "{tr}subscript <text>",
            "{tr}subscript reply this command to text message",
        ],
        "examples": "{tr}subscript DogeUserBot",
    },
)
async def stylish_generator(event):
    "chages given text into subscript"
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        return await eor(event, "What I am Supposed to change give text")

    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            subscriptcharacter = fonts.subscriptfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, subscriptcharacter)
    await eor(event, string)
