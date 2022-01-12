# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from platform import python_version
from random import choice
from re import compile
from time import time

from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery
from telethon.version import __version__

from . import (
    ALIVETEMP,
    BOT_USERNAME,
    IALIVETEMP,
    StartTime,
    doge,
    dogeversion,
    eor,
    get_readable_time,
    gvar,
    mention,
    reply_id,
    tr,
)

plugin_category = "bot"


@doge.bot_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "h": "Botun durumunu kontrol edin",
        "o": "Medyayı özelleştirmek için herhangi bi medyaya yanıtlayarak {tr}sdog ALIVE_PIC yazın.",
        "u": [
            "{tr}alive",
        ],
    },
)
async def thisalive(event):
    "Botun durumunu kontrol edin"
    start = datetime.now()
    await event.edit("ㅤ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time() - StartTime))
    ALIVE_TEXT = gvar("ALIVE_TEXT") or "🐶 Doɢᴇ UsᴇʀBoᴛ 🐾"
    try:
        fixialive = "ㅤ\n"
        doge_caption = gvar("ALIVE") or IALIVETEMP
        caption = fixialive + doge_caption.format(
            msg=ALIVE_TEXT,
            mention=mention,
            up=uptime,
            tv=__version__,
            dv=dogeversion,
            pv=python_version(),
            ping=ms,
        )
        results = await event.client.inline_query(BOT_USERNAME, caption)
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()

    except Exception:
        DOG_IMG = (
            gvar("ALIVE_PIC") or "https://telegra.ph/file/4d498bf8dfc83a93f418b.png"
        )
        doge_caption = gvar("ALIVE") or ALIVETEMP
        caption = doge_caption.format(
            msg=ALIVE_TEXT,
            mention=mention,
            dv=dogeversion,
            up=uptime,
            tv=__version__,
            pv=python_version(),
            ping=ms,
        )
        if DOG_IMG:
            DOG = [x for x in DOG_IMG.split()]
            PIC = choice(DOG)
            try:
                await event.client.send_file(
                    event.chat_id, PIC, caption=caption, reply_to=reply_to_id
                )
                await event.delete()
            except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
                return await eor(
                    event,
                    caption
                    + f"\n\n\n[Medyayı]({PIC}) bulamadım.\nMedyayı ayarlamak için bir medyayı yanıtlayarak {tr}sdog ALIVE_PIC yazın.",
                )
        else:
            await eor(event, caption)


@doge.bot.on(CallbackQuery(data=compile(b"infos")))
async def on_plug_in_callback_query_handler(event):
    statstext = f"🐶 Doɢᴇ UsᴇʀBoᴛ\
            \n🐾 Bɪʟɢɪ\n\
            \n🔹 Çalıştığını kontrol etmek için:\
            \n{tr}alive\n\
            \n🔹 Yardım Menüsü için:\
            \n{tr}doge"

    await event.answer(statstext, cache_time=0, alert=True)
