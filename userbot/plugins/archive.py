# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
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

from . import TMP_DOWNLOAD_DIRECTORY, doge, edl, eor, progress

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
        "h": "Dosya veya klasörü zip olarak sıkıştırır.",
        "d": "Verilen dosya yolu veya klasör yolu için bir zip dosyası oluşturur.",
        "u": [
            "{tr}zip <dosya/klasör yolu>",
        ],
        "e": ["{tr}zip downloads ", "{tr}zip sample_config.py"],
    },
)
async def zip_file(event):
    "Dosya veya klasörü zip olarak sıkıştırır."
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(event, "`Bir şeyi zip olarak sıkıştırmam için dosya yolu sağlayın.`")
    start = datetime.now()
    if not osp.exists(Path(input_str)):
        return await eor(
            event,
            f"{input_str} adında böyle bir dizin veya dosya yok tekrar kontrol edin!",
        )
    if osp.isfile(Path(input_str)):
        return await edl(event, "`Dosya sıkıştırma henüz uygulanmadı.`")
    mone = await eor(event, "`Zip sıkıştırma işlemi devam ediyor...`")
    filePaths = zipdir(input_str)
    filepath = osp.join(TMP_DOWNLOAD_DIRECTORY, osp.basename(Path(input_str)))
    destination = f"{filepath}.zip"
    zip_file = ZipFile(destination, "w")
    with zip_file:
        for file in filePaths:
            zip_file.write(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"{input_str} ögesini {destination} içine {ms} saniyede sıkıştırdım."
    )


@doge.bot_cmd(
    pattern="tar(?:\s|$)([\s\S]*)",
    command=("tar", plugin_category),
    info={
        "h": "Dosya veya klasörü tar olarak sıkıştırır.",
        "d": "Verilen dosya yolu veya klasör yolu için bir tar dosyası oluşturur.",
        "u": [
            "{tr}tar <dosya/klasör yolu>",
        ],
        "e": ["{tr}tar downloads ", "{tr}tar sample_config.py"],
    },
)
async def tar_file(event):
    "Dosya veya klasörü tar olarak sıkıştırır."
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(event, "`Bir şeyi tar olarak sıkıştırmam için dosya yolu sağlayın.`")
    if not osp.exists(Path(input_str)):
        return await eor(
            event,
            f"{input_str} adında böyle bir dizin veya dosya yok tekrar kontrol edin.",
        )
    if osp.isfile(Path(input_str)):
        return await edl(event, "`Dosya sıkıştırma henüz uygulanmadı.`")
    mone = await eor(event, "`Tar sıkıştırma işlemi devam ediyor...`")
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
    await mone.edit(
        f"{input_str} ögesini {destination} içine {ms} saniyede sıkıştırdım."
    )


@doge.bot_cmd(
    pattern="unzip(?:\s|$)([\s\S]*)",
    command=("unzip", plugin_category),
    info={
        "h": "Zip dosyası açar.",
        "d": "Bir zip dosyasını açmak için bir zip dosyasına yanıt verin veya zip dosyası yolu sağlayın.",
        "u": [
            "{tr}unzip <yanıt/dosya yolu>",
        ],
    },
)
async def zip_file(event):  # sourcery no-metrics
    "Zip dosyası açar."
    input_str = event.pattern_match.group(1)
    if input_str:
        path = Path(input_str)
        if osp.exists(path):
            start = datetime.now()
            if not is_zipfile(path):
                return await edl(
                    event, f"`Verilen yol {path}, paketten çıkarılacak zip dosyası değil.`"
                )

            mone = await eor(event, "`Çıkartıyorum...`")
            destination = osp.join(
                TMP_DOWNLOAD_DIRECTORY,
                osp.splitext(osp.basename(path))[0],
            )
            with ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"{destination} yoluna çıkarttım! {ms} saniye sürdü."
            )
        else:
            await edl(event, f"`{input_str} yolunu bulamıyorum.`")
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        ext = get_extension(reply.document)
        if ext != ".zip":
            return await edl(
                event,
                "`Yanıtlanan dosya, bir zip dosyası değil, yanıtlanan mesajı tekrar kontrol edin.`",
            )
        mone = await eor(event, "`Çıkartılıyor...`")
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
                    progress(d, t, mone, c_time, "İndiriliyor")
                ),
            )
            dl.close()
        except Exception as e:
            return await edl(mone, f"**Hata:**\n`{e}`")

        await mone.edit("`İndirme bitti, dosyayı açıyorum...`")
        destination = osp.join(
            TMP_DOWNLOAD_DIRECTORY,
            osp.splitext(osp.basename(filename))[0],
        )
        with ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(destination)
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
           f"{destination} yoluna çıkarttım. {ms} saniye sürdü."
        )
        remove(filename)
    else:
        await edl(
            event,
            "`Zip dosyasına yanıt verin veya komutla birlikte zip dosyasının yolunu sağlayın.`",
        )


@doge.bot_cmd(
    pattern="untar(?:\s|$)([\s\S]*)",
    command=("untar", plugin_category),
    info={
        "h": "Tar dosyası açar.",
        "d": "Bir tar dosyasını açmak için bir tar dosyasına yanıt verin veya tar dosyası yolunu sağlayın.",
        "u": [
            "{tr}untar <yanıt/dosya yolu>",
        ],
    },
)
async def untar_file(event):  # sourcery no-metrics
    "Tar dosyası açar."
    input_str = event.pattern_match.group(1)
    if input_str:
        path = Path(input_str)
        if osp.exists(path):
            start = datetime.now()
            if not is_tarfile(path):
                return await edl(
                    event, f"`Verilen yol {path}, paketinden çıkarılacak tar dosyası değil`"
                )

            mone = await eor(event, "`Çıkartıyorum...`")
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
            await mone.edit(
                f"`{input_str}` ögesini `{destination}` yoluna çıkarttım! {ms} saniye sürdü."
            )
        else:
            await edl(event, f"{input_str} yolunu bulamıyorum.`")
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        mone = await eor(event, "`Çıkartıyorum...`")
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
                    progress(d, t, mone, c_time, "İndiriliyor")
                ),
            )
            dl.close()
        except Exception as e:
            return await edl(mone, f"**Hata:**\n`{e}`")

        if not is_tarfile(filename):
            return await edl(
                mone, "`Yanıtlanan dosya, bir tar dosyası değil, yanıtlanan mesajı tekrar kontrol edin.`"
            )

        await mone.edit("`İndirme bitti, dosyayı açıyorum...`")
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
        await mone.edit(
            f"`{destination}` yoluna çıkarttım. {ms} saniye sürdü."
        )
        remove(filename)
    else:
        await edl(
            event,
            "`Tar dosyasına yanıt verin veya komutla birlikte tar dosyasının yolunu sağlayın.`",
        )
