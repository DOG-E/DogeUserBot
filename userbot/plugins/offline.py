# Credits to @jisan7509 (@jisan09)
#
# Forked, developed and edited for @DogeUserbot
#
import os
import urllib

from telethon.tl import functions

from userbot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, gvarstatus

plugin_category = "utils"

OFFLINE_TAG = "[OFFLINE]"


@doge.ub(
    pattern="offline$",
    command=("offline", plugin_category),
    info={
        "header": "To your status as offline",
        "description": " it change your pic as offline, and add offline tag in name.",
        "usage": "{tr}offline",
    },
)
async def offlineyourself(event):
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        return await edit_delete(event, "**Already in Offline Mode.**")
    await edit_or_reply(event, "**Changing Profile to Offline...**")
    photo = "./temp/donottouch.jpg"
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    urllib.request.urlretrieve(
        "https://telegra.ph/file/249f27d5b52a87babcb3f.jpg", photo
    )
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:
            await edit_or_reply(event, str(e))
        else:
            await edit_or_reply(event, "**Changed profile to OffLine.**")
    os.remove(photo)
    first_name = user.first_name
    addgvar("my_first_name", first_name)
    last_name = user.last_name
    if last_name:
        addgvar("my_last_name", last_name)
    tag_name = OFFLINE_TAG
    await event.client(
        functions.account.UpdateProfileRequest(
            last_name=first_name, first_name=tag_name
        )
    )
    await edit_delete(event, f"**`{tag_name} {first_name}`\nI am Offline now.**")


@doge.ub(
    pattern="online$",
    command=("online", plugin_category),
    info={
        "header": "To your status as online",
        "description": " it change your pic back normal, and remove offline tag in name.",
        "usage": "{tr}online",
    },
)
async def onlineyourself(event):
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        await edit_or_reply(event, "**Changing Profile to Online...**")
    else:
        await edit_delete(event, "**Already Online.**")
        return
    try:
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
    except Exception as e:
        await edit_or_reply(event, str(e))
    else:
        await edit_or_reply(event, "**Changed profile to Online.**")
    first_name = gvarstatus("my_first_name")
    last_name = gvarstatus("my_last_name") or ""
    await event.client(
        functions.account.UpdateProfileRequest(
            last_name=last_name, first_name=first_name
        )
    )
    await edit_delete(event, f"**`{first_name} {last_name}`\nI am Online !**")
