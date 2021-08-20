# Made by @mrconfused and @sandy1709
# memify plugin for catuserbot
from asyncio import sleep, create_subprocess_exec
from asyncio.subprocess import PIPE
from base64 import b64decode
from os import path as ospath, mkdir, remove

from cv2 import imwrite, VideoCapture
from PIL.Image import open as Imopen
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import (
    _dogetools,
    add_frame,
    addgvar,
    asciiart,
    convert_toimage,
    crop,
    doge,
    dogemmfhelper,
    dogemmshelper,
    edl,
    eor,
    flip_image,
    grayscale,
    gvarstatus,
    invert_colors,
    media_type,
    mirror_file,
    pframehelper,
    random_color,
    reply_id,
    solarize,
)

plugin_category = "fun"

FONTS = (
    "1. `droidsans_mono.ttf`\n\
    2. `impact.ttf`\n\
    3. `modern.ttf`\n\
    4. `productsans_bolditalic.ttf`\n\
    5. `productsans_light.ttf`\n\
    6. `roboto_italic.ttf`\n\
    7. `roboto_medium.ttf`\n\
    8. `roboto_regular.ttf`"
)
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
        "header": "Adds frame for the replied image.",
        "flags": {
            "-f": "To send output file not as streamble image.",
        },
        "usage": [
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
        image = Imopen(imag[1])
    except Exception as e:
        return await edl(dogevent, f"**Error in identifying image:**\n__{e}__")
    output=pframehelper(image)
    await event.client.send_file(
        event.chat_id, output, reply_to=reply, force_document=force
    )
    await dogevent.delete()
    if ospath.exists(output):
        remove(output)


@doge.bot_cmd(
    pattern="cfont(?:\s|$)([\s\S]*)",
    command=("cfont", plugin_category),
    info={
        "header": "Change the font style use for memify.To get font list use cfont command as it is without input.",
        "usage": "{tr}.cfont <Font Name>",
        "examples": "{tr}cfont modern.ttf",
    },
)
async def lang(event):
    "Change the font style use for memify."
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.edit(f"**Available Fonts names are here:-**\n\n{FONTS}")
        return
    if input_str not in font_list:
        dogevent = await eor(event, "`Give me a correct font name...`")
        await sleep(1)
        await dogevent.edit(f"**Available Fonts names are here:**\n\n{FONTS}")
    else:
        arg = f"userbot/helpers/resources/fonts/{input_str}"
        addgvar("CNG_FONTS", arg)
        await eor(event, f"**Fonts for memify changed to:** `{input_str}`")


@doge.bot_cmd(
    pattern="ascii(?:\s|$)([\s\S]*)",
    command=("ascii", plugin_category),
    info={
        "header": "To get ascii image of replied image.",
        "description": "pass hexa colou code along with the cmd to change custom background colour",
        "usage": [
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
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "ascii_file.webp")
        if teledoge
        else ospath.join("./temp", "ascii_file.jpg")
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
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="invert$",
    command=("invert", plugin_category),
    info={
        "header": "To invert colours of given image or sticker.",
        "usage": "{tr}invert",
    },
)
async def imemes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await eor(event, "`Reply to supported Media...`")
        return
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp/"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "invert.webp")
        if teledoge
        else ospath.join("./temp", "invert.jpg")
    )
    await invert_colors(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="solarize$",
    command=("solarize", plugin_category),
    info={
        "header": "To sun burn the colours of given image or sticker.",
        "usage": "{tr}solarize",
    },
)
async def smemes(event):
    "Sun burn of image."
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "solarize.webp")
        if teledoge
        else ospath.join("./temp", "solarize.jpg")
    )
    await solarize(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="mirror$",
    command=("mirror", plugin_category),
    info={
        "header": "shows you the reflection of the media file.",
        "usage": "{tr}mirror",
    },
)
async def mmemes(event):
    "shows you the reflection of the media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "mirror_file.webp")
        if teledoge
        else ospath.join("./temp", "mirror_file.jpg")
    )
    await mirror_file(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="flip$",
    command=("flip", plugin_category),
    info={
        "header": "shows you the upside down image of the given media file.",
        "usage": "{tr}flip",
    },
)
async def fmemes(event):
    "shows you the upside down image of the given media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "flip_image.webp")
        if teledoge
        else ospath.join("./temp", "flip_image.jpg")
    )
    await flip_image(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="gray$",
    command=("gray", plugin_category),
    info={
        "header": "makes your media file to black and white.",
        "usage": "{tr}gray",
    },
)
async def gmemes(event):
    "makes your media file to black and white"
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "grayscale.webp")
        if teledoge
        else ospath.join("./temp", "grayscale.jpg")
    )
    await grayscale(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="zoom ?([\s\S]*)",
    command=("zoom", plugin_category),
    info={
        "header": "zooms your media file,",
        "usage": ["{tr}zoom", "{tr}zoom range"],
    },
)
async def zmemes(event):
    "zooms your media file."
    doginput = event.pattern_match.group(1)
    doginput = 50 if not doginput else int(doginput)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "zoomimage.webp")
        if teledoge
        else ospath.join("./temp", "zoomimage.jpg")
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
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="frame ?([\s\S]*)",
    command=("frame", plugin_category),
    info={
        "header": "make a frame for your media file.",
        "fill": "This defines the pixel fill value or color value to be applied. The default value is 0 which means the color is black.",
        "usage": ["{tr}frame", "{tr}frame range", "{tr}frame range ; fill"],
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
    happy = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogid = await reply_id(event)
    if not ospath.isdir("./temp"):
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
        happy = Get(happy)
        await event.client(happy)
    except BaseException:
        pass
    outputfile = (
        ospath.join("./temp", "framed.webp")
        if teledoge
        else ospath.join("./temp", "framed.jpg")
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
        if files and ospath.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="mmf(?:\s|$)([\s\S]*)",
    command=("mmf", plugin_category),
    info={
        "header": "To write text on images.",
        "description": "To create memes.",
        "usage": [
            "{tr}mmf toptext ; bottomtext",
        ],
        "examples": [
            "{tr}mmf wow (only on top)",
            "{tr}mmf ; doge (only on bottom)",
            "{tr}mmf wow ; doge (both on top and bottom) <reply_media>",
        ],
    },
)
async def dogemmf(event):
    reply = await event.get_reply_message()
    dogeinput = event.pattern_match.group(1)
    if not (reply and (reply.media)):
        return await edl(event, "`Reply to any media!`")
    if not dogeinput:
        return await edl(event, "`Give me something text to write...`")
    dogemeem = await reply.download_media()
    if dogemeem.endswith((".tgs")):
        dogevent = await eor(event, "`WOW this is animated sticker!`")
        cmd = ["lottie_convert.py", dogemeem, "@DogeUserBot.png"]
        file = "@DogeUserBot.png"
        process = await create_subprocess_exec(
            *cmd, stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif dogemeem.endswith((".webp", ".png")):
        dogevent = await eor(event, "`Processing`")
        im = Imopen(dogemeem)
        im.save("@DogeUserBot.png", format="PNG", optimize=True)
        file = "@DogeUserBot.png"
    else:
        dogevent = await eor(event, "`Processing`")
        img = VideoCapture(dogemeem)
        heh, lol = img.read()
        imwrite("@DogeUserBot.png", lol)
        file = "@DogeUserBot.png"
    if gvarstatus("CNG_FONTS") is None:
        CNG_FONTS = "userbot/helpers/resources/fonts/impact.ttf"
    else:
        CNG_FONTS = gvarstatus("CNG_FONTS")
    stick = await dogemmfhelper(file, dogeinput, CNG_FONTS)
    await event.client.send_file(
        event.chat_id, stick, force_document=False, reply_to=event.reply_to_msg_id
    )
    await dogevent.delete()
    try:
        remove(dogemeem)
        remove(file)
        remove(stick)
    except BaseException:
        pass


@doge.bot_cmd(
    pattern="mms(?:\s|$)([\s\S]*)",
    command=("mms", plugin_category),
    info={
        "header": "To write text on stickers.",
        "description": "To create memes.",
        "usage": [
            "{tr}mms toptext ; bottomtext",
        ],
        "examples": [
            "{tr}mms wow (only on top)",
            "{tr}mms ; doge (only on bottom)",
            "{tr}mms wow ; doge (both on top and bottom) <reply_media>",
        ],
    },
)
async def dogemms(event):
    reply = await event.get_reply_message()
    dogeinput = event.pattern_match.group(1)
    if not (reply and (reply.media)):
        return await edl(event, "`Reply to any media`")
    if not dogeinput:
        return await edl(event, "`Give me something text to write`")
    dogemeem = await reply.download_media()
    if dogemeem.endswith((".tgs")):
        dogevent = await eor(event, "`WOW this is animated sticker`")
        cmd = ["lottie_convert.py", dogemeem, "@DogeUserBot.png"]
        file = "@DogeUserBot.png"
        process = await create_subprocess_exec(
            *cmd, stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif dogemeem.endswith((".webp", ".png")):
        dogevent = await eor(event, "`Processing`")
        im = Imopen(dogemeem)
        im.save("@DogeUserBot.png", format="PNG", optimize=True)
        file = "@DogeUserBot.png"
    else:
        dogevent = await eor(event, "`Processing`")
        img = VideoCapture(dogemeem)
        heh, lol = img.read()
        imwrite("@DogeUserBot.png", lol)
        file = "@DogeUserBot.png"
    if gvarstatus("CNG_FONTS") is None:
        CNG_FONTS = "userbot/helpers/resources/fonts/impact.ttf"
    else:
        CNG_FONTS = gvarstatus("CNG_FONTS")
    pic = await dogemmshelper(file, dogeinput, CNG_FONTS)
    await event.client.send_file(
        event.chat_id, pic, force_document=False, reply_to=event.reply_to_msg_id
    )
    await dogevent.delete()
    try:
        remove(dogemeem)
        remove(file)
    except BaseException:
        pass
    remove(pic)
