# Ported from Uniborg (@spechide)
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import remove
from os.path import join

from requests import post

from . import (
    TEMP_DIR,
    convert_toimage,
    convert_tosticker,
    doge,
    edl,
    eor,
    gvar,
    reply_id,
)

plugin_category = "misc"


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": gvar("REMOVEBG_API"),
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": gvar("REMOVEBG_API"),
    }
    data = {"image_url": input_url}
    return post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )


@doge.bot_cmd(
    pattern="(rbg|srbg)(?:\s|$)([\s\S]*)",
    command=("rbg", plugin_category),
    info={
        "h": "To remove background of a image/sticker/image link.",
        "o": {
            "rbg": "to get output as png format",
            "srbg": "To get output as webp format(sticker).",
        },
        "u": [
            "{tr}rbg",
            "{tr}srbg",
            "{tr}rbg image link",
            "{tr}srbg image link",
        ],
    },
)
async def remove_background(event):
    "To remove background of a image."
    if gvar("REMOVEBG_API") is None:
        return await edl(
            event,
            "`You have to set REMOVEBG_API in Config vars with API token from remove.bg to use this plugin .`",
        )

    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    message_id = await reply_id(event)
    if event.reply_to_msg_id and not input_str:
        reply_message = await event.get_reply_message()
        dogevent = await eor(event, "`Analysing this Image/Sticker...`")
        file_name = join(TEMP_DIR, "rbg.png")
        try:
            await event.client.download_media(reply_message, file_name)
        except Exception as e:
            return await edl(dogevent, f"`{e}`", 5)

        else:
            await dogevent.edit("`Removing Background of this media`")
            file_name = convert_toimage(file_name)
            response = ReTrieveFile(file_name)
            remove(file_name)
    elif input_str:
        dogevent = await eor(event, "`Removing Background of this media`")
        response = ReTrieveURL(input_str)
    else:
        return await edl(
            event,
            "`Reply to any image or sticker with rbg/srbg to get background less png file or webp format or provide image link along with command`",
            5,
        )

    contentType = response.headers.get("content-type")
    remove_bg_image = "backgroundless.png"
    if "image" in contentType:
        with open("backgroundless.png", "wb") as removed_bg_file:
            removed_bg_file.write(response.content)
    else:
        return await edl(dogevent, f"`{response.content.decode('UTF-8')}`", 5)

    if cmd == "srbg":
        file = convert_tosticker(remove_bg_image, filename="backgroundless.webp")
        await event.client.send_file(
            event.chat_id,
            file,
            reply_to=message_id,
        )
    else:
        file = remove_bg_image
        await event.client.send_file(
            event.chat_id,
            file,
            force_document=True,
            reply_to=message_id,
        )
    await dogevent.delete()
