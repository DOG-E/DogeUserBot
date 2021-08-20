from asyncio import get_event_loop
from datetime import datetime
from os import path, remove
from time import time

from . import Config, doge, edl, eor, progress, reply_id

plugin_category = "tool"

thumb_image_path = path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@doge.bot_cmd(
    pattern="rename ?(-f)? ([\s\S]*)",
    command=("rename", plugin_category),
    info={
        "header": "To rename and upload the replied file.",
        "flags": {"f": "will upload as file that is document not streamable."},
        "description": "If flag is not used then will upload as steamable file",
        "usage": [
            "{tr}rename <new file name>",
            "{tr}rename -f <new file name>",
        ],
    },
)
async def _(event):
    "To rename and upload the file"
    thumb = thumb_image_path if path.exists(thumb_image_path) else None
    flags = event.pattern_match.group(1)
    forcedoc = bool(flags)
    supsstream = not flags
    dogevent = await eor(
        event,
        "`Rename & upload in process...`",
    )
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(2)
    if not event.reply_to_msg_id:
        return await dogevent.edit(
            "**Syntax : **`.rename filename.extension` as reply to a Telegram media"
        )
    start = datetime.now()
    file_name = input_str
    reply_message = await event.get_reply_message()
    c_time = time()
    downloaded_file_name = path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name)
    downloaded_file_name = await event.client.download_media(
        reply_message,
        downloaded_file_name,
        progress_callback=lambda d, t: get_event_loop().create_task(
            progress(d, t, dogevent, c_time, "trying to download", file_name)
        ),
    )
    end = datetime.now()
    ms_one = (end - start).seconds
    try:
        thumb = await reply_message.download_media(thumb=-1)
    except Exception:
        thumb = thumb
    if not path.exists(downloaded_file_name):
        return await dogevent.edit(f"File Not Found {input_str}")
    c_time = time()
    doog = await event.client.send_file(
        event.chat_id,
        downloaded_file_name,
        force_document=forcedoc,
        supports_streaming=supsstream,
        allow_cache=False,
        reply_to=reply_to_id,
        thumb=thumb,
        progress_callback=lambda d, t: get_event_loop().create_task(
            progress(d, t, event, c_time, "trying to upload", downloaded_file_name)
        ),
    )
    end_two = datetime.now()
    remove(downloaded_file_name)
    ms_two = (end_two - end).seconds
    await edl(
        dogevent,
        f"`Downloaded file in {ms_one} seconds.\nAnd Uploaded in {ms_two} seconds.`",
    )
