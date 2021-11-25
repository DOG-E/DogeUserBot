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
    BOT_USERNAME,
    StartTime,
    check_data_base_heal_th,
    doge,
    dogealive,
    dogeversion,
    eor,
    get_readable_time,
    gvar,
    lan,
    mention,
    reply_id,
    tr,
)

plugin_category = "bot"


@doge.bot_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": lan("alive8"),
        "options": lan("alive9").format(tr),
        "usage": [
            "{tr}alive",
        ],
    },
)
async def thisalive(event):
    lan("alive10")
    start = datetime.now()
    await event.edit("ㅤ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvar("ALIVE_TEXT") or lan("dogeemoji")
    try:
        fixialive = "ㅤ\n"
        doge_caption = gvar("ALIVE") or lan("ialive")
        caption = fixialive + doge_caption.format(
            msg=ALIVE_TEXT,
            mention=mention,
            uptime=uptime,
            tv=__version__,
            dv=dogeversion,
            pv=python_version(),
            db=check_sgnirts,
            ping=ms,
        )
        results = await event.client.inline_query(BOT_USERNAME, caption)
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()

    except Exception:
        DOG_IMG = (
            gvar("ALIVE_PIC") or "https://telegra.ph/file/4d498bf8dfc83a93f418b.png"
        )
        doge_caption = gvar("ALIVE") or lan("aalive")
        caption = doge_caption.format(
            msg=ALIVE_TEXT,
            mention=mention,
            dv=dogeversion,
            uptime=uptime,
            db=check_sgnirts,
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
                    f"**{lan('mediavalueerror')}**\n{lan('alive11')}`{tr}setdog`\n\n{lan('alive12')} `{PIC}`",
                )
        else:
            await eor(event, caption)


@doge.tgbot.on(CallbackQuery(data=compile(b"infos")))
async def on_plug_in_callback_query_handler(event):
    statstext = await dogealive()
    await event.answer(statstext, cache_time=0, alert=True)
