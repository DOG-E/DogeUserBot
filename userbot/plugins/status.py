from os import mkdir, path, remove
from urllib.request import urlretrieve

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest

from . import addgvar, doge, edl, eor, gvarstatus

plugin_category = "tool"

OFFLINE_TAG = "[OFFLINE]"


@doge.bot_cmd(
    pattern="offline$",
    command=("offline", plugin_category),
    info={
        "header": "To your status as offline",
        "description": " it change your pic as offline, and add offline tag in name.",
        "usage": "{tr}offline",
    },
)
async def pussy(event):
    "make yourself offline"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        return await edl(event, "**Already in Offline Mode.**")
    await eor(event, "**Changing Profile to Offline...**")
    photo = "./temp/donottouch.jpg"
    if not path.isdir("./temp"):
        mkdir("./temp")
    urlretrieve(
        "https://telegra.ph/file/249f27d5b52a87babcb3f.jpg", photo
    )
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
    addgvar("my_first_name", first_name)
    last_name = user.last_name
    if last_name:
        addgvar("my_last_name", last_name)
    tag_name = OFFLINE_TAG
    await event.client(
        UpdateProfileRequest(
            last_name=first_name, first_name=tag_name
        )
    )
    await edl(event, f"**`{tag_name} {first_name}`\nI am Offline now.**")


@doge.bot_cmd(
    pattern="online$",
    command=("online", plugin_category),
    info={
        "header": "To your status as online",
        "description": " it change your pic back normal, and remove offline tag in name.",
        "usage": "{tr}online",
    },
)
async def dog(event):
    "make yourself online"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        await eor(event, "**Changing Profile to Online...**")
    else:
        await edl(event, "**Already Online.**")
        return
    try:
        await event.client(
            DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await eor(event, str(e))
    else:
        await eor(event, "**Changed profile to Online.**")
    first_name = gvarstatus("my_first_name")
    last_name = gvarstatus("my_last_name") or ""
    await event.client(
        UpdateProfileRequest(
            last_name=last_name, first_name=first_name
        )
    )
    await edl(event, f"**`{first_name} {last_name}`\nI am Online!**")
