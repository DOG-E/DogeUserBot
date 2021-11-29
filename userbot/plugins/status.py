# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import mkdir, path, remove
from urllib.request import urlretrieve

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest

from . import doge, edl, eor, gvar, sgvar

plugin_category = "tool"

OFFLINE_TAG = "[OFFLINE]"


@doge.bot_cmd(
    pattern="offline$",
    command=("offline", plugin_category),
    info={
        "h": "To your status as offline",
        "d": " it change your pic as offline, and add offline tag in name.",
        "u": "{tr}offline",
    },
)
async def off_line(event):
    "make yourself offline"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        return await edl(event, "**Already in Offline Mode.**")
    await eor(event, "**Changing Profile to Offline...**")
    photo = "./temp/donottouch.jpg"
    if not path.isdir("./temp"):
        mkdir("./temp")
    urlretrieve("https://telegra.ph/file/249f27d5b52a87babcb3f.jpg", photo)
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await event.client(UploadProfilePhotoRequest(file))
        except Exception as e:  # pylint:disable=C0103,W0703
            await eor(event, str(e))
        else:
            await eor(event, "**Changed profile to OffLine.**")
    remove(photo)
    first_name = user.first_name
    sgvar("my_first_name", first_name)
    last_name = user.last_name
    if last_name:
        sgvar("my_last_name", last_name)
    tag_name = OFFLINE_TAG
    await event.client(UpdateProfileRequest(last_name=first_name, first_name=tag_name))
    await edl(event, f"**`{tag_name} {first_name}`\nI am Offline now.**")


@doge.bot_cmd(
    pattern="online$",
    command=("online", plugin_category),
    info={
        "h": "To your status as online",
        "d": " it change your pic back normal, and remove offline tag in name.",
        "u": "{tr}online",
    },
)
async def on_line(event):
    "make yourself online"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        await eor(event, "**Changing Profile to Online...**")
    else:
        await edl(event, "**Already Online.**")
        return
    try:
        await event.client(
            DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await eor(event, str(e))
    else:
        await eor(event, "**Changed profile to Online.**")
    first_name = gvar("my_first_name")
    last_name = gvar("my_last_name") or ""
    await event.client(UpdateProfileRequest(last_name=last_name, first_name=first_name))
    await edl(event, f"**`{first_name} {last_name}`\nI am Online!**")
