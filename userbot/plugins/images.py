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
from shutil import rmtree

from glitch_this import ImageGlitcher
from PIL.Image import new
from PIL.Image import open as Imopen
from PIL.ImageColor import getrgb
from PIL.ImageFilter import GaussianBlur
from PIL.ImageOps import flip, mirror

from ..helpers.google_image_download import googleimagesdownload
from . import (
    _dogetools,
    _dogeutils,
    clippy,
    convert_toimage,
    deepfry,
    doge,
    dotify,
    edl,
    eor,
    fsfile,
    fsmessage,
    media_type,
    mediatoarttext,
    newmsgres,
    reply_id,
)

plugin_category = "misc"


@doge.bot_cmd(
    pattern="img(?: |$)(\d*)? ?([\s\S]*)",
    command=("img", plugin_category),
    info={
        "header": "Google image search.",
        "description": "To search images in google. By default will send 3 images.you can get more images(upto 10 only by changing limit value as shown in usage and examples.",
        "usage": ["{tr}img <1-10> <query>", "{tr}img <query>"],
        "examples": [
            "{tr}img 10 DogeUserBot",
            "{tr}img DogeUserBot",
            "{tr}img 7 DogeUserBot",
        ],
    },
)
async def img_sampler(event):
    "Google image search."
    reply_to_id = await reply_id(event)
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await eor(event, "Reply to a message or pass a query to search!")
    dog = await eor(event, "**⏳ Processing...**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim > 10:
            lim = int(10)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(3)
    response = googleimagesdownload()
    arguments = {
        "keywords": query.replace(",", " "),
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await dog.edit(f"Error: \n`{e}`")
    lst = paths[0][query.replace(",", " ")]
    await event.client.send_file(event.chat_id, lst, reply_to=reply_to_id)
    rmtree(path.dirname(path.abspath(lst[0])))
    await dog.delete()


@doge.bot_cmd(
    pattern="imirror(s)? ?(.)?(l|r|u|b)?$",
    command=("imirror", plugin_category),
    info={
        "header": "Gives to reflected  image of one part on other part.",
        "description": "Additionaly use along with cmd i.e, imirrors to gib out put as sticker.",
        "flags": {
            ".l": "Right half will be reflection of left half.",
            ".r": "Left half will be reflection of right half.",
            ".u": "bottom half will be reflection of upper half.",
            ".b": "upper half will be reflection of bottom half.",
        },
        "usage": [
            "{tr}imirror <flag> - gives output as image",
            "{tr}imirrors <flag> - gives output as sticker",
        ],
        "examples": [
            "{tr}imirror .l",
            "{tr}imirrors .u",
        ],
    },
)
async def imirror(event):  # sourcery no-metrics
    "imgae refelection fun."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make mirror.__")
    dogevent = await event.edit("__Reflecting the image....__")
    args = event.pattern_match.group(1)
    if args:
        filename = "DogeUserBot.webp"
        f_format = "webp"
    else:
        filename = "DogeUserBot.jpg"
        f_format = "jpeg"
    try:
        imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
        if imag[1] is None:
            return await edl(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        image = Imopen(imag[1])
    except Exception as e:
        return await edl(dogevent, f"**Error in identifying image:**\n__{e}__")
    flag = event.pattern_match.group(3) or "r"
    w, h = image.size
    if w % 2 != 0 and flag in ["r", "l"] or h % 2 != 0 and flag in ["u", "b"]:
        image = image.resize((w + 1, h + 1))
        h, w = image.size
    if flag == "l":
        left = 0
        upper = 0
        right = w // 2
        lower = h
        nw = right
        nh = left
    elif flag == "r":
        left = w // 2
        upper = 0
        right = w
        lower = h
        nw = upper
        nh = upper
    elif flag == "u":
        left = 0
        upper = 0
        right = w
        lower = h // 2
        nw = left
        nh = lower
    elif flag == "b":
        left = 0
        upper = h // 2
        right = w
        lower = h
        nw = left
        nh = left
    temp = image.crop((left, upper, right, lower))
    temp = mirror(temp) if flag in ["l", "r"] else flip(temp)
    image.paste(temp, (nw, nh))
    img = BytesIO()
    img.name = filename
    image.save(img, f_format)
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="irotate(?: |$)(\d+)$",
    command=("irotate", plugin_category),
    info={
        "header": "To rotate the replied image or sticker",
        "usage": [
            "{tr}irotate <angel>",
        ],
    },
)
async def irotate(event):
    "To convert replied image or sticker to gif"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(
            event, "__Reply to photo or sticker to rotate it with given angle.__"
        )
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to rotate it with given angle. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    dogevent = await eor(event, "__Rotating the replied media...__")
    imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
    if imag[1] is None:
        return await edl(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    image = Imopen(imag[1])
    try:
        image = image.rotate(int(args), expand=True)
    except Exception as e:
        return await edl(event, "**Error**\n" + str(e))
    await event.delete()
    img = BytesIO()
    img.name = "DogeUserBot.png"
    image.save(img, "PNG")
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="iresize(?:\s|$)([\s\S]*)$",
    command=("iresize", plugin_category),
    info={
        "header": "To resize the replied image/sticker",
        "usage": [
            "{tr}iresize <dimension> will send square image of that dimension",
            "{tr}iresize <width> <height> will send square image of that dimension",
        ],
        "examples": ["{tr}iresize 250", "{tr}iresize 500 250"],
    },
)
async def iresize(event):
    "To resize the replied image/sticker"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to resize it.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to resize it. Animated sticker is not supported__",
        )
    args = (event.pattern_match.group(1)).split()
    dogevent = await eor(event, "__Resizeing the replied media...__")
    imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
    if imag[1] is None:
        return await edl(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    image = Imopen(imag[1])
    w, h = image.size
    nw, nh = None, None
    if len(args) == 1:
        try:
            nw, nh = int(args[0]), int(args[0])
        except ValueError:
            return await edl(dogevent, f"**Error:**\n__Invalid dimension.__")
    else:
        try:
            nw = int(args[0])
        except ValueError:
            return await edl(dogevent, f"**Error:**\n__Invalid width.__")
        try:
            nh = int(args[1])
        except ValueError:
            return await edl(dogevent, f"**Error:**\n__Invalid height.__")
    try:
        image = image.resize((nw, nh))
    except Exception as e:
        return await edl(dogevent, f"**Error:** __While resizing.\n{e}__")
    await event.delete()
    img = BytesIO()
    img.name = "DogeUserBot.png"
    image.save(img, "PNG")
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="square$",
    command=("square", plugin_category),
    info={
        "header": "Converts replied image to square image.",
        "usage": "{tr}square",
    },
)
async def square_cmd(event):
    "Converts replied image to square image."
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
        img = Imopen(imag[1])
    except Exception as e:
        return await edl(dogevent, f"**Error in identifying image:**\n__{e}__")
    w, h = img.size
    if w == h:
        return await edl(event, "__The replied image is already in 1:1 ratio__")
    _min, _max = min(w, h), max(w, h)
    bg = img.crop(((w - _min) // 2, (h - _min) // 2, (w + _min) // 2, (h + _min) // 2))
    bg = bg.filter(GaussianBlur(5))
    bg = bg.resize((_max, _max))
    bg.paste(img, ((_max - w) // 2, (_max - h) // 2))
    img = BytesIO()
    img.name = "img.jpg"
    bg.save(img)
    img.seek(0)
    await event.client.send_file(event.chat_id, img, reply_to=reply)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="clip ?([\s\S]*)",
    command=("clip", plugin_category),
    info={
        "header": "Convert media to sticker by clippy",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into sticker by clippy.",
        "usage": [
            "{tr}clip <reply to a media>",
        ],
    },
)
async def clipartx(event):
    "Make a media to clippy sticker"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edl(event, "`Reply to a media file!`")
    dogevent = await eor(event, "**⏳ Processing...**")
    c_id = await reply_id(event)
    if not path.isdir("./temp"):
        mkdir("./temp")
    output_file = path.join("./temp", "doge.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/doge.jpg")
    await clippy(event.client, output_file, event.chat_id, c_id)
    await dogevent.delete()
    if path.exists(output_file):
        remove(output_file)


@doge.bot_cmd(
    pattern="icolor ?([\s\S]*)",
    command=("icolor", plugin_category),
    info={
        "header": "Make color media",
        "description": "Reply to any media files like pic, gif, sticker, video and it will make colored image.",
        "usage": [
            "{tr}icolor <reply to a media>",
        ],
    },
)
async def colorizer(event):
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edl(event, "`Reply to a media file!`")

    chat = "@PhotoColorizerBot"
    dogevent = await eor(event, "**⏳ Processing...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Forward"):
            return await edl(
                dogevent,
                "`Can you kindly disable your forward privacy settings for good?`",
            )
        elif response.text.startswith("🇷🇺"):
            dogeclick = await event.client.get_messages(chat)
            await dogeclick[0].click(0)
            await conv.get_response()
            await event.client.forward_messages(chat, reply_message)
            response = await newmsgres(conv, chat)
        await dogevent.delete()
        await event.client.send_file(
            event.chat_id,
            response.message.media,
        )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="ipixel ?([\s\S]*)",
    command=("ipixel", plugin_category),
    info={
        "header": "Make pixel media",
        "description": "Reply to any media files like pic, gif, sticker, video and it will make pixelled image.",
        "usage": [
            "{tr}ipixel <reply to a media>",
        ],
    },
)
async def picture(event):
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edl(event, "`Reply to a media file!`")

    chat = "@PixelatorBot"
    dogevent = await eor(event, "**⏳ Processing...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Forward"):
            await edl(
                dogevent,
                "`Can you kindly disable your forward privacy settings for good?`",
            )
        else:
            await dogevent.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
            )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="dotify(?: |$)(\d+)?$",
    command=("dotify", plugin_category),
    info={
        "header": "To convert image into doted with black & white color image.",
        "usage": [
            "{tr}dotify <number>",
        ],
    },
)
async def pic_gifcmd(event):
    "To convert image into doted image"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make it doted image.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to make it doted image. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    if args:
        if args.isdigit():
            pix = int(args) if int(args) > 0 else 100
    else:
        pix = 50
    dogevent = await eor(event, "__🎞 Dotifying image...__")
    imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
    if imag[1] is None:
        return await edl(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    result = await dotify(imag[1], pix, True)
    await event.client.send_file(event.chat_id, result, reply_to=reply)
    await dogevent.delete()
    for i in [imag[1]]:
        if path.exists(i):
            remove(i)


@doge.bot_cmd(
    pattern="dotif(?: |$)(\d+)?$",
    command=("dotif", plugin_category),
    info={
        "header": "To convert image into doted with RGB color image.",
        "usage": [
            "{tr}dotif <number>",
        ],
    },
)
async def pic_gifcmd(event):
    "To convert image into doted image"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make it doted image.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to make it doted image. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    if args:
        if args.isdigit():
            pix = int(args) if int(args) > 0 else 100
    else:
        pix = 50
    dogevent = await eor(event, "__🎞 Dotifying image...__")
    imag = await _dogetools.media_to_pic(dogevent, reply, noedits=True)
    if imag[1] is None:
        return await edl(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    result = await dotify(imag[1], pix, False)
    await event.client.send_file(event.chat_id, result, reply_to=reply)
    await dogevent.delete()
    for i in [imag[1]]:
        if path.exists(i):
            remove(i)


@doge.bot_cmd(
    pattern="glitch(s)?(?: |$)([1-8])?",
    command=("glitch", plugin_category),
    info={
        "header": "Glitches the given Image.",
        "description": "Glitches the given mediafile (gif, stickers, image, videos) to a sticker/image and glitch range is from 1 to 8.\
                    If nothing is mentioned then by default it is 2",
        "options": {
            "glitch": "To output result as gif.",
            "glitchs": "To output result as sticker.",
        },
        "usage": ["{tr}glitch <1-8>", "{tr}glitch", "{tr}glitchs", "{tr}glitchs <1-8>"],
    },
)
async def glitch(event):
    "Glitches the given Image."
    cmd = event.pattern_match.group(1)
    doginput = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    dogid = await reply_id(event)
    if not path.isdir("./temp"):
        mkdir("./temp")
    doginput = int(doginput) if doginput else 2
    glitch_file = await _dogetools.media_to_pic(event, reply)
    if glitch_file[1] is None:
        return await edl(
            glitch_file[0], "__Unable to extract image from the replied message.__"
        )
    glitcher = ImageGlitcher()
    img = Imopen(glitch_file[1])
    if cmd:
        glitched = path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, doginput, color_offset=True)
        glitch_img.save(glitched)
        await event.client.send_file(event.chat_id, glitched, reply_to=dogid)
    else:
        glitched = path.join("./temp", "glitched.gif")
        glitch_img = glitcher.glitch_image(img, doginput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        teledoge = await event.client.send_file(event.chat_id, glitched, reply_to=dogid)
        await _dogeutils.unsavegif(event, teledoge)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and path.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="iascii ?([\s\S]*)",
    command=("iascii", plugin_category),
    info={
        "header": "Convert media to ascii art.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into ascii.",
        "usage": [
            "{tr}iascii <reply to a media>",
        ],
    },
)
async def asciiartx(event):
    "Make a media to ascii art"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edl(event, "```Reply to a media file...```")
    dogevent = await eor(event, "**⏳ Processing...**")
    c_id = await reply_id(event)
    if not path.isdir("./temp"):
        mkdir("./temp")
    output_file = path.join("./temp", "doge.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/doge.jpg")
    chat = "@AsciiArt_Bot"
    async with event.client.conversation(chat) as conv:
        await fsfile(event.client, output_file, chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Forward"):
            await edl(
                dogevent,
                "`Can you kindly disable your forward privacy settings for good?`",
            )
        else:
            await dogevent.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                reply_to=c_id,
            )
        await conv.mark_read()
        await conv.cancel_all()
    if path.exists(output_file):
        remove(output_file)


@doge.bot_cmd(
    pattern="line ?([\s\S]*)",
    command=("line", plugin_category),
    info={
        "header": "Convert media to line image.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into line image.",
        "usage": [
            "{tr}line <reply to a media>",
        ],
    },
)
async def lineartx(event):
    "Make a media to line image"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edl(event, "```Reply to a media file...```")
    dogevent = await eor(event, "**⏳ Processing...**")
    c_id = await reply_id(event)
    if not path.isdir("./temp"):
        mkdir("./temp")
    output_file = path.join("./temp", "doge.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/doge.jpg")
    chat = "@Lines50Bot"
    async with event.client.conversation(chat) as conv:
        await fsfile(event.client, output_file, chat)
        pic = await newmsgres(conv, chat)
        await dogevent.delete()
        await event.client.send_file(
            event.chat_id,
            pic.message.media,
            reply_to=c_id,
        )
        await conv.mark_read()
        await conv.cancel_all()
    if path.exists(output_file):
        remove(output_file)


@doge.bot_cmd(
    pattern="frybot",
    command=("frybot", plugin_category),
    info={
        "header": "Fries the given sticker or image.",
        "usage": "{tr}frybot",
    },
)
async def _(event):
    "Fries the given sticker or image"
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make it fried image.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to make it fried image. Animated sticker is not supported__",
        )
    chat = "@image_DeepFryBot"
    if reply.sender.bot:
        event = await eor(event, "Reply to actual users message.")
        return
    event = await eor(event, "**⏳ Processing...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Forward"):
            await event.edit(
                "`Can you kindly disable your forward privacy settings for good?`"
            )
        else:
            await event.client.send_file(
                event.chat_id, response.message.media, reply_to=reply_to
            )
        await event.delete()
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="deepfry(?: |$)([1-9])?",
    command=("deepfry", plugin_category),
    info={
        "header": "image fryer",
        "description": "Fries the given sticker or image based on level if you don't give anything then it is default to 1",
        "usage": [
            "{tr}deepfry <1 to 9>",
            "{tr}deepfry",
        ],
    },
)
async def deepfryer(event):
    "image fryer"
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    frycount = int(input_str) if input_str else 1
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make it fried image.__")

    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to make it fried image. Animated sticker is not supported__",
        )
    # download last photo (highres) as byte array
    image = BytesIO()
    await event.client.download_media(reply, image)
    image = Imopen(image)
    # fry the image
    hmm = await eor(event, "`Deep frying media…`")
    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.client.send_file(event.chat_id, fried_io, reply_to=reply_to)
    await hmm.delete()


