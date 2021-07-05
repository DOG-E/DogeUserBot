# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import edit_or_reply
from ..tools import media_type
from .utils import runcmd

LOGS = logging.getLogger(__name__)


async def media_to_pic(event, reply, noedits=False):  # sourcery no-metrics
    mediatype = media_type(reply)
    if mediatype not in [
        "Photo",
        "Round Video",
        "Gif",
        "Sticker",
        "Video",
        "Voice",
        "Audio",
        "Document",
    ]:
        return event, None
    if not noedits:
        dogevent = await edit_or_reply(
            event, f"`Transfiguration Time! Converting to ....`"
        )
    else:
        dogevent = event
    dogemedia = None
    dogefile = os.path.join("./temp/", "meme.png")
    if os.path.exists(dogefile):
        os.remove(dogefile)
    if mediatype == "Photo":
        dogemedia = await reply.download_media(file="./temp")
        im = Image.open(dogemedia)
        im.save(dogefile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, dogefile, thumb=-1)
    elif mediatype == "Sticker":
        dogemedia = await reply.download_media(file="./temp")
        if dogemedia.endswith(".tgs"):
            dogecmd = f"lottie_convert.py --frame 0 -if lottie -of png '{dogemedia}' '{dogefile}'"
            stdout, stderr = (await runcmd(dogecmd))[:2]
            if stderr:
                LOGS.info(stdout + stderr)
        elif dogemedia.endswith(".webp"):
            im = Image.open(dogemedia)
            im.save(dogefile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, dogefile, thumb=-1)
        if not os.path.exists(dogefile):
            dogemedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(dogefile, 0.1)
            except:
                clip = clip.save_frame(dogefile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            dogemedia = await reply.download_media(file="./temp")
            im = Image.open(dogemedia)
            im.save(dogefile)
    if dogemedia and os.path.lexists(dogemedia):
        os.remove(dogemedia)
    if os.path.lexists(dogefile):
        return dogevent, dogefile, mediatype
    return dogevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
