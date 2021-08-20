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
    M_STERS,
    Config,
    StartTime,
    check_data_base_heal_th,
    doge,
    dogealive,
    dogeversion,
    edl,
    eor,
    get_readable_time,
    get_user_from_event,
    gvarstatus,
    mention,
    reply_id,
)

plugin_category = "bot"

temp = "{msg}\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅᴏɢᴇ ᴏғ - {mention}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅᴏɢᴇ ᴠᴇʀꜱɪᴏɴ - {dv}\n\
┃ ᴀʟɪᴠᴇ ꜱɪɴᴄᴇ - {uptime}\n\
┃ ꜱᴛᴀᴛᴜꜱ - {db}\n\
┃ ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ - {tv}\n\
┃ ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ - {pv}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴘɪɴɢ - {ping} ms\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
        ↠━━━━━ღ◆ღ━━━━━↞"


@doge.bot_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by {tr}tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def thisalive(event):
    "A kind of showing bot details"
    start = datetime.now()
    await event.edit("ㅤ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "🐶 Dᴏɢᴇ UsᴇʀBᴏᴛ 🐾"
    DOG_IMG = (
        gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg"
    )
    doge_caption = gvarstatus("ALIVE") or temp
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
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await eor(event, caption)


@doge.bot_cmd(incoming=True, from_users=M_STERS, pattern="dlive$", disable_errors=True)
async def dlive(event):
    user = await get_user_from_event(event)
    if user.id not in M_STERS:
        return await edl(event, "**Only Doge admins can use, dude!**")
    reply_to_id = await reply_id(event)
    start = datetime.now()
    ppingx = await event.reply("ㅤ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = await get_readable_time((time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "🐶 Dᴏɢᴇ UsᴇʀBᴏᴛ 🐾"
    DOG_IMG = (
        gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/dd72e42027e6e7de9c0c9.jpg"
    )
    doge_caption = gvarstatus("ALIVE") or temp
    caption = doge_caption.format(
        msg=ALIVE_TEXT,
        mention=mention,
        uptime=uptime,
        tv=__version__,
        dv=dogeversion,
        pv=python_version(),
        db=check_sgnirts,
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
            await event.reply(caption)
    else:
        await event.reply(caption)
    try:
        ppingx.delete()
    except:
        pass


@doge.bot_cmd(
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
async def thisialive(event):
    "A kind of showing bot details by your inline bot"
    start = datetime.now()
    await eor(event, "ㅤ")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "🐶 Dᴏɢᴇ UsᴇʀBᴏᴛ 🐾"
    doge_caption = gvarstatus("ALIVE") or temp
    caption = doge_caption.format(
        msg=ALIVE_TEXT,
        mention=mention,
        uptime=uptime,
        tv=__version__,
        dv=dogeversion,
        pv=python_version(),
        db=check_sgnirts,
        ping=ms,
    )
    results = await event.client.inline_query(Config.BOT_USERNAME, caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@doge.tgbot.on(CallbackQuery(data=compile(b"infos")))
async def on_plug_in_callback_query_handler(event):
    statstext = await dogealive()
    await event.answer(statstext, cache_time=0, alert=True)
