from os import path as ospath
from os import remove
from typing import Optional

from lottie import exporters, parsers
from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import eor
from ..tools import media_type
from .utils import run_sync, runcmd

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
        dogevent = await eor(event, "**Transfiguration Time! Converting to...**")
    else:
        dogevent = event
    dogmedia = None
    dogfile = ospath.join("./temp/", "meme.png")
    if ospath.exists(dogfile):
        remove(dogfile)
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
        if not ospath.exists(dogfile):
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
    if dogmedia and ospath.lexists(dogmedia):
        remove(dogmedia)
    if ospath.lexists(dogfile):
        return dogevent, dogfile, mediatype
    return dogevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or ospath.join(
        "./temp/", f"{ospath.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if ospath.exists(thumb_image_path) else None


async def make_gif(event, reply, quality=None, fps=None):
    fps = fps or 1
    quality = quality or 256
    result_p = ospath.join("temp", "animation.gif")
    animation = parsers.tgs.parse_tgs(reply)
    with open(result_p, "wb") as result:
        await run_sync(exporters.gif.export_gif, animation, result, quality, fps)
    return result_p


async def thumb_from_audio(audio_path, output):
    await runcmd(f"ffmpeg -i {audio_path} -filter:v scale=500:500 -an {output}")
