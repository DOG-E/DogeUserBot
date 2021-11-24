# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import get_event_loop
from datetime import datetime
from io import FileIO
from os import mkdir
from os import path as osp
from os import remove, walk
from pathlib import Path
from tarfile import is_tarfile
from tarfile import open as tar_open
from time import time
from zipfile import ZipFile, is_zipfile

from telethon.tl.types import DocumentAttributeFilename
from telethon.utils import get_extension

from . import TMP_DOWNLOAD_DIRECTORY, doge, edl, eor
from . import lan as l
from . import progress, tr

plugin_category = "tool"

thumb_image_path = osp.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


def zipdir(dirName):
    filePaths = []
    for root, directories, files in walk(dirName):
        for filename in files:
            filePath = osp.join(root, filename)
            filePaths.append(filePath)
    return filePaths


@doge.bot_cmd(
    pattern="zip(?:\s|$)([\s\S]*)",
    command=("zip", plugin_category),
    info={
        "header": l("zip1"),
        "description": l("zip2"),
        "usage": [
            f"{tr}zip {l('zip3')}",
        ],
        "examples": [f"{tr}zip downloads", "{tr}zip sample_config.py"],
    },
)
async def zip_file(event):
    l("zip5")
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(event, l("zip6"))
    start = datetime.now()
    if not osp.exists(Path(input_str)):
        return await eor(
            event,
            l("zip7").format(input_str),
        )
    if osp.isfile(Path(input_str)):
        return await edl(event, l("zip8"))
    mone = await eor(event, l("zip9"))
    filePaths = zipdir(input_str)
    filepath = osp.join(TMP_DOWNLOAD_DIRECTORY, osp.basename(Path(input_str)))
    zip_file = ZipFile(filepath + ".zip", "w")
    with zip_file:
        for file in filePaths:
            zip_file.write(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(l("zip10").format(input_str, filepath + ".zip", ms))


@doge.bot_cmd(
    pattern="tar(?:\s|$)([\s\S]*)",
    command=("tar", plugin_category),
    info={
        "header": l("tar1"),
        "description": l("tar2"),
        "usage": [
            f"{tr}tar {l('tar3')}",
        ],
        "examples": ["{tr}tar downloads", "{tr}tar sample_config.py"],
    },
)
async def tar_file(event):
    "To create tar file"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(event, l("tar4"))
    if not osp.exists(Path(input_str)):
        return await eor(
            event,
            l("tar5").format(input_str),
        )
    if osp.isfile(Path(input_str)):
        return await edl(event, l("tar6"))
    mone = await eor(event, l("tar7"))
    start = datetime.now()
    filePaths = zipdir(input_str)
    filepath = osp.join(TMP_DOWNLOAD_DIRECTORY, osp.basename(Path(input_str)))
    destination = f"{filepath}.tar.gz"
    zip_file = tar_open(destination, "w:gz")
    with zip_file:
        for file in filePaths:
            zip_file.add(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(l("tar8").format(input_str, destination, ms))


@doge.bot_cmd(
    pattern="unzip(?:\s|$)([\s\S]*)",
    command=("unzip", plugin_category),
    info={
        "header": l("unzip1"),
        "description": l("unzip2"),
        "usage": [
            f"{tr}unzip {l('unzip3')}",
        ],
    },
)
async def zip_file(event):  # sourcery no-metrics
    l("unzip4")
    input_str = event.pattern_match.group(1)
    if input_str:
        path = Path(input_str)
        if osp.exists(path):
            start = datetime.now()
            if not is_zipfile(path):
                return await edl(event, l("unzip5").format(path))

            mone = await eor(event, l("unzip6"))
            destination = osp.join(
                TMP_DOWNLOAD_DIRECTORY,
                osp.splitext(osp.basename(path))[0],
            )
            with ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(l("unzip7").format(destination, ms))
        else:
            await edl(event, l("unzip8").format(input_str))
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        ext = get_extension(reply.document)
        if ext != ".zip":
            return await edl(
                event,
                l("unzip9"),
            )
        mone = await eor(event, l("unzip6"))
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, DocumentAttributeFilename):
                filename = attr.file_name
        filename = osp.join(TMP_DOWNLOAD_DIRECTORY, filename)
        c_time = time()
        try:
            dl = FileIO(filename, "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, mone, c_time, l("unzip10"))
                ),
            )
            dl.close()
        except Exception as e:
            return await edl(mone, f"{l('errr')}\n__{e}__")

        await mone.edit(l("unzip11"))
        destination = osp.join(
            TMP_DOWNLOAD_DIRECTORY,
            osp.splitext(osp.basename(filename))[0],
        )
        with ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(destination)
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(l("unzip12").format(destination, ms))
        remove(filename)
    else:
        await edl(
            event,
            l("unzip13"),
        )


@doge.bot_cmd(
    pattern="untar(?:\s|$)([\s\S]*)",
    command=("untar", plugin_category),
    info={
        "header": l("untar1"),
        "description": l("untar2"),
        "usage": [
            f"{tr}untar {l('untar3')}",
        ],
    },
)
async def untar_file(event):  # sourcery no-metrics
    l("untar4")
    input_str = event.pattern_match.group(1)
    if input_str:
        path = Path(input_str)
        if osp.exists(path):
            start = datetime.now()
            if not is_tarfile(path):
                return await edl(event, l("untar6").format(path))

            mone = await eor(event, l("untar6"))
            destination = osp.join(
                TMP_DOWNLOAD_DIRECTORY, (osp.basename(path).split("."))[0]
            )
            if not osp.exists(destination):
                mkdir(destination)
            file = tar_open(path)
            # extracting file
            file.extractall(destination)
            file.close()
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(l("untar7").format(ms, input_str, destination))
        else:
            await edl(event, l("untar8").format(input_str))
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        mone = await eor(event, l("untar6"))
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, DocumentAttributeFilename):
                filename = attr.file_name
        filename = osp.join(TMP_DOWNLOAD_DIRECTORY, filename)
        c_time = time()
        try:
            dl = FileIO(filename, "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, mone, c_time, l("unzip10"))
                ),
            )
            dl.close()
        except Exception as e:
            return await edl(mone, f"{l('errr')}\n__{e}__")

        if not is_tarfile(filename):
            return await edl(mone, l("untar9"))

        await mone.edit(l("untar10"))
        destination = osp.join(
            TMP_DOWNLOAD_DIRECTORY, (osp.basename(filename).split("."))[0]
        )

        if not osp.exists(destination):
            mkdir(destination)
        file = tar_open(filename)
        # extracting file
        file.extractall(destination)
        file.close()
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(l("untar11").format(ms, destination))
        remove(filename)
    else:
        await edl(
            event,
            l("untar12"),
        )
