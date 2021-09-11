# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import get_event_loop
from glob import glob
from io import open as iopen
from os import path as osp
from os import remove
from pathlib import Path
from re import search
from time import time

from telethon.tl.types import (
    DocumentAttributeAudio,
    DocumentAttributeVideo,
    InputMediaUploadedDocument,
)
from telethon.utils import get_attributes
from wget import download
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from ..core.pool import run_in_thread
from ..helpers.functions.utube import _mp3Dl
from . import (
    TEMP_DIR,
    _format,
    doge,
    edl,
    eor,
    get_yt_video_id,
    get_ytthumb,
    logging,
    progress,
    reply_id,
    ytsearch,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

BASE_YT_URL = "https://www.youtube.com/watch?v="
video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        {"key": "FFmpegMetadata"},
    ],
    "outtmpl": "%(title)s.mp4",
    "logtostderr": False,
    "quiet": True,
}


async def ytdl_down(event, opts, url):
    ytdl_data = None
    try:
        await event.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{DE}`")
    except ContentTooShortError:
        await event.edit("`The download content was too short.`")
    except GeoRestrictedError:
        await event.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
    except MaxDownloadsReached:
        await event.edit("`Max-downloads limit has been reached.`")
    except PostProcessingError:
        await event.edit("`There was an error during post processing.`")
    except UnavailableVideoError:
        await event.edit("`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await event.edit("`There was an error during info extraction.`")
    except Exception as e:
        await event.edit(f"**Error:** \n__{e}__")
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """Avoid multiple instances of an attribute."""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = True

    attributes, mime_type = get_attributes(path)
    if suffix == "mp3":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = DocumentAttributeAudio(
            duration=duration, voice=None, title=title, performer=uploader
        )
    elif suffix == "mp4":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=round_message,
            supports_streaming=supports_streaming,
        )

    if audio and isinstance(audio, DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, DocumentAttributeVideo):
        new_attributes.append(video)

    for attr in attributes:
        if (
            isinstance(attr, DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, DocumentAttributeAudio)
            and not video
            or not isinstance(attr, DocumentAttributeAudio)
            and not isinstance(attr, DocumentAttributeVideo)
        ):
            new_attributes.append(attr)
    return new_attributes, mime_type


@doge.bot_cmd(
    pattern="yta(?:\s|$)([\s\S]*)",
    command=("yta", plugin_category),
    info={
        "header": "To download audio from many sites like Youtube",
        "description": "downloads the audio from the given link (Suports the all sites which support youtube-dl)",
        "examples": ["{tr}yta <reply to link>", "{tr}yta <link>"],
    },
)
async def download_audio(event):
    """To download audio from YouTube and many other sites."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await eor(event, "`What I am Supposed to do? Give link`")
    dogevent = await eor(event, "`Preparing to download...`")
    reply_to_id = await reply_id(event)
    try:
        vid_data = YoutubeDL({"no-playlist": True}).extract_info(url, download=False)
    except ExtractorError:
        vid_data = {"title": url, "uploader": "Dogeuserbot", "formats": []}
    startTime = time()
    retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
    if retcode != 0:
        return await event.edit(str(retcode))
    _fpath = ""
    thumb_pic = None
    for _path in glob(osp.join(TEMP_DIR, str(startTime), "*")):
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
        else:
            _fpath = _path
    if not _fpath:
        return await edl(dogevent, "__Unable to upload file__")
    await dogevent.edit(
        f"`Preparing to upload video:`\
        \n**{vid_data['title']}**\
        \nby *{vid_data['uploader']}*"
    )
    attributes, mime_type = get_attributes(str(_fpath))
    ul = iopen(Path(_fpath), "rb")
    if thumb_pic is None:
        thumb_pic = str(
            await run_in_thread(download)(await get_ytthumb(get_yt_video_id(url)))
        )
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: get_event_loop().create_task(
            progress(
                d,
                t,
                dogevent,
                startTime,
                "trying to upload",
                file_name=osp.basename(Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        caption=f"<b>File Name: </b><code>{vid_data.get('title', osp.basename(Path(_fpath)))}</code>",
        reply_to=reply_to_id,
        parse_mode="html",
    )
    for _path in [_fpath, thumb_pic]:
        remove(_path)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="ytv(?:\s|$)([\s\S]*)",
    command=("ytv", plugin_category),
    info={
        "header": "To download video from many sites like Youtube",
        "description": "downloads the video from the given link(Suports the all sites which support youtube-dl)",
        "examples": [
            "{tr}ytv <reply to link>",
            "{tr}ytv <link>",
        ],
    },
)
async def download_video(event):
    """To download video from YouTube and many other sites."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await eor(event, "What I am Supposed to find? Give link")
    dogevent = await eor(event, "`Preparing to download...`")
    reply_to_id = await reply_id(event)
    ytdl_data = await ytdl_down(dogevent, video_opts, url)
    if ytdl_down is None:
        return
    f = Path(f"{ytdl_data['title']}.mp4".replace("|", "_"))
    dogthumb = Path(f"{ytdl_data['title']}.jpg".replace("|", "_"))
    if not osp.exists(dogthumb):
        dogthumb = Path(f"{ytdl_data['title']}.webp".replace("|", "_"))
    if not osp.exists(dogthumb):
        dogthumb = None
    await dogevent.edit(
        f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
    )
    ul = iopen(f, "rb")
    c_time = time()
    attributes, mime_type = await fix_attributes(f, ytdl_data, supports_streaming=True)
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: get_event_loop().create_task(
            progress(d, t, dogevent, c_time, "upload", file_name=f)
        ),
    )
    ul.close()
    media = InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        thumb=await event.client.upload_file(dogthumb) if dogthumb else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        reply_to=reply_to_id,
        caption=ytdl_data["title"],
    )
    remove(f)
    if dogthumb:
        remove(dogthumb)
    await event.delete()


@doge.bot_cmd(
    pattern="yts(?: |$)(\d*)? ?([\s\S]*)",
    command=("yts", plugin_category),
    info={
        "header": "To search youtube videos",
        "description": "Fetches youtube search results with views and duration with required no of count results by default it fetches 10 results",
        "examples": [
            "{tr}yts <query>",
            "{tr}yts <1-9> <query>",
        ],
    },
)
async def yt_search(event):
    "Youtube search command"
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edl(event, "`Reply to a message or pass a query to search!`")
    video_q = await eor(event, "`Searching...`")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edl(video_q, str(e), parse_mode=_format.parse_pre)
    reply_text = f"**•  Search Query:**\n`{query}`\n\n**•  Results:**\n{full_response}"
    await eor(video_q, reply_text)
