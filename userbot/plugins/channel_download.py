# Credits: @Zero_cool7870
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import makedirs, path
from subprocess import PIPE, Popen, check_output

from . import TMP_DOWNLOAD_DIRECTORY, doge, eor, media_type

plugin_category = "tool"


@doge.bot_cmd(
    pattern="getc(?:\s|$)([\s\S]*)",
    command=("getc", plugin_category),
    info={
        "h": "Kanal medya dosyalarını indirir",
        "d": "Komutu kontrol etmek için kullanıcı adını ve en son mesajların sayısını iletin. Böylece bot, medya dosyalarını bu son mesaj sayısından sunucuya indirecektir. ",
        "u": "{tr}getc sayı channel_username",
        "e": "{tr}getc 10 @DogeUserBot",
    },
)
async def get_media(event):
    dogty = event.pattern_match.group(1)
    limit = int(dogty.split(" ")[0])
    channel_username = str(dogty.split(" ")[1])
    tempdir = path.join(TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        makedirs(tempdir)
    except BaseException:
        pass
    event = await eor(event, "`Bu kanaldan medya indirir.`")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(f"Bu kanaldan medya yükleniyor.\n**İndirildi:** `{i}`")
    ps = Popen(("ls", tempdir), stdout=PIPE)
    output = check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", " ")
    output = output.replace("\\n'", " ")
    await event.edit(
        f"{channel_username} adlı kullanıcıdan geçici dizine {output} adet medya başarıyla indirildi!"
    )


@doge.bot_cmd(
    pattern="geta(?:\s|$)([\s\S]*)",
    command=("geta", plugin_category),
    info={
        "h": "Kanalın tüm medya dosyalarını indirir",
        "d": "komuta kullanıcı adını iletin, böylece bot tüm medya dosyalarını bu en son mesaj sayısından sunucuya indirir ",
        "note": "API limitlerini önlemek için bu işlem için 3000 mesaj sınırı vardır. bu, tüm medya dosyalarını en son 3000 mesajdan indirecektir.",
        "u": "{tr}geta channel_username",
        "e": "{tr}geta @DogeUserBot",
    },
)
async def get_media(event):
    channel_username = event.pattern_match.group(1)
    tempdir = path.join(TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        makedirs(tempdir)
    except BaseException:
        pass
    event = await eor(event, "`Tüm medyaları bu kanaldan indirir.`")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(f"Bu kanaldan medya yükleniyor.\n **İndirildi:** `{i}`")
    ps = Popen(("ls", tempdir), stdout=PIPE)
    output = check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit(
        f"{channel_username} kaynağından geçici dizine {output} adet medya başarıyla indirildi!"
    )
