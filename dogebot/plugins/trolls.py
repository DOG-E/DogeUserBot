#    Copyright (C) 2020  sandeep.n(π.$)
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import os

from telegraph import exceptions, upload_file

from dogebot import doge

from ..core.managers import edit_or_reply
from ..helpers.utils import _dogetools, reply_id
from . import convert_toimage, deEmojify, phcomment, threats, trap, trash

plugin_category = "fun"


@doge.ub(
    pattern="trash$",
    command=("trash", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}trash",
    },
)
async def dogebot(event):
    "image meme creator."
    replied = await event.get_reply_message()
    dogeid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await event.reply(file=download_location)
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**Error: **\n`{str(exc)}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await trash(dog)
    os.remove(download_location)
    await output[0].delete()
    await event.client.send_file(event.chat_id, dog, reply_to=dogeid)


@doge.ub(
    pattern="threats$",
    command=("threats", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "usage": "{tr}threats",
    },
)
async def dogebot(event):
    "image meme creator."
    replied = await event.get_reply_message()
    dogeid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**Error: **\n`{str(exc)}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await threats(dog)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogeid)


@doge.ub(
    pattern="trap(?:\s|$)([\s\S]*)",
    command=("trap", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "Description": "creates a trap card",
        "usage": "{tr}trap (name of the person to trap) ; (trapper name)",
    },
)
async def dogebot(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        text1, text2 = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap);(trapper name)`",
        )
    replied = await event.get_reply_message()
    dogeid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )
    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**Error: **\n`{str(exc)}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await trap(text1, text2, dog)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogeid)


@doge.ub(
    pattern="phub(?:\s|$)([\s\S]*)",
    command=("phub", plugin_category),
    info={
        "header": "Reply to image/sticker to get meme on that image.",
        "description": "pornhub comment creator",
        "usage": "{tr}phub (username);(text in comment)",
    },
)
async def dogebot(event):
    "image meme creator."
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if ";" in input_str:
        username, text = input_str.split(";")
    else:
        return await edit_or_reply(
            event,
            "**Syntax :** reply to image or sticker with `.phub (username);(text in comment)`",
        )
    replied = await event.get_reply_message()
    dogeid = await reply_id(event)
    if not replied:
        return await edit_or_reply(event, "reply to a supported media file")
    output = await _dogetools.media_to_pic(event, replied)
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    download_location = convert_toimage(output[1])
    size = os.stat(download_location).st_size
    if size > 5242880:
        os.remove(download_location)
        return await output[0].edit(
            "the replied file size is not supported it must me below 5 mb"
        )

    await output[0].edit("generating image..")
    try:
        response = upload_file(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await output[0].edit(f"**Error: **\n`{str(exc)}`")
    dog = f"https://telegra.ph{response[0]}"
    dog = await phcomment(dog, text, username)
    await output[0].delete()
    os.remove(download_location)
    await event.client.send_file(event.chat_id, dog, reply_to=dogeid)