@doge.bot_cmd(
    pattern="txtart$",
    command=("txtart", plugin_category),
    info={
        "header": "Make replied image into textart.",
        "description": "Reply to any sticker or image to convert it into text art.",
        "usage": "{tr}txtart reply to image/sticker",
    },
)
async def txt_art(event):
    "Make replied image into textart."
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    dogeid = await reply_id(event)
    if not path.isdir("./temp"):
        mkdir("./temp")
    dogemedia = None
    output = await _dogetools.media_to_pic(event, reply)
    if output[2] in ["Round Video", "Gif", "Sticker", "Video"]:
        dogemedia = True
    try:
        outputfile = mediatoarttext(dogemedia, output)
        await event.client.send_file(
            event.chat_id, outputfile, reply_to=dogeid, force_document=False
        )
        await output[0].delete()
        for files in (outputfile, output[1]):
            if files and path.exists(files):
                remove(files)
    except BaseException as e:
        system(output[1])
        await edl(output[0], f"**Error**\n`{str(e)}`")


@doge.bot_cmd(
    pattern="color ([\s\S]*)",
    command=("color", plugin_category),
    info={
        "header": "To get color pic of given hexa color code.",
        "usage": "{tr}color <colour code>",
        "examples": "{tr}color #ff0000",
    },
)
async def _(event):
    "To get color pic of given hexa color code."
    input_str = event.pattern_match.group(1)
    message_id = await reply_id(event)
    if not input_str.startswith("#"):
        return await eor(
            event, "**Syntax:** `.color <color_code>` example: `.color #ff0000`"
        )
    try:
        usercolor = getrgb(input_str)
    except Exception as e:
        return await event.edit(str(e))
    else:
        im = new(mode="RGB", size=(1280, 720), color=usercolor)
        im.save("@DogeUserBot.png", "PNG")
        input_str = input_str.replace("#", "#COLOR_")
        await event.client.send_file(
            event.chat_id,
            "@DogeUserBot.png",
            force_document=False,
            caption=input_str,
            reply_to=message_id,
        )
        remove("@DogeUserBot.png")
        await event.delete()
