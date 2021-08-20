from asyncio import get_event_loop, sleep
from datetime import datetime
from io import FileIO
from math import floor
from os import getcwd, makedirs
from os import path as osp
from pathlib import Path
from time import time

from pySmartDL import SmartDL
from telethon.tl.types import DocumentAttributeFilename
from telethon.utils import get_extension

from . import Config, _format, doge, edl, eor, humanbytes, progress

plugin_category = "misc"

NAME = "untitled"
downloads = Path(osp.join(getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@doge.bot_cmd(
    pattern="d(own)?l(oad)?(?:\s|$)([\s\S]*)",
    command=("download", plugin_category),
    info={
        "header": "To download the replied telegram file",
        "description": "Will download the replied telegram file to server .",
        "note": "The downloaded files will auto delete if you restart heroku.",
        "usage": [
            "{tr}download <reply>",
            "{tr}dl <reply>",
            "{tr}download custom name<reply>",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    "To download the replied telegram file"
    mone = await eor(event, "`Downloading....`")
    input_str = event.pattern_match.group(3)
    name = NAME
    path = None
    if not osp.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    reply = await event.get_reply_message()
    if reply:
        start = datetime.now()
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, DocumentAttributeFilename):
                name = attr.file_name
        if input_str:
            path = Path(osp.join(downloads, input_str.strip()))
        else:
            path = Path(osp.join(downloads, name))
        ext = get_extension(reply.document)
        if path and not path.suffix and ext:
            path = path.with_suffix(ext)
        if name == NAME:
            name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
        if path and path.exists():
            if path.is_file():
                newname = str(path.stem) + "_OLD"
                path.rename(path.with_name(newname).with_suffix(path.suffix))
                file_name = path
            else:
                file_name = path / name
        elif path and not path.suffix and ext:
            file_name = downloads / path.with_suffix(ext)
        elif path:
            file_name = path
        else:
            file_name = downloads / name
        file_name.parent.mkdir(parents=True, exist_ok=True)
        c_time = time()
        if (
            not reply.document
            and reply.photo
            and file_name
            and file_name.suffix
            or not reply.document
            and not reply.photo
        ):
            await reply.download_media(
                file=file_name.absolute(),
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        elif not reply.document:
            file_name = await reply.download_media(
                file=downloads,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        else:
            dl = FileIO(file_name.absolute(), "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            dl.close()
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{osp.relpath(file_name,getcwd())}`\n   "
        )
    elif input_str:
        start = datetime.now()
        if "|" in input_str:
            url, file_name = input_str.split("|")
        else:
            url = input_str
            file_name = None
        url = url.strip()
        file_name = osp.basename(url) if file_name is None else file_name.strip()
        downloaded_file_name = Path(osp.join(downloads, file_name))
        if not downloaded_file_name.suffix:
            ext = osp.splitext(url)[1]
            downloaded_file_name = downloaded_file_name.with_suffix(ext)
        downloader = SmartDL(url, str(downloaded_file_name), progress_bar=False)
        downloader.start(blocking=False)
        c_time = time()
        delay = 0
        oldmsg = ""
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            now = time()
            delay = now - c_time
            percentage = downloader.get_progress() * 100
            dspeed = downloader.get_speed()
            progress_str = "`{0}{1} {2}`%".format(
                "".join("▰" for i in range(floor(percentage / 5))),
                "".join("▱" for i in range(20 - floor(percentage / 5))),
                round(percentage, 2),
            )
            estimated_total_time = downloader.get_eta(human=True)
            current_message = f"Downloading the file\
                                \n\n**URL : **`{url}`\
                                \n**File Name :** `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)} of {humanbytes(total_length)} @ {humanbytes(dspeed)}`\
                                \n**ETA : **`{estimated_total_time}`"
            if oldmsg != current_message and delay > 5:
                await mone.edit(current_message)
                delay = 0
                c_time = time()
                oldmsg = current_message
            await sleep(1)
        end = datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await mone.edit(
                f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded file location :- ** `{osp.relpath(downloaded_file_name,getcwd())}`"
            )
        else:
            await mone.edit("Incorrect URL\n {}".format(input_str))
    else:
        await mone.edit("`Reply to a message to download to my local server.`")


@doge.bot_cmd(
    pattern="d(own)?l(oad)?to(?:\s|$)([\s\S]*)",
    command=("dlto", plugin_category),
    info={
        "header": "To download the replied telegram file to specific directory",
        "description": "Will download the replied telegram file to server that is your custom folder.",
        "note": "The downloaded files will auto delete if you restart heroku.",
        "usage": [
            "{tr}downloadto <folder path>",
            "{tr}dlto <folder path>",
        ],
    },
)
async def _(event):  # sourcery no-metrics
    pwd = getcwd()
    input_str = event.pattern_match.group(3)
    if not input_str:
        return await edl(
            event,
            "Where should i save this file. mention folder name",
            parse_mode=_format.parse_pre,
        )

    location = osp.join(pwd, input_str)
    if not osp.isdir(location):
        makedirs(location)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(
            event,
            "Reply to media file to download it to bot server",
            parse_mode=_format.parse_pre,
        )
    mone = await eor(event, "Downloading the file ...", parse_mode=_format.parse_pre)
    start = datetime.now()
    for attr in getattr(reply.document, "attributes", []):
        if isinstance(attr, DocumentAttributeFilename):
            name = attr.file_name
    if input_str:
        path = Path(osp.join(location, input_str.strip()))
    else:
        path = Path(osp.join(location, name))
    ext = get_extension(reply.document)
    if path and not path.suffix and ext:
        path = path.with_suffix(ext)
    if name == NAME:
        name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
    if path and path.exists():
        if path.is_file():
            newname = str(path.stem) + "_OLD"
            path.rename(path.with_name(newname).with_suffix(path.suffix))
            file_name = path
        else:
            file_name = path / name
    elif path and not path.suffix and ext:
        file_name = location / path.with_suffix(ext)
    elif path:
        file_name = path
    else:
        file_name = location / name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    c_time = time()
    if (
        not reply.document
        and reply.photo
        and file_name
        and file_name.suffix
        or not reply.document
        and not reply.photo
    ):
        await reply.download_media(
            file=file_name.absolute(),
            progress_callback=lambda d, t: get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    elif not reply.document:
        file_name = await reply.download_media(
            file=location,
            progress_callback=lambda d, t: get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    else:
        dl = FileIO(file_name.absolute(), "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
            progress_callback=lambda d, t: get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
        dl.close()
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{osp.relpath(file_name,getcwd())}`\n   "
    )
