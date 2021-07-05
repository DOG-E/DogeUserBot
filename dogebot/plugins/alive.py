# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import random
import re
import time
from datetime import datetime
from platform import python_version as pyver

from telethon import __version__ as telever
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from dogebot import StartTime, doge

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import check_data_base_heal_th, dogealive, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import dogeversion as dogever
from . import lang, mention

plugin_category = "utils"


@doge.doge_cmd(
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
    await edit_or_reply(event, f"**{lang('checking')}...**")
    end = datetime.now()
    ping = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    dbhealth = check_sgnirts
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or lang("alive1")
    doge_caption = gvarstatus("ALIVE_TEMPLATE") or lang("alive1temp")
    caption = doge_caption.format(
        ALIVE_TEXT,
        mention,
        dogever,
        uptime,
        dbhealth,
        telever,
        pyver(),
        ping,
    )
    DOG_IMG = (
        gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg"
    )
    if DOG_IMG:
        DOG = [x for x in DOG_IMG.split()]
        PIC = random.choice(DOG)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(event, caption)


temp = "**{ALIVE_TEXT}**\n\n\
**{EMOJI} Master : {mention}**\n\
**{EMOJI} Uptime :** `{uptime}`\n\
**{EMOJI} Telethon version :** `{telever}`\n\
**{EMOJI} Doge UserBot version :** `{dogever}`\n\
**{EMOJI} Python Version :** `{pyver}`\n\
**{EMOJI} {lang('database')} :** `{dbhealth}`\n"


@doge.doge_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}ialive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    doge_caption = f"**Doge UserBot is Up and Running**\n"
    doge_caption += f"**{EMOJI} Telethon version :** `{telever}\n`"
    doge_caption += f"**{EMOJI} Doge UserBot Version :** `{dogever}`\n"
    doge_caption += f"**{EMOJI} Python Version :** `{pyver()}\n`"
    doge_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, doge_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@doge.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await dogealive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
