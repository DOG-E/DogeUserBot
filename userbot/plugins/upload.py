from asyncio import get_event_loop
from datetime import datetime
from io import open as iopen
from os import listdir
from os import path as osp
from os import walk
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen
from time import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import InputMediaUploadedDocument
from telethon.utils import get_attributes

from . import Config, doge, edl, eor, progress, reply_id

plugin_category = "misc"

PATH = osp.join("./temp", "temp_vid.mp4")
thumb_image_path = osp.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
downloads = Path("./downloads/").absolute()
NAME = "untitled"


class UPLOAD:
    def __init__(self):
        self.uploaded = 0


UPLOAD_ = UPLOAD()


async def doglst_of_files(path):
    files = []
    for dirname, dirnames, filenames in walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(osp.join(dirname, filename))
    return files


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    cmd = [
        "ffmpeg",
        "-i",
        file,
        "-ss",
        str(int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)),
        # '-filter:v', 'scale={}:-1'.format(width),
        "-vframes",
        "1",
        output,
    ]
    p = Popen(
        cmd,
        stdout=PIPE,
        stderr=DEVNULL,
    )
    p.communicate()
    if not p.returncode and osp.lexists(file):
        return output


def sortthings(contents, path):
    dogsort = []
    contents.sort()
    for file in contents:
        dogpath = osp.join(path, file)
        if osp.isfile(dogpath):
            dogsort.append(file)
    for file in contents:
        dogpath = osp.join(path, file)
        if osp.isdir(dogpath):
            dogsort.append(file)
    return dogsort


async def _get_file_name(path: Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


async def upload(path, event, udir_event, dogflag=None):  # sourcery no-metrics
    dogflag = dogflag or False
    reply_to_id = await reply_id(event)
    if osp.isdir(path):
        await event.client.send_message(
            event.chat_id,
            f"**Folder: **`{path}`",
        )
        Files = listdir(path)
        Files = sortthings(Files, path)
        for file in Files:
            dogpath = osp.join(path, file)
            await upload(Path(dogpath), event, udir_event)
    elif osp.isfile(path):
        fname = osp.basename(path)
        c_time = time()
        thumb = thumb_image_path if osp.exists(thumb_image_path) else None
        f = path.absolute()
        attributes, mime_type = get_attributes(str(f))
        ul = iopen(f, "rb")
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to upload", file_name=fname)
            ),
        )
        ul.close()
        media = InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=dogflag,
            thumb=await event.client.upload_file(thumb) if thumb else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"**File Name: **`{fname}`",
            reply_to=reply_to_id,
        )

        UPLOAD_.uploaded += 1


@doge.bot_cmd(
    pattern="upload( -f)? ([\s\S]*)",
    command=("upload", plugin_category),
    info={
        "header": "To upload files from server to telegram",
        "description": "To upload files which are downloaded in your bot.",
        "flags": {"f": "Use this to make upload files as documents."},
        "examples": [
            "{tr}upload <file/folder path>",
            "{tr}upload -f <file/folder path>",
        ],
    },
)
async def uploadir(event):
    "To upload files to telegram."
    input_str = event.pattern_match.group(2)
    path = Path(input_str)
    start = datetime.now()
    flag = event.pattern_match.group(1)
    flag = bool(flag)
    if not osp.exists(path):
        return await eor(
            event,
            f"`there is no such directory/file with the name {path} to upload`",
        )
    udir_event = await eor(event, "Uploading....")
    if osp.isdir(path):
        await eor(udir_event, f"`Gathering file details in directory {path}`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, dogflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edl(
            udir_event,
            f"`Uploaded {UPLOAD_.uploaded} files successfully in {ms} seconds. `",
        )
    else:
        await eor(udir_event, "`Uploading file .....`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, dogflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edl(udir_event, f"`Uploaded file {path} successfully in {ms} seconds. `")
