# credits to @mrconfused and @sandy1709

import os

from telegraph import exceptions, upload_file
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import doge

from ..Config import Config
from ..core.managers import edit_or_reply
from . import awooify, baguette, convert_toimage, iphonex, lolice

plugin_category = "extra"


@doge.bot_cmd(
    pattern="mask$",
    command=("mask", plugin_category),
    info={
        "header": "reply to image to get hazmat suit for that image.",
        "usage": "{tr}mask",
    },
)
async def _(dogbot):
    "Hazmat suit maker"
    reply_message = await dogbot.get_reply_message()
    if not reply_message.media or not reply_message:
        return await edit_or_reply(dogbot, "```reply to media message```")
    chat = "@hazmat_suit_bot"
    if reply_message.sender.bot:
        return await edit_or_reply(dogbot, "```Reply to actual users message.```")
    event = await dogbot.edit("```Processing```")
    async with dogbot.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=905164246)
            )
            await dogbot.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            return await event.edit(
                "```Please unblock @hazmat_suit_bot and try again```"
            )
        if response.text.startswith("Forward"):
            await event.edit(
                "```can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await dogbot.client.send_file(event.chat_id, response.message.media)
            await event.delete()


@doge.bot_cmd(
    pattern="awooify$",
    command=("awooify", plugin_category),
    info={
        "header": "Check yourself by replying to image.",
        "usage": "{tr}awooify",
    },
)
async def dogbot(dogmemes):
    "replied Image will be face of other image"
    replied = await dogmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    if replied.media:
        dogevent = await edit_or_reply(dogmemes, "passing to telegraph...")
    else:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    download_location = await dogmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            os.remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        os.remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await awooify(dog)
    await dogevent.delete()
    await dogmemes.client.send_file(dogmemes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="lolice$",
    command=("lolice", plugin_category),
    info={
        "header": "image masker check your self by replying to image.",
        "usage": "{tr}lolice",
    },
)
async def dogbot(dogmemes):
    "replied Image will be face of other image"
    replied = await dogmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    if replied.media:
        dogevent = await edit_or_reply(dogmemes, "passing to telegraph...")
    else:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    download_location = await dogmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            os.remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        os.remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await lolice(dog)
    await dogevent.delete()
    await dogmemes.client.send_file(dogmemes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="bun$",
    command=("bun", plugin_category),
    info={
        "header": "reply to image and check yourself.",
        "usage": "{tr}bun",
    },
)
async def dogbot(dogmemes):
    "replied Image will be face of other image"
    replied = await dogmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    if replied.media:
        dogevent = await edit_or_reply(dogmemes, "passing to telegraph...")
    else:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    download_location = await dogmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            os.remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        os.remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await baguette(dog)
    await dogevent.delete()
    await dogmemes.client.send_file(dogmemes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="iphx$",
    command=("iphx", plugin_category),
    info={
        "header": "replied image as iphone x wallpaper.",
        "usage": "{tr}iphx",
    },
)
async def dogbot(dogmemes):
    "replied image as iphone x wallpaper."
    replied = await dogmemes.get_reply_message()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    if replied.media:
        dogevent = await edit_or_reply(dogmemes, "passing to telegraph...")
    else:
        return await edit_or_reply(dogmemes, "reply to a supported media file")
    download_location = await dogmemes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            os.remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        os.remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        os.remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await iphonex(dog)
    await dogevent.delete()
    await dogmemes.client.send_file(dogmemes.chat_id, dog, reply_to=replied)
