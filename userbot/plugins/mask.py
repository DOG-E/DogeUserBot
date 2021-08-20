# credits to @mrconfused and @sandy1709

from os import makedirs, path, remove, stat

from telegraph import upload_file
from telegraph.exceptions import TelegraphException
from telethon.events import NewMessage

from . import (
    Config,
    awooify,
    baguette,
    convert_toimage,
    doge,
    eor,
    fsmessage,
    iphonex,
    lan,
    lolice,
)

plugin_category = "fun"


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
        return await eor(dogbot, "```reply to media message```")
    chat = "@Hazmat_Suit_Bot"
    if reply_message.sender.bot:
        return await eor(dogbot, "```Reply to actual users message.```")
    event = await dogbot.edit(lan("processing"))
    async with dogbot.client.conversation(chat) as conv:
        response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await response
        if response.text.startswith("Forward"):
            await event.edit(
                "```Can you kindly disable your forward privacy settings for good?```"
            )
        else:
            await dogbot.client.send_file(event.chat_id, response.message.media)
            await event.delete()
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="awooify$",
    command=("awooify", plugin_category),
    info={
        "header": "Check yourself by replying to image.",
        "usage": "{tr}awooify",
    },
)
async def dogbot(dogememes):
    "replied Image will be face of other image"
    replied = await dogememes.get_reply_message()
    if not path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await eor(dogememes, "reply to a supported media file")
    if replied.media:
        dogevent = await eor(dogememes, "passing to telegraph...")
    else:
        return await eor(dogememes, "reply to a supported media file")
    download_location = await dogememes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        remove(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await awooify(dog)
    await dogevent.delete()
    await dogememes.client.send_file(dogememes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="lolice$",
    command=("lolice", plugin_category),
    info={
        "header": "image masker check your self by replying to image.",
        "usage": "{tr}lolice",
    },
)
async def dogbot(dogememes):
    "replied Image will be face of other image"
    replied = await dogememes.get_reply_message()
    if not path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await eor(dogememes, "reply to a supported media file")
    if replied.media:
        dogevent = await eor(dogememes, "passing to telegraph...")
    else:
        return await eor(dogememes, "reply to a supported media file")
    download_location = await dogememes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        remove(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await lolice(dog)
    await dogevent.delete()
    await dogememes.client.send_file(dogememes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="bun$",
    command=("bun", plugin_category),
    info={
        "header": "reply to image and check yourself.",
        "usage": "{tr}bun",
    },
)
async def dogbot(dogememes):
    "replied Image will be face of other image"
    replied = await dogememes.get_reply_message()
    if not path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await eor(dogememes, "reply to a supported media file")
    if replied.media:
        dogevent = await eor(dogememes, "passing to telegraph...")
    else:
        return await eor(dogememes, "reply to a supported media file")
    download_location = await dogememes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        remove(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await baguette(dog)
    await dogevent.delete()
    await dogememes.client.send_file(dogememes.chat_id, dog, reply_to=replied)


@doge.bot_cmd(
    pattern="iphx$",
    command=("iphx", plugin_category),
    info={
        "header": "replied image as iphone x wallpaper.",
        "usage": "{tr}iphx",
    },
)
async def dogbot(dogememes):
    "replied image as iphone x wallpaper."
    replied = await dogememes.get_reply_message()
    if not path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not replied:
        return await eor(dogememes, "reply to a supported media file")
    if replied.media:
        dogevent = await eor(dogememes, "passing to telegraph...")
    else:
        return await eor(dogememes, "reply to a supported media file")
    download_location = await dogememes.client.download_media(
        replied, Config.TMP_DOWNLOAD_DIRECTORY
    )
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            remove(download_location)
            return await dogevent.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
        await dogevent.edit("generating image..")
    else:
        remove(download_location)
        return await dogevent.edit("the replied file is not supported")
    try:
        response = upload_file(download_location)
        remove(download_location)
    except TelegraphException as exc:
        remove(download_location)
        return await dogevent.edit("ERROR: " + str(exc))
    dog = f"https://telegra.ph{response[0]}"
    dog = await iphonex(dog)
    await dogevent.delete()
    await dogememes.client.send_file(dogememes.chat_id, dog, reply_to=replied)
