# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from collections import defaultdict
from os import path
from re import compile, findall
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from telethon import Button
from ujson import dump, load, loads
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError, GeoRestrictedError
from youtubesearchpython import VideosSearch

from ...Config import Config
from ...core import pool
from ...core.logger import logging
from ..aiohttp_helper import AioHttp
from ..progress import humanbytes
from .functions import sublists

LOGS = logging.getLogger(__name__)

BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./userbot/cache/ytsearch.json"

song_dl = "youtube-dl --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "youtube-dl --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "youtube-dl --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' -f '[filesize<20M]' {video_link}"
name_dl = (
    "youtube-dl --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


async def yt_search(dog):
    try:
        dog = quote(dog)
        html = urlopen(f"https://www.youtube.com/results?search_query={dog}")
        user_data = findall(r"watch\?v=(\S{11})", html.read().decode())
        video_link = []
        k = 0
        for i in user_data:
            if user_data:
                video_link.append("https://www.youtube.com/watch?v=" + user_data[k])
            k += 1
            if k > 3:
                break
        if video_link:
            return video_link[0]
        return "Couldn't fetch results"
    except Exception:
        return "Couldn't fetch results"


async def ytsearch(query, limit):
    result = ""
    videolinks = VideosSearch(query.lower(), limit=limit)
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += (
                f"**◽ Dᴇsᴄʀɪᴘᴛɪoɴ:** `{v['descriptionSnippet'][-1]['text']}`\n"
            )
        except Exception:
            textresult += "**◽ Dᴇsᴄʀɪᴘᴛɪoɴ:** `None`\\n"
        textresult += f"**⏱ Dᴜʀᴀᴛɪoɴ:** __{v['duration']}__   **◾ Vɪᴇᴡs:** __{v['viewCount']['short']}__\n"
        result += f"📺 {textresult}\n"
    return result


class YT_Search_X:
    def __init__(self):
        if not path.exists(PATH):
            with open(PATH, "w") as f_x:
                dump({}, f_x)
        with open(PATH) as yt_db:
            self.db = load(yt_db)

    def store_(self, rnd_id: str, results: dict):
        self.db[rnd_id] = results
        self.save()

    def save(self):
        with open(PATH, "w") as outfile:
            dump(self.db, outfile, indent=4)


ytsearch_data = YT_Search_X()


async def yt_data(dog):
    params = {"format": "json", "url": dog}
    url = "https://www.youtube.com/oembed"  # https://stackoverflow.com/questions/29069444/returning-the-urls-as-a-list-from-a-youtube-search-query
    query_string = urlencode(params)
    url = f'{url}?{query_string}'
    with urlopen(url) as response:
        response_text = response.read()
        data = loads(response_text.decode())
    return data


async def get_ytthumb(videoid: str):
    thumb_quality = [
        "maxresdefault.jpg",  # Best quality
        "hqdefault.jpg",
        "sddefault.jpg",
        "mqdefault.jpg",
        "default.jpg",  # Worst quality
    ]
    thumb_link = "https://i.imgur.com/4LwPLai.png"
    for q in thumb_quality:
        link = f"https://i.ytimg.com/vi/{videoid}/{q}"
        if await AioHttp().get_status(link) == 200:
            thumb_link = link
            break
    return thumb_link


def get_yt_video_id(url: str):
    if match := YOUTUBE_REGEX.search(url):
        return match.group(1)


# Based on https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f
def get_choice_by_id(choice_id, media_type: str):
    if choice_id == "mkv":
        choice_str = "bestvideo+bestaudio/best"
        disp_str = "best(video+audio)"
    elif choice_id == "mp3":
        choice_str = "320"
        disp_str = "320 Kbps"
    elif choice_id == "mp4":
        choice_str = "bestvideo[ext=webm]+251/bestvideo[ext=mp4]+(258/256/140/bestaudio[ext=m4a])/bestvideo[ext=webm]+(250/249)/best"
        disp_str = "best(video+audio)[webm/mp4]"
    else:
        disp_str = str(choice_id)
        if media_type == "v":
            choice_str = f'{disp_str}+(258/256/140/bestaudio[ext=m4a])/best'
        else:  # Audio
            choice_str = disp_str
    return choice_str, disp_str


async def result_formatter(results: list):
    output = {}
    for index, r in enumerate(results, start=1):
        v_deo_id = r.get("id")
        thumb = await get_ytthumb(v_deo_id)
        upld = r.get("channel")
        title = f'<a href={r.get("link")}><b>{r.get("title")}</b></a>\n'
        out = title
        if r.get("descriptionSnippet"):
            out += "<code>{}</code>\n\n".format(
                "".join(x.get("text") for x in r.get("descriptionSnippet"))
            )
        out += f'<b>❯ Duration:</b> {r.get("accessibility").get("duration")}\n'
        views = f'<b>❯ Views:</b> {r.get("viewCount").get("short")}\n'
        out += views
        out += f'<b>❯ Upload Date:</b> {r.get("publishedTime")}\n'
        if upld:
            out += "<b>❯ Uploader:</b> "
            out += f'<a href={upld.get("link")}>{upld.get("name")}</a>'

        output[index] = dict(
            message=out,
            thumb=thumb,
            video_id=v_deo_id,
            list_view=f'<img src={thumb}><b><a href={r.get("link")}>{index}. {r.get("accessibility").get("title")}</a></b><br>',
        )

    return output


def yt_search_btns(
    data_key: str, page: int, vid: str, total: int, del_back: bool = False
):
    buttons = [
        [
            Button.inline(
                text="⬅️️ Bᴀcᴋ", data=f"ytdl_back_{data_key}_{page}"
            ),
            Button.inline(
                text=f"🔹 {page} - {total} 🔹",
                data=f"ytdl_next_{data_key}_{page}",
            ),
        ],
        [
            Button.inline(
                text="📜 Lɪsᴛ Aʟʟ", data=f"ytdl_listall_{data_key}_{page}"
            ),
            Button.inline(text="📥 Doᴡɴʟoᴀᴅ", data=f"ytdl_download_{vid}_0"),
        ],
    ]

    if del_back:
        buttons[0].pop(0)
    return buttons


@pool.run_in_thread
def download_button(vid: str, body: bool = False):  # sourcery no-metrics
    try:
        vid_data = YoutubeDL({"no-playlist": True}).extract_info(
            BASE_YT_URL + vid, download=False
        )
    except ExtractorError:
        vid_data = {"formats": []}
    buttons = [
        [
            Button.inline("🌟 Bᴇsᴛ - 🎞 ᴍᴋᴠ", data=f"ytdl_download_{vid}_mkv_v"),
            Button.inline(
                "🌟 Bᴇsᴛ - 🎞 ᴡᴇʙᴍ/ᴍᴘ4", data=f"ytdl_download_{vid}_mp4_v"
            ),
        ]
    ]


    qual_dict = defaultdict(lambda: defaultdict(int))
    qual_list = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p"]
    audio_dict = {}
    for video in vid_data["formats"]:
        fr_note = video.get("format_note")
        fr_id = int(video.get("format_id"))
        fr_size = video.get("filesize")
        if video.get("ext") == "mp4":
            for frmt_ in qual_list:
                if fr_note in (frmt_, f'{frmt_}60'):
                    qual_dict[frmt_][fr_id] = fr_size
        if video.get("acodec") != "none":
            bitrrate = int(video.get("abr", 0))
            if bitrrate != 0:
                audio_dict[
                    bitrrate
                ] = f"🎵 {bitrrate}ᴋʙᴘs ({humanbytes(fr_size) or '-'})"

    video_btns = []
    for frmt in qual_list:
        frmt_dict = qual_dict[frmt]
        if len(frmt_dict) != 0:
            frmt_id = sorted(list(frmt_dict))[-1]
            frmt_size = humanbytes(frmt_dict.get(frmt_id)) or "-"
            video_btns.append(
                Button.inline(
                    f"📺 {frmt} ({frmt_size})",
                    data=f"ytdl_download_{vid}_{frmt_id}_v",
                )
            )
    buttons += sublists(video_btns, width=2)
    buttons += [
        [
            Button.inline(
                "🌟 Bᴇsᴛ - 🎵 ᴍᴘ3 - 320ᴋʙᴘs", data=f"ytdl_download_{vid}_mp3_a"
            )
        ]
    ]

    buttons += sublists(
        [
            Button.inline(audio_dict.get(key_), data=f"ytdl_download_{vid}_{key_}_a")
            for key_ in sorted(audio_dict.keys())
        ],
        width=2,
    )
    if body:
        vid_body = f"<a href={vid_data.get('webpage_url')}><b>[{vid_data.get('title')}]</b></a>"
        return vid_body, buttons
    return buttons


@pool.run_in_thread
def _tubeDl(url: str, starttime, uid: str):
    ydl_opts = {
        "addmetadata": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": path.join(
            Config.TEMP_DIR, str(starttime), "%(title)s-%(format)s.%(ext)s"
        ),
        # "logger": LOGS,
        "format": uid,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "postprocessors": [
            {"key": "FFmpegMetadata"}
            # ERROR R15: Memory quota vastly exceeded
            # {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
        "quiet": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            x = ydl.download([url])
    except DownloadError as e:
        LOGS.error(e)
    except GeoRestrictedError:
        LOGS.error(
            "**🚨 Eʀʀoʀ:** The uploader hasn't made this video available in your country."
        )

    else:
        return x


@pool.run_in_thread
def _mp3Dl(url: str, starttime, uid: str):
    _opts = {
        "outtmpl": path.join(Config.TEMP_DIR, str(starttime), "%(title)s.%(ext)s"),
        # "logger": LOGS,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": uid,
            },
            {"key": "EmbedThumbnail"},  # ERROR: Conversion failed!
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    try:
        with YoutubeDL(_opts) as ytdl:
            dloader = ytdl.download([url])
    except Exception as y_e:
        LOGS.exception(y_e)
        return y_e
    else:
        return dloader
