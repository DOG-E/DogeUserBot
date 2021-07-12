import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from ..Config import Config
from ..core.managers import eor
from ..helpers.functions import check_data_base_heal_th, dogalive, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import StartTime, doge, dogeversion, mention

plugin_category = "utils"


@doge.bot_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    start = datetime.now()
    await eor(event, "Checking...")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "✮ MY BOT IS RUNNING SUCCESSFULLY ✮"
    doge_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = doge_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        Televar=version.__version__,
        dogever=dogeversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    DOG_IMG = gvarstatus("ALIVE_PIC")
    if DOG_IMG:
        DOG = [x for x in DOG_IMG.split()]
        PIC = random.choice(DOG)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await eor(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await eor(event, caption)


temp = "**{ALIVE_TEXT}**\n\n\
**{EMOJI} Master : {mention}**\n\
**{EMOJI} Uptime :** `{uptime}`\n\
**{EMOJI} Telethon version :** `{Televar}`\n\
**{EMOJI} DogeUserBot Version :** `{dogever}`\n\
**{EMOJI} Python Version :** `{pyver}`\n\
**{EMOJI} Database :** `{dbhealth}`\n"


@doge.bot_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**Dogeuserbot is Up and Running**"
    doge_caption = f"{ALIVE_TEXT}\n"
    doge_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    doge_caption += f"**{EMOJI} DogeUserBot Version :** `{dogeversion}`\n"
    doge_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    doge_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, doge_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@doge.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await dogalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
