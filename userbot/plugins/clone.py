# Credits of Plugin @ViperAdnan and @mrconfused(revert)[will add sql soon]
from html import escape

from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.users import GetFullUserRequest

from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    Config,
    doge,
    edl,
    get_user_from_event,
    wowmydev,
)

plugin_category = "fun"

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else "🐶 @DogeUserBot 🐾"


@doge.bot_cmd(
    pattern="clone(?:\s|$)([\s\S]*)",
    command=("clone", plugin_category),
    info={
        "header": "To clone account of mentiond user or replied user",
        "usage": "{tr}clone <username/userid/reply>",
    },
)
async def _(event):
    "To clone account of mention user or replied user"
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    user_id = replied_user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(UpdateProfileRequest(first_name=first_name))
    await event.client(UpdateProfileRequest(last_name=last_name))
    await event.client(UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edl(event, f"**Failed to clone due to error:**\n__{e}__")
    await event.client(UploadProfilePhotoRequest(pfile))
    await edl(event, "**LET US BE AS ONE**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#CLONED\nSuccessfully cloned [{first_name}](tg://user?id={user_id })",
        )


@doge.bot_cmd(
    pattern="revert$",
    command=("revert", plugin_category),
    info={
        "header": "To revert back to your original name , bio and profile pic",
        "note": "For proper Functioning of this command you need to set AUTONAME and DEFAULT_BIO with your profile name and bio respectively.",
        "usage": "{tr}revert",
    },
)
async def _(event):
    "To reset your original details"
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
    )
    await event.client(UpdateProfileRequest(about=bio))
    await event.client(UpdateProfileRequest(first_name=name))
    await event.client(UpdateProfileRequest(last_name=blank))
    await edl(event, "successfully reverted to your account back")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#REVERT\nSuccessfully reverted back to your profile",
        )
