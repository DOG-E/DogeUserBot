import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import eor
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
        dogevent = await eor(event, f"`Transfiguration Time! Converting to ....`")
    else:
        dogevent = event
    dogmedia = None
    dogfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(dogfile):
        os.remove(dogfile)
    if mediatype == "Photo":
        dogmedia = await reply.download_media(file="./temp")
        im = Image.open(dogmedia)
        im.save(dogfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, dogfile, thumb=-1)
    elif mediatype == "Sticker":
        dogmedia = await reply.download_media(file="./temp")
        if dogmedia.endswith(".tgs"):
            dogecmd = f"lottie_convert.py --frame 0 -if lottie -of png '{dogmedia}' '{dogfile}'"
            stdout, stderr = (await runcmd(dogecmd))[:2]
            if stderr:
                LOGS.info(stdout + stderr)
        elif dogmedia.endswith(".webp"):
            im = Image.open(dogmedia)
            im.save(dogfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, dogfile, thumb=-1)
        if not os.path.exists(dogfile):
            dogmedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(dogfile, 0.1)
            except Exception:
                clip = clip.save_frame(dogfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            dogmedia = await reply.download_media(file="./temp")
            im = Image.open(dogmedia)
            im.save(dogfile)
    if dogmedia and os.path.lexists(dogmedia):
        os.remove(dogmedia)
    if os.path.lexists(dogfile):
        return dogevent, dogfile, mediatype
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
