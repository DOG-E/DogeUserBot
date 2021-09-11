# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import makedirs, path, remove, stat

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import (
    DeletePhotosRequest,
    GetUserPhotosRequest,
    UploadProfilePhotoRequest,
)
from telethon.tl.types import InputPhoto

from . import TMP_DOWNLOAD_DIRECTORY, doge, edl, eor, logging, sgvar

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile picture changed successfully.```"
PP_TOO_SMOL = "```This image is too small, use a bigger image.```"
PP_ERROR = "```Failure occured while processing image.```"
BIO_SUCCESS = "```Successfully edited Bio.```"
NAME_OK = "```Your name was successfully changed.```"
USERNAME_SUCCESS = "```Your username was successfully changed.```"
USERNAME_TAKEN = "```This username is already taken.```"
# ===============================================================


@doge.bot_cmd(
    pattern="pbio ([\s\S]*)",
    command=("pbio", plugin_category),
    info={
        "header": "To set bio for this account.",
        "usage": "{tr}pbio <your bio>",
    },
)
async def _(event):
    "To set bio for this account."
    bio = event.pattern_match.group(1)
    try:
        if len(bio) < 70:
            await event.client(UpdateProfileRequest(about=bio))
            sgvar("AFKRBIO", bio)
            await edl(event, "`Successfully changed my profile bio`")
        else:
            return await edl(
                event,
                "**🚧 Max bio length is 70 characters.**",
            )
    except Exception as e:
        await edl(event, f"**🚨 ERROR:**\n{e}")


@doge.bot_cmd(
    pattern="pname ([\s\S]*)",
    command=("pname", plugin_category),
    info={
        "header": "To set/change name for this account.",
        "usage": ["{tr}pname firstname ; last name", "{tr}pname firstname"],
    },
)
async def _(event):
    "To set/change name for this account."
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split(";", 1)
    try:
        await event.client(
            UpdateProfileRequest(first_name=first_name, last_name=last_name)
        )
        await edl(event, "`My name was changed successfully`")
    except Exception as e:
        await eor(event, f"**Error:**\n`{e}`")


@doge.bot_cmd(
    pattern="ppic$",
    command=("ppic", plugin_category),
    info={
        "header": "To set profile pic for this account.",
        "usage": "{tr}ppic <reply to image or gif>",
    },
)
async def _(event):
    "To set profile pic for this account."
    reply_message = await event.get_reply_message()
    dogevent = await eor(event, "`Downloading Profile Picture to my local ...`")
    if not path.isdir(TMP_DOWNLOAD_DIRECTORY):
        makedirs(TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(reply_message, TMP_DOWNLOAD_DIRECTORY)
    except Exception as e:
        await dogevent.edit(str(e))
    else:
        if photo:
            await dogevent.edit("`now, Uploading to Telegram ...`")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = stat(photo).st_size
                if size > 2097152:
                    await dogevent.edit("`size must be less than 2 mb`")
                    remove(photo)
                    return
                dogepic = None
                dogevideo = await event.client.upload_file(photo)
            else:
                dogepic = await event.client.upload_file(photo)
                dogevideo = None
            try:
                await event.client(
                    UploadProfilePhotoRequest(
                        file=dogepic, video=dogevideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await dogevent.edit(f"**Error:**\n`{e}`")
            else:
                await eor(dogevent, "`My profile picture was successfully changed`")
    try:
        remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@doge.bot_cmd(
    pattern="pusername ([\s\S]*)",
    command=("pusername", plugin_category),
    info={
        "header": "To set/update username for this account.",
        "usage": "{tr}pusername <new username>",
    },
)
async def update_username(event):
    """For .username command, set a new username in Telegram."""
    newusername = event.pattern_match.group(1)
    try:
        await event.client(UpdateUsernameRequest(newusername))
        await edl(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await eor(event, USERNAME_TAKEN)
    except Exception as e:
        await eor(event, f"**Error:**\n`{e}`")


@doge.bot_cmd(
    pattern="delpfp ?([\s\S]*)",
    command=("delpfp", plugin_category),
    info={
        "header": "To delete profile pic for this account.",
        "description": "If you haven't mentioned no of profile pics then only 1 will be deleted.",
        "usage": ["{tr}delpfp <no of pics to be deleted>", "{tr}delpfp"],
    },
)
async def remove_profilepic(delpfp):
    """For .delpfp command, delete your current profile picture in Telegram."""
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edl(delpfp, f"`Successfully deleted {len(input_photos)} profile picture(s).`")


@doge.bot_cmd(
    pattern="myusernames$",
    command=("myusernames", plugin_category),
    info={
        "header": "To list public channels or groups created by this account.",
        "usage": "{tr}myusernames",
    },
)
async def _(event):
    "To list all public channels and groups."
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "**Your current reserved usernames are:**\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await eor(event, output_str)
