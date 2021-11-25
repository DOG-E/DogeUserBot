# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from io import BytesIO
from os import mkdir, path, remove, system
from random import choice, randint
from textwrap import wrap
from urllib.request import urlretrieve

from numpy import array, dstack
from PIL.Image import fromarray, new
from PIL.Image import open as Imopen
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

from . import (
    _dogetools,
    clippy,
    convert_tosticker,
    deEmojify,
    doge,
    edl,
    eor,
    hide_inlinebot,
    hide_inlinebot_point,
    higlighted_text,
    media_type,
    reply_id,
    waifutxt,
)

plugin_category = "fun"


@doge.bot_cmd(
    pattern="(|b)qbs(?:\s|$)([\s\S]*)",
    command=("qbs", plugin_category),
    info={
        "header": "Make quby say anything.",
        "flags": {
            "b": "Give the sticker on background.",
        },
        "usage": [
            "{tr}qbs <text/reply to msg>",
            "{tr}bqbs <text/reply to msg>",
        ],
        "examples": [
            "{tr}qbs Gib money",
            "{tr}bqbs Gib money",
        ],
    },
)
async def quby(event):
    "Make a cool quby text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edl(event, "__What is quby supposed to say? Give some text.__")
    await edl(event, "**⏳ Processing...**")
    if not path.isdir("./temp"):
        mkdir("./temp")
    temp_name = "./temp/quby_temp.png"
    file_name = "./temp/quby.png"
    templait = urlretrieve(
        "https://telegra.ph/file/09f4df5a129758a2e1c9c.jpg", temp_name
    )
    if len(text) < 40:
        font = 80
        wrap = 1.4
        position = (100, 0)
    else:
        font = 60
        wrap = 1.2
        position = (0, 0)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="+4",
        position=position,
    )
    if cmd == "b":
        dog = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, dog, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and path.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="(|b)bls(?:\s|$)([\s\S]*)",
    command=("bls", plugin_category),
    info={
        "header": "Give the sticker on background.",
        "flags": {
            "b": "To create knife sticker transparent.",
        },
        "usage": [
            "{tr}bls <text/reply to msg>",
            "{tr}bbls <text/reply to msg>",
        ],
        "examples": [
            "{tr}bls Gib money",
            "{tr}bbls Gib money",
        ],
    },
)
async def knife(event):
    "Make a blob knife text sticker"
    cmd = event.pattern_match.group(1).lower
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edl(event, "__What is knife supposed to say? Give some text.__")
    await edl(event, "**⏳ Processing...**")
    if not path.isdir("./temp"):
        mkdir("./temp")
    temp_name = "./temp/knife_temp.png"
    file_name = "./temp/knife.png"
    templait = urlretrieve(
        "https://telegra.ph/file/2188367c8c5f43c36aa59.jpg", temp_name
    )
    if len(text) < 50:
        font = 90
        wrap = 2
        position = (250, -450)
    else:
        font = 60
        wrap = 1.4
        position = (150, 500)
    text = deEmojify(text)
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace="-5",
        position=position,
        direction="upwards",
    )
    if cmd == "b":
        dog = convert_tosticker(file_name)
        await event.client.send_file(
            event.chat_id, dog, reply_to=reply_to_id, force_document=False
        )
    else:
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await event.delete()
    for files in (temp_name, file_name):
        if files and path.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="(|b)dgs(?:\s|$)([\s\S]*)",
    command=("dgs", plugin_category),
    info={
        "header": "Make doge say anything.",
        "flags": {
            "b": "To create doge sticker with highligted text.",
        },
        "usage": [
            "{tr}dgs <text/reply to msg>",
            "{tr}bdgs <text/reply to msg>",
        ],
        "examples": [
            "{tr}dgs Gib money",
            "{tr}bdsgs Gib money",
        ],
    },
)
async def dogesticker(event):
    "Make a cool doge text sticker"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if not text and event.is_reply:
        text = (await event.get_reply_message()).message
    if not text:
        return await edl(event, "__What is doge supposed to say? Give some text.__")
    await edl(event, "**⏳ Processing...**")
    if not path.isdir("./temp"):
        mkdir("./temp")
    temp_name = "./temp/doge_temp.jpg"
    file_name = "./temp/doge.jpg"
    templait = urlretrieve(
        "https://telegra.ph/file/6f621b9782d9c925bd6c4.jpg", temp_name
    )
    text = deEmojify(text)
    font, wrap = (90, 2) if len(text) < 90 else (70, 2.5)
    bg, fg, alpha, ls = (
        ("black", "white", 255, "5") if cmd == "b" else ("white", "black", 0, "-40")
    )
    higlighted_text(
        temp_name,
        text,
        file_name,
        text_wrap=wrap,
        font_size=font,
        linespace=ls,
        position=(0, 10),
        align="left",
        background=bg,
        foreground=fg,
        transparency=alpha,
    )
    dog = convert_tosticker(file_name)
    await event.client.send_file(
        event.chat_id, dog, reply_to=reply_to_id, force_document=False
    )
    await event.delete()
    for files in (temp_name, file_name):
        if files and path.exists(files):
            remove(files)


