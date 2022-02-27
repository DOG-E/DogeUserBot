# Modded: code-rgb
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import get_event_loop, sleep
from glob import glob
from io import open as iopen
from os import path
from pathlib import Path
from re import compile
from time import time

from telethon import Button
from telethon.errors import BotResponseTimeoutError
from telethon.events import CallbackQuery
from telethon.tl.types import InputMediaUploadedDocument
from telethon.utils import get_attributes
from ujson import load
from wget import download

from ..core.pool import run_in_thread
from ..helpers.functions.utube import _mp3Dl, _tubeDl
from . import (
    BOTLOG_CHATID,
    TEMP_DIR,
    check_owner,
    doge,
    download_button,
    edl,
    eor,
    get_choice_by_id,
    get_ytthumb,
    gvar,
    logging,
    post_to_telegraph,
    progress,
    reply_id,
    yt_search_btns,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./userbot/cache/ytsearch.json"


@doge.bot_cmd(
    pattern="yt(?:\s|$)([\s\S]*)",
    command=("yt", plugin_category),
    info={
        "h": "Satır içi butonlarla YouTube'dan videolar indirin.",
        "d": "YouTube videolarını satır içi butonlara göre aramak ve indirmek için.",
        "u": "{tr}yt yazı ya da yanıtlanmış ya da yazılmış link",
    },
)
async def yt_inline(event):
    "YouTube videolarını satır içi butonlara göre aramak ve indirmek için."
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    if not input_url:
        return await edl(
            event, "**📺 Geçerli bir YouTube URL'sine girin veya cevap verin!**"
        )

    dogevent = await eor(
        event, "**🔎 Şunun için YouTube'da arama yapıyorm:** `{}`...".format(input_url)
    )
    flag = True
    cout = 0
    results = None
    while flag:
        try:
            results = await event.client.inline_query(
                gvar("BOT_USERNAME"), f"yt {input_url}"
            )
            break
        except BotResponseTimeoutError:
            await sleep(2)
        cout += 1
        if cout > 5:
            break
    if results:
        await dogevent.delete()
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    else:
        await dogevent.edit("**🚨 Üzgünüm! Hiçbir sonuç bulamadım.**")


@doge.bot.on(
    CallbackQuery(data=compile(b"^ytdl_download_(.*)_([\d]+|mkv|mp4|mp3)(?:_(a|v))?"))
)
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):  # sourcery no-metrics
    yt_code = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    choice_id = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    downtype = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    if str(choice_id).isdigit():
        choice_id = int(choice_id)
        if choice_id == 0:
            await c_q.answer("**⏳ İşleniyor...**", alert=False)
            await c_q.edit(buttons=(await download_button(yt_code)))
            return
    startTime = time()
    choice_str, disp_str = get_choice_by_id(choice_id, downtype)
    media_type = "Video" if downtype == "v" else "Audio"
    callback_continue = "📥 Lütfen bekleyin, {} indiriyorum...".format(media_type)
    callback_continue += f"\n\n🆔 Format Kodu: {disp_str}"
    await c_q.answer(callback_continue, alert=True)
    upload_msg = await c_q.client.send_message(BOTLOG_CHATID, "**📤 Yükleniyor...**")
    yt_url = BASE_YT_URL + yt_code
    await c_q.edit(
        f"<b>⬇️ İndiriliyor {media_type}...</b>\n\n<a href={yt_url}> <b>🔗 Bağlantı</b></a>\n🆔 <b>Format Kodu:</b> {disp_str}",
        parse_mode="html",
    )
    if downtype == "v":
        retcode = await _tubeDl(url=yt_url, starttime=startTime, uid=choice_str)
    else:
        retcode = await _mp3Dl(url=yt_url, starttime=startTime, uid=choice_str)
    if retcode != 0:
        return await upload_msg.edit(str(retcode))

    _fpath = ""
    thumb_pic = None
    for _path in glob(path.join(TEMP_DIR, str(startTime), "*")):
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
        else:
            _fpath = _path
    if not _fpath:
        return await edl(upload_msg, "**🚨 Üzgünüm! Hiçbir sonuç bulamadım.**")

    if not thumb_pic:
        thumb_pic = str(await run_in_thread(download)(await get_ytthumb(yt_code)))
    attributes, mime_type = get_attributes(str(_fpath))
    ul = iopen(Path(_fpath), "rb")
    uploaded = await c_q.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: get_event_loop().create_task(
            progress(
                d,
                t,
                c_q,
                startTime,
                "**📤 Yüklemeyi Deniyorum...**",
                file_name=path.basename(Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await c_q.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    uploaded_media = await c_q.client.send_file(
        BOTLOG_CHATID,
        file=media,
        caption=f"<b>ℹ️ Dosya Adı:</b> <code>{path.basename(Path(_fpath))}</code>",
        parse_mode="html",
    )
    await upload_msg.delete()
    await c_q.edit(
        text=f"🎞 <a href={yt_url}><b>{path.basename(Path(_fpath))}</b></a>",
        file=uploaded_media.media,
        parse_mode="html",
    )


@doge.bot.on(
    CallbackQuery(data=compile(b"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)"))
)
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
    choosen_btn = (
        str(c_q.pattern_match.group(1).decode("UTF-8"))
        if c_q.pattern_match.group(1) is not None
        else None
    )
    data_key = (
        str(c_q.pattern_match.group(2).decode("UTF-8"))
        if c_q.pattern_match.group(2) is not None
        else None
    )
    page = (
        str(c_q.pattern_match.group(3).decode("UTF-8"))
        if c_q.pattern_match.group(3) is not None
        else None
    )
    if not path.exists(PATH):
        return await c_q.answer(
            "🚨 Arama verileri artık mevcut değil.\
            \n\
            \n🔁 Lütfen tekrar arama yapın.",
            alert=True,
        )

    with open(PATH) as f:
        view_data = load(f)
    search_data = view_data.get(data_key)
    total = len(search_data) if search_data is not None else 0
    if total == 0:
        return await c_q.answer(
            "🚨 Botun bu konuda bilgileri kaybetti.\
            \n\
            \n🔁 Lütfen tekrar arayın.",
            alert=True,
        )

    if choosen_btn == "back":
        index = int(page) - 1
        del_back = index == 1
        await c_q.answer()
        back_vid = search_data.get(str(index))
        await c_q.edit(
            text=back_vid.get("message"),
            file=await get_ytthumb(back_vid.get("video_id")),
            buttons=yt_search_btns(
                del_back=del_back,
                data_key=data_key,
                page=index,
                vid=back_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "next":
        index = int(page) + 1
        if index > total:
            return await c_q.answer("🔔 Hepsi bu kadar!", alert=True)

        await c_q.answer()
        front_vid = search_data.get(str(index))
        await c_q.edit(
            text=front_vid.get("message"),
            file=await get_ytthumb(front_vid.get("video_id")),
            buttons=yt_search_btns(
                data_key=data_key,
                page=index,
                vid=front_vid.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
    elif choosen_btn == "listall":
        await c_q.answer("➡️ Görünüm olarak şu değiştirildi: 📜 Liste", alert=False)
        list_res = "".join(
            search_data.get(vid_s).get("list_view") for vid_s in search_data
        )

        telegraph = await post_to_telegraph(
            "ℹ️ Verilen sorgu:{} için  YouTube video sonuçları gösteriliyor...".format(
                total
            ),
            list_res,
        )
        await c_q.edit(
            file=await get_ytthumb(search_data.get("1").get("video_id")),
            buttons=[
                Button.url("↗️ Açᴍᴀᴋ Içɪɴ Tıᴋʟᴀʏıɴ", url=telegraph),
                Button.inline("📊 Dᴇᴛᴀʏʟᴀʀı Göʀ", data=f"ytdl_detail_{data_key}_{page}"),
            ],
        )

    else:  # Detailed
        index = 1
        await c_q.answer("➡️ Görünüm şu olarak değiştirildi: 📊 Detaylı", alert=False)
        first = search_data.get(str(index))
        await c_q.edit(
            text=first.get("message"),
            file=await get_ytthumb(first.get("video_id")),
            buttons=yt_search_btns(
                del_back=True,
                data_key=data_key,
                page=index,
                vid=first.get("video_id"),
                total=total,
            ),
            parse_mode="html",
        )
