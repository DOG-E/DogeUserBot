# Credits: @sandy1709
# Copyright (C) 2020 Alfiananda P.A
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import mkdir, path, remove

from . import _dogeutils, doge, edl, eor, make_gif, reply_id

plugin_category = "misc"


@doge.bot_cmd(
    pattern="collage(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "h": "Video / GIF'den çıkarılan fotoğraflardan kolaj oluşturur.",
        "d": "Video / GIF'den çıkarılan görüntülerin ızgara görüntüsünü gösterir.Kılavuz boyutunu, komut ile 1 ila 9 arasında bir rakam yazarak özelleştirebilirsiniz. Varsayılan olarak 3'tür'.",
        "u": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "Video / GIF'den çıkarılan fotoğraflardan kolaj oluşturur."
    doginput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    dogid = await reply_id(event)
    event = await eor(event, "```Bu birkaç dakika sürebilir..... 😁```")
    if not (reply and (reply.media)):
        await event.edit("`Medya bulunamadı...`")
        return
    if not path.isdir("./temp/"):
        mkdir("./temp/")
    dogsticker = await reply.download_media(file="./temp/")
    if not dogsticker.endswith((".mp4", ".mkv", ".tgs")):
        remove(dogsticker)
        await event.edit("`Medya formatı desteklenmiyor...`")
        return
    if doginput:
        if not doginput.isdigit():
            remove(dogsticker)
            await event.edit("`Girdi geçersiz, tekrar kontrol edin!`")
            return
        doginput = int(doginput)
        if not 0 < doginput < 10:
            remove(dogsticker)
            await event.edit(
                "`Neden çok görüntü görmek istiyorsunuz ki?, 1 ile 9 arasında boyut kullanın.`"
            )
            return
    else:
        doginput = 3
    if dogsticker.endswith(".tgs"):
        hmm = await make_gif(event, dogsticker)
        if hmm.endswith(("@tgstogifbot")):
            remove(dogsticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = dogsticker
    endfile = "./temp/collage.png"
    dogecmd = f"vcsi -g {doginput}x{doginput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _dogeutils.runcmd(dogecmd))[:2]
    if not path.exists(endfile):
        for files in (dogsticker, collagefile):
            if files and path.exists(files):
                remove(files)
        return await edl(
            event,
            "`Medya desteklenmiyor veya daha küçük ızgara boyutuyla deneyin.`",
            5,
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=dogid,
    )
    await event.delete()
    for files in (dogsticker, collagefile, endfile):
        if files and path.exists(files):
            remove(files)