# Random RGB Sticklet by @PhycoNinja13b
@doge.bot_cmd(
    pattern="stcr ?([\s\S]*)",
    command=("stcr", plugin_category),
    info={
        "header": "your text as sticker.",
        "usage": [
            "{tr}stcr <text>",
        ],
        "examples": "{tr}stcr hello",
    },
)
async def sticklet(event):
    "your text as sticker"
    R = randint(0, 256)
    G = randint(0, 256)
    B = randint(0, 256)
    FONTS = [
        "userbot/helpers/resources/fonts/droidsans_mono.ttf",
        "userbot/helpers/resources/fonts/impact.ttf",
        "userbot/helpers/resources/fonts/modern.ttf",
        "userbot/helpers/resources/fonts/productsans_light.ttf",
        "userbot/helpers/resources/fonts/roboto_medium.ttf",
        "userbot/helpers/resources/fonts/roboto_italic.ttf",
    ]
    reply_to_id = await reply_id(event)
    sticktext = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not sticktext:
        if event.reply_to_msg_id:
            sticktext = reply_message.message
        else:
            return await eor(event, "need something, hmm")
    await event.delete()
    sticktext = deEmojify(sticktext)
    sticktext = wrap(sticktext, width=10)
    sticktext = "\n".join(sticktext)
    image = new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = Draw(image)
    fontsize = 230
    FONT_FILE = choice(FONTS)
    font = truetype(FONT_FILE, size=int(fontsize))
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = truetype(FONT_FILE, size=int(fontsize))
    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )
    image_stream = BytesIO()
    image_stream.name = "DogeUserBot.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    await event.client.send_file(
        event.chat_id,
        image_stream,
        reply_to=reply_to_id,
    )
    try:
        remove(FONT_FILE)
    except BaseException:
        pass


@doge.bot_cmd(
    pattern="waifu(?:\s|$)([\s\S]*)",
    command=("waifu", plugin_category),
    info={
        "header": "Anime that makes your writing fun.",
        "usage": "{tr}waifu <text>",
        "examples": "{tr}waifu hello",
    },
)
async def waifu(animu):
    "Anime that makes your writing fun"
    text = animu.pattern_match.group(1)
    reply_to_id = await reply_id(animu)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            return await eor(
                animu, "`You haven't written any article, Waifu is going away.`"
            )
    text = deEmojify(text)
    await animu.delete()
    await waifutxt(text, animu.chat_id, reply_to_id, animu.client)


