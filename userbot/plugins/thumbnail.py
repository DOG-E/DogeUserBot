# Thumbnail Utilities ported from uniborg
# credits @spechide
from os import path, remove

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL.Image import open as Imopen

from . import Config, _dogetools, doge, eor, lan

plugin_category = "tool"

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@doge.bot_cmd(
    pattern="sthumb$",
    command=("sthumb", plugin_category),
    info={
        "header": "To save replied image as temporary thumb.",
        "usage": "{tr}sthumb",
    },
)
async def _(event):
    "To save replied image as temporary thumb."
    dogevent = await eor(event, lan("processing"))
    if not event.reply_to_msg_id:
        return await dogevent.edit("`Reply to a photo to save custom thumbnail`")
    downloaded_file_name = await event.client.download_media(
        await event.get_reply_message(), Config.TMP_DOWNLOAD_DIRECTORY
    )
    if downloaded_file_name.endswith(".mp4"):
        metadata = extractMetadata(createParser(downloaded_file_name))
        if metadata and metadata.has("duration"):
            duration = metadata.get("duration").seconds
        downloaded_file_name = await _dogetools.take_screen_shot(
            downloaded_file_name, duration
        )
    # https://stackoverflow.com/a/21669827/4723940
    Imopen(downloaded_file_name).convert("RGB").save(thumb_image_path, "JPEG")
    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
    remove(downloaded_file_name)
    await dogevent.edit(
        "Custom video/file thumbnail saved. This image will be used in the upload, till `.dthumb`."
    )


@doge.bot_cmd(
    pattern="dthumb$",
    command=("dthumb", plugin_category),
    info={
        "header": "To delete thumb image.",
        "usage": "{tr}dthumb",
    },
)
async def _(event):
    "To delete thumb image."
    if path.exists(thumb_image_path):
        remove(thumb_image_path)
    else:
        await eor(event, "`No thumbnail is set to clear`")
    await eor(event, "✅ Custom thumbnail deleted successfully.")


@doge.bot_cmd(
    pattern="thumb$",
    command=("thumb", plugin_category),
    info={
        "header": "To get thumbnail of given video or gives your present thumbnail.",
        "usage": "{tr}thumb",
    },
)
async def _(event):
    "To get thumbnail of given video or gives your present thumbnail"
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await r.download_media(thumb=-1)
        except Exception as e:
            return await eor(event, str(e))
        try:
            await event.client.send_file(
                event.chat_id,
                a,
                force_document=False,
                allow_cache=False,
                reply_to=event.reply_to_msg_id,
            )
            remove(a)
            await event.delete()
        except Exception as e:
            await eor(event, str(e))
    elif path.exists(thumb_image_path):
        caption_str = "Current thumbnail"
        await event.client.send_file(
            event.chat_id,
            thumb_image_path,
            caption=caption_str,
            force_document=False,
            allow_cache=False,
            reply_to=event.message.id,
        )
    else:
        await eor(
            event,
            "No thumbnails have been saved.\nWrite `.sthumb` as a reply to a media",
        )
