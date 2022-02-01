# Copyright (C) 2019 The Raphielscape Company LLC.
#
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
from asyncio import sleep
from os import environ
from re import sub
from sys import setrecursionlimit
from urllib.parse import quote

from pylast import LastFMNetwork, MalformedResponseError, User, WSError, md5
from telethon.errors import AboutTooLongError
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    deEmojify,
    doge,
    gvar,
    hide_inlinebot,
    logging,
    reply_id,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

LASTFM_PASS = md5(gvar("LASTFM_PASSWORD_PLAIN"))
if (
    gvar("LASTFM_API")
    and gvar("LASTFM_SECRET")
    and gvar("LASTFM_USERNAME")
    and LASTFM_PASS
):
    lastfm = LastFMNetwork(
        api_key=gvar("LASTFM_API"),
        api_secret=gvar("LASTFM_SECRET"),
        username=gvar("LASTFM_USERNAME"),
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None

# =================== CONSTANT ===================
LFM_BIO_ENABLED = "```last.fm'den bio'ya güncel müzik aktarıldı.```"
LFM_BIO_DISABLED = "```last.fm'den bio'ya güncel müzik aktarımı devre dışı. Bio varsayılana döndürüldü.```"
LFM_BIO_RUNNING = "```last.fm'den bio'ya güncel müzik aktarımı zaten çalışıyor.```"
LFM_BIO_ERR = "```Seçenek belirtilmedi.```"
LFM_LOG_ENABLED = "```bot günlüğüne last.fm günlüğü etkinleştirildi.```"
LFM_LOG_DISABLED = "```bot günlüğüne last.fm günlüğü devre dışı bırakıldı.```"
LFM_LOG_ERR = "```Seçenek belirtilmedi.```"
ERROR_MSG = "```last.fm modülü durduruldu, beklenmeyen bir hata oluştu```"
# ================================================


class LASTFM:
    def __init__(self):
        self.ARTIST = 0
        self.SONG = 0
        self.USER_ID = 0
        self.LASTFMCHECK = False
        self.RUNNING = False
        self.LastLog = False


LASTFM_ = LASTFM()


async def gettags(track=None, isNowPlaying=None, playing=None):
    if isNowPlaying:
        tags = playing.get_top_tags()
        arg = playing
        if not tags:
            tags = playing.artist.get_top_tags()
    else:
        tags = track.track.get_top_tags()
        arg = track.track
    if not tags:
        tags = arg.artist.get_top_tags()
    tags = "".join(" #" + t.item.__str__() for t in tags[:5])
    tags = sub("^ ", "", tags)
    tags = sub(" ", "_", tags)
    tags = sub("_#", " #", tags)
    return tags


async def artist_and_song(track):
    return f"{track.track}"


async def get_curr_track(lfmbio):  # sourcery no-metrics
    oldartist = ""
    oldsong = ""
    while LASTFM_.LASTFMCHECK:
        DEFAULT_BIO = gvar("DEFAULT_BIO") or "🐶 @DogeUserBot 🐾"
        try:
            if LASTFM_.USER_ID == 0:
                LASTFM_.USER_ID = (await lfmbio.client.get_me()).id
            user_info = await doge(GetFullUserRequest(LASTFM_.USER_ID))
            LASTFM_.RUNNING = True
            playing = User(gvar("LASTFM_USERNAME"), lastfm).get_now_playing()
            LASTFM_.SONG = playing.get_title()
            LASTFM_.ARTIST = playing.get_artist()
            oldsong = environ.get("oldsong", None)
            oldartist = environ.get("oldartist", None)
            if (
                playing is not None
                and LASTFM_.SONG != oldsong
                and LASTFM_.ARTIST != oldartist
            ):
                environ["oldsong"] = str(LASTFM_.SONG)
                environ["oldartist"] = str(LASTFM_.ARTIST)
                if gvar("BIO_PREFIX"):
                    lfmbio = (
                        f"{gvar('BIO_PREFIX')} 🎧: {LASTFM_.ARTIST} - {LASTFM_.SONG}"
                    )
                else:
                    lfmbio = f"🎧: {LASTFM_.ARTIST} - {LASTFM_.SONG}"
                try:
                    if BOTLOG and LASTFM_.LastLog:
                        await doge.bot.send_message(
                            BOTLOG_CHATID,
                            f"**Bio şu şekilde değiştirildi:**\n`{lfmbio}`",
                        )
                    await doge(UpdateProfileRequest(about=lfmbio))
                except AboutTooLongError:
                    short_bio = f"🎧: {LASTFM_.SONG}"
                    await doge(UpdateProfileRequest(about=short_bio))
            if playing is None and user_info.about != DEFAULT_BIO:
                await sleep(6)
                await doge(UpdateProfileRequest(about=DEFAULT_BIO))
                if BOTLOG and LASTFM_.LastLog:
                    await doge.bot.send_message(
                        BOTLOG_CHATID, f"**Bio eski haline döndürüldü:**\n{DEFAULT_BIO}"
                    )
        except AttributeError:
            try:
                if user_info.about != DEFAULT_BIO:
                    await sleep(6)
                    await doge(UpdateProfileRequest(about=DEFAULT_BIO))
                    if BOTLOG and LASTFM_.LastLog:
                        await doge.bot.send_message(
                            BOTLOG_CHATID,
                            f"**Bio eski haline döndürüldü:**\n{DEFAULT_BIO}",
                        )
            except FloodWaitError as err:
                if BOTLOG and LASTFM_.LastLog:
                    await doge.bot.send_message(
                        BOTLOG_CHATID, f"**Bio değiştirilirken hata oluştu:**\n{err}"
                    )
        except (
            FloodWaitError,
            WSError,
            MalformedResponseError,
            AboutTooLongError,
        ) as err:
            if BOTLOG and LASTFM_.LastLog:
                await doge.bot.send_message(
                    BOTLOG_CHATID, f"**Bio değiştirilirken hata oluştu:**\n{err}"
                )
        await sleep(2)
    LASTFM_.RUNNING = False


@doge.bot_cmd(
    pattern="lastfm$",
    command=("lastfm", plugin_category),
    info={
        "h": "Scrobble verilerini last.fm'den getirir.",
        "d": "O anda izlenen parçayı, eğer hiçbir şey çalmıyorsa, en son çalan parçanın verilerini gösterir.",
        "u": "{tr}lastfm",
    },
)
async def last_fm(lastFM):
    ".lastfm komutu ile, scrobble verilerini last.fm'den getirir."
    await lastFM.edit("**⏳ İşleniyor...**")
    preview = None
    playing = User(gvar("LASTFM_USERNAME"), lastfm).get_now_playing()
    username = f"https://www.last.fm/user/{gvar('LASTFM_USERNAME')}"
    if playing is not None:
        try:
            image = (
                User(gvar("LASTFM_USERNAME"), lastfm)
                .get_now_playing()
                .get_cover_image()
            )
        except IndexError:
            image = None
        tags = await gettags(isNowPlaying=True, playing=playing)
        rectrack = quote(f"{playing}")
        rectrack = sub("^", "https://open.spotify.com/search/", rectrack)
        if image:
            output = f"[‎]({image})[{gvar('LASTFM_USERNAME')}]({username}) __şimdi şunu dinliyor:__\n\n• [{playing}]({rectrack})\n"
            preview = True
        else:
            output = f"[{gvar('LASTFM_USERNAME')}]({username}) __şimdi şunu dinliyor:__\n\n• [{playing}]({rectrack})\n"
    else:
        recent = User(gvar("LASTFM_USERNAME"), lastfm).get_recent_tracks(limit=3)
        playing = User(gvar("LASTFM_USERNAME"), lastfm).get_now_playing()
        output = (
            f"[{gvar('LASTFM_USERNAME')}]({username}) __en son şunu dinliyordu:__\n\n"
        )
        for i, track in enumerate(recent):
            LOGS.info(i)
            printable = await artist_and_song(track)
            tags = await gettags(track)
            rectrack = quote(str(printable))
            rectrack = sub("^", "https://open.spotify.com/search/", rectrack)
            output += f"• [{printable}]({rectrack})\n"
            if tags:
                output += f"`{tags}`\n\n"
    if preview is not None:
        await lastFM.edit(f"{output}", parse_mode="md", link_preview=True)
    else:
        await lastFM.edit(f"{output}", parse_mode="md")


@doge.bot_cmd(
    pattern="now$",
    command=("now", plugin_category),
    info={
        "h": "Dinlediğiniz şarkıyı Lastfm/Spotify/Deezer'dan gönderir.",
        "u": "{tr}now",
        "note": "Bu komutun çalışması için @NowPlayBot'u yetkilendirmeniz gerekir.",
    },
)
async def now(event):
    "Dinlediğiniz mevcut şarkınızı gönderr."
    text = " "
    reply_to_id = await reply_id(event)
    bot_name = "@nowplaybot"
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="inow$",
    command=("inow", plugin_category),
    info={
        "h": "Dinlediğiniz mevcut şarkınızı harika bir görüntü şeklinde gösterir.",
        "u": "{tr}inow",
        "note": "Bu komutun çalışması için @SpotiPieBot'u yetkilendirmeniz gerekir.",
    },
)
async def nowimg(event):
    "Mevcut dinleme şarkınızı gösterir."
    text = " "
    reply_to_id = await reply_id(event)
    bot_name = "@Spotipiebot"
    text = deEmojify(text)
    await event.delete()
    await hide_inlinebot(event.client, bot_name, text, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="lastbio (on|off)",
    command=("lastbio", plugin_category),
    info={
        "h": "last.fm'i çalan şarkıy bio'da etkinleştirmek veya devre dışı bırakır.",
        "u": [
            "{tr}lastbio on",
            "{tr}lastbio off",
        ],
    },
)
async def lastbio(lfmbio):
    "Tlast.fm'i çalan şarkıy bio'da etkinleştirmek veya devre dışı bırakır."
    arg = lfmbio.pattern_match.group(1).lower()
    if arg == "on":
        setrecursionlimit(700000)
        if not LASTFM_.LASTFMCHECK:
            LASTFM_.LASTFMCHECK = True
            environ["errorcheck"] = "0"
            await lfmbio.edit(LFM_BIO_ENABLED)
            await sleep(4)
            await get_curr_track(lfmbio)
        else:
            await lfmbio.edit(LFM_BIO_RUNNING)
    elif arg == "off":
        DEFAULT_BIO = gvar("DEFAULT_BIO") or "🐶 @DogeUserBot 🐾"
        LASTFM_.LASTFMCHECK = False
        LASTFM_.RUNNING = False
        await lfmbio.client(UpdateProfileRequest(about=DEFAULT_BIO))
        await lfmbio.edit(LFM_BIO_DISABLED)
    else:
        await lfmbio.edit(LFM_BIO_ERR)


@doge.bot_cmd(
    pattern="lastlog (on|off)",
    command=("lastlog", plugin_category),
    info={
        "h": "Last.fm'in mevcut oynatmasını günlük grubuna göndermesini etkinleştirmek veya devre dışı bırakır.",
        "u": [
            "{tr}lastlog on",
            "{tr}lastlog off",
        ],
    },
)
async def lastlog(lstlog):
    "Last.fm'in mevcut oynatmasını günlük grubuna göndermesini etkinleştirmek veya devre dışı bırakır"
    arg = lstlog.pattern_match.group(1).lower()
    LASTFM_.LastLog = False
    if arg == "on":
        LASTFM_.LastLog = True
        await lstlog.edit(LFM_LOG_ENABLED)
    elif arg == "off":
        LASTFM_.LastLog = False
        await lstlog.edit(LFM_LOG_DISABLED)
    else:
        await lstlog.edit(LFM_LOG_ERR)
