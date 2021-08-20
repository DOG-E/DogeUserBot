# credits to @mrconfused and @sandy1709
#    Copyright (C) 2020  sandeep.n(π.$)

from os import remove, stat

from telegraph import upload_file
from telegraph.exceptions import TelegraphException
from telethon.tl.functions.users import GetFullUserRequest

from . import (
    ALIVE_NAME,
    _dogetools,
    convert_toimage,
    deEmojify,
    doge,
    edl,
    eor,
    phcomment,
    reply_id,
    threats,
    trap,
    trash,
)

plugin_category = "fun"


@doge.bot_cmd(
    pattern="trash$",
    command=("trash", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}trash",
    },
)
async def dogbot(event):
    "image meme creator."
    replied = await event.get_reply_message()
    dogid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = stat(download_location).st_size
    if size > 5242880:
        remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await event.reply(file=download_location)
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await output[0].edit(f"**Error: **\n`{exc}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await trash(dog)
    remove(download_location)
    await output[0].delete()
    await event.client.send_file(event.chat_id, dog, reply_to=dogid)


@doge.bot_cmd(
    pattern="threats$",
    command=("threats", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}threats",
    },
)
async def dogbot(event):
    "image meme creator."
    replied = await event.get_reply_message()
    dogid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = stat(download_location).st_size
    if size > 5242880:
        remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await output[0].edit(f"**Error: **\n`{exc}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await threats(dog)
    await output[0].delete()
    remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogid)


@doge.bot_cmd(
    pattern="trap(?:\s|$)([\s\S]*)",
    command=("trap", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "Description": "creates a trap card",
        "usage": "{tr}trap (name of the person to trap) ; (trapper name)",
    },
)
async def dogbot(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        return await eor(
            event,
            "**Syntax:** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
    replied = await event.get_reply_message()
    dogid = await reply_id(event)
    if not replied:
        return await eor(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = stat(download_location).st_size
    if size > 5242880:
        remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await output[0].edit(f"**Error: **\n`{exc}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await trap(text1, text2, dog)
    await output[0].delete()
    remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogid)


@doge.bot_cmd(
    pattern="phub(?:\s|$)([\s\S]*)",
    command=("phub", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "description": "pornhub comment creator",
        "usage": [
            "{tr}phub <username>;<text in comment> <reply a pic>",
        ],
    },
)
async def dogbot(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    reply = await event.get_reply_message()
    if ";" in input_str:
        username, text = input_str.split(";")
    elif not input_str and event.is_reply:
        text = reply.message
        getuser = await event.client(GetFullUserRequest(reply.from_id))
        username = getuser.user.first_name
    elif input_str and event.is_reply:
        text = input_str
        getuser = await event.client(GetFullUserRequest(reply.from_id))
        username = getuser.user.first_name
    elif input_str:
        text = input_str
        username = ALIVE_NAME
    else:
        return await edl(
            event,
            "what should I tweet? Give some text and format must be like `.tweet much text` ",
            5,
        )
    dogid = await reply_id(event)
    if reply.media:
        output = await _dogetools.media_to_pic(event, reply)
        if output[1] is None:
            return await edl(
                output[0], "__Unable to extract image from the replied message.__"
            )
        download_location = convert_toimage(output[1])
        size = stat(download_location).st_size
        if size > 5242880:
            remove(download_location)
            return await output[0].edit(
                "the replied file size is not supported it must me below 5 mb"
            )

        await output[0].edit("generating image..")
        try:
            response = upload_file(download_location)
        except TelegraphException as exc:
            remove(download_location)
            return await output[0].edit(f"**Error: **\n`{exc}`")
        dog = f"https://telegra.ph{response[0]}"
    elif not reply.media:
        dog = "https://telegra.ph/file/b7e740bbda31d43d510ab.jpg"
    dog = await phcomment(dog, text, username)
    await output[0].delete()
    remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogid)