@doge.bot_cmd(
    pattern="honk(?:\s|$)([\s\S]*)",
    command=("honk", plugin_category),
    info={
        "header": "Make honk say anything.",
        "usage": "{tr}honk <text/reply to msg>",
        "examples": "{tr}honk How you doing?",
    },
)
async def honk(event):
    "Make honk say anything."
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@honka_says_bot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edl(event, "__What is honk supposed to say? Give some text.__")
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot_point(event.client, bot_name, text, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="twt(?:\s|$)([\s\S]*)",
    command=("twt", plugin_category),
    info={
        "header": "Make a cool tweet of your account",
        "usage": "{tr}twt <text/reply to msg>",
        "examples": "{tr}twt DogeUserBot",
    },
)
async def twt(event):
    "Make a cool tweet of your account."
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@TwitterStatusBot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edl(event, "__What am I supposed to Tweet? Give some text.__")
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="glax(|r)(?:\s|$)([\s\S]*)",
    command=("glax", plugin_category),
    info={
        "header": "Make glax the dragon scream your text.",
        "flags": {
            "r": "Reverse the face of the dragon",
        },
        "usage": [
            "{tr}glax <text/reply to msg>",
            "{tr}glaxr <text/reply to msg>",
        ],
        "examples": [
            "{tr}glax Die you",
            "{tr}glaxr Die you",
        ],
    },
)
async def glax(event):
    "Make glax the dragon scream your text."
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    bot_name = "@GlaxScremBot"
    c_lick = 1 if cmd == "r" else 0
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edl(event, "What is glax supposed to scream? Give text..")
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(
        event.client, bot_name, text, event.chat_id, reply_to_id, c_lick=c_lick
    )


@doge.bot_cmd(
    pattern="gogle(?:\s|$)([\s\S]*)",
    command=("gogle", plugin_category),
    info={
        "header": "Search in google animation",
        "usage": "{tr}gogle <text/reply to msg>",
        "examples": "{tr}gogle DogeUserBot",
    },
)
async def gogle(event):
    "Search in google animation."
    text = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    bot_name = "@GooglaxBot"
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            return await edl(event, "__What am I supposed to search? Give some text.__")
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


# Credits: TeamUltroid
@doge.bot_cmd(
    pattern="sround(?:\s|$)([\s\S]*)",
    command=("sround", plugin_category),
    info={
        "header": "To convert media round square sticker.",
        "usage": "{tr}sround <reply to a sticker>",
    },
)
async def stickround(event):
    "To convert media round square sticker."
    reply = await event.get_reply_message()

    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo"]:
        return await edl(event, "__Reply to photo to make it square image.__")
    dogevent = await event.edit("__Adding borders to make it square....__")
    try:
        imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
        if imag[1] is None:
            return await edl(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        img = Imopen(imag[1]).convert("RGB")
    except Exception as e:
        return await edl(dogevent, f"**Error in identifying image:**\n__{e}__")

    npImage = array(img)
    h, w = img.size
    alpha = new("L", img.size, 0)
    draw = Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = array(alpha)
    npImage = dstack((npImage, npAlpha))
    fromarray(npImage).save("dogeuserbot.webp")
    await event.client.send_file(
        event.chat_id,
        "dogeuserbot.webp",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await dogevent.delete()
    remove(img)
    remove("dogeuserbot.webp")


# Credits: TeamUltroid
@doge.bot_cmd(
    pattern="destroy$",
    command=("destroy", plugin_category),
    info={
        "header": "Destory a animated sticker.",
        "usage": "{tr}destroy <reply to a animated sticker>",
    },
)
async def destroyasticker(event):
    "Destory a animated sticker"
    dog = await event.get_reply_message()
    if not event.is_reply:
        return await edl(event, "`Reply to animated sticker only.`")
    if not (
        dog.media and dog.media.document and "tgsticker" in dog.media.document.mime_type
    ):
        return await edl(event, "`Reply to animated sticker only.`")
    await event.client.download_media(dog, "dogeuserbot.tgs")
    dogevent = await eor(event, "`Processing...`")
    system("lottie_convert.py dogeuserbot.tgs json.json")
    with open("json.json") as json:
        jsn = json.read()
    jsn = (
        jsn.replace("[100]", "[200]")
        .replace("[10]", "[40]")
        .replace("[-1]", "[-10]")
        .replace("[0]", "[15]")
        .replace("[1]", "[20]")
        .replace("[2]", "[17]")
        .replace("[3]", "[40]")
        .replace("[4]", "[37]")
        .replace("[5]", "[60]")
        .replace("[6]", "[70]")
        .replace("[7]", "[40]")
        .replace("[8]", "[37]")
        .replace("[9]", "[110]")
    )
    open("json.json", "w").write(jsn)
    system("lottie_convert.py json.json dogeuserbot.tgs")
    await event.client.send_file(
        event.chat_id,
        file="dogeuserbot.tgs",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await dogevent.delete()
    remove("json.json")
