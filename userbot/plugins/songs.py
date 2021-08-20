# by  @sandy1709 ( https://t.me/mrconfused  )
from base64 import b64decode
from io import FileIO
from os import path, remove
from pathlib import Path

from ShazamAPI import Shazam
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import DocumentAttributeFilename
from validators.url import url as vurl
from youtubesearchpython.Video import get as Vget

from . import (
    _dogeutils,
    doge,
    edl,
    eor,
    fsmessage,
    hmention,
    logging,
    media_type,
    name_dl,
    reply_id,
    song_dl,
    video_dl,
    yt_search,
)

plugin_category = "fun"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
SONGBOT_BLOCKED_STRING = "<code>Please unblock @songdl_bot and try again</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@doge.bot_cmd(
    pattern="song(320)?(?:\s|$)([\s\S]*)",
    command=("song", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def _(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await eor(event, "`What I am Supposed to find `")
    dog = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogevent = await eor(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not vurl(video_link):
        return await dogevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        dog = Get(dog)
        await event.client(dog)
    except BaseException:
        pass
    stderr = (await _dogeutils.runcmd(song_cmd))[1]
    if stderr:
        return await dogevent.edit(f"**Error:** `{stderr}`")
    dogname, stderr = (await _dogeutils.runcmd(name_cmd))[:2]
    if stderr:
        return await dogevent.edit(f"**Error:** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    dogname = path.splitext(dogname)[0]
    # if stderr:
    #    return await dogevent.edit(f"**Error:** `{stderr}`")
    song_file = Path(f"{dogname}.mp3")
    if not path.exists(song_file):
        return await dogevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await dogevent.edit("`yeah..! i found something wi8..🥰`")
    dogthumb = Path(f"{dogname}.jpg")
    if not path.exists(dogthumb):
        dogthumb = Path(f"{dogname}.webp")
    elif not path.exists(dogthumb):
        dogthumb = None
    ytdata = Vget(video_link)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"<b><i>➥ Title :- {ytdata['title']}</i></b>\n<b><i>➥ Uploaded by:- {hmention}</i></b>",
        parse_mode="html",
        thumb=dogthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await dogevent.delete()
    for files in (dogthumb, song_file):
        if files and path.exists(files):
            remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@doge.bot_cmd(
    pattern="vsong(?:\s|$)([\s\S]*)",
    command=("vsong", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "To search video songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await eor(event, "`What I am Supposed to find`")
    dog = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    dogevent = await eor(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not vurl(video_link):
        return await dogevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _dogeutils.runcmd(video_cmd))[1]
    if stderr:
        return await dogevent.edit(f"**Error:** `{stderr}`")
    dogname, stderr = (await _dogeutils.runcmd(name_cmd))[:2]
    if stderr:
        return await dogevent.edit(f"**Error:** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        dog = Get(dog)
        await event.client(dog)
    except BaseException:
        pass
    # if stderr:
    #    return await dogevent.edit(f"**Error:** `{stderr}`")
    dogname = path.splitext(dogname)[0]
    vsong_file = Path(f"{dogname}.mp4")
    if not path.exists(vsong_file):
        vsong_file = Path(f"{dogname}.mkv")
    elif not path.exists(vsong_file):
        return await dogevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await dogevent.edit("`yeah..! i found something wi8..🥰`")
    dogthumb = Path(f"{dogname}.jpg")
    if not path.exists(dogthumb):
        dogthumb = Path(f"{dogname}.webp")
    elif not path.exists(dogthumb):
        dogthumb = None
    ytdata = Vget(video_link)
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=f"<b><i>➥ Title :- {ytdata['title']}</i></b>\n<b><i>➥ Uploaded by:- {hmention}</i></b>",
        parse_mode="html",
        thumb=dogthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await dogevent.delete()
    for files in (dogthumb, vsong_file):
        if files and path.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="shazam$",
    command=("shazam", plugin_category),
    info={
        "header": "To reverse search song.",
        "description": "Reverse search audio file using shazam api",
        "usage": "{tr}shazam <reply to voice/audio>",
    },
)
async def shazamcmd(event):
    "To reverse search song."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edl(
            event, "__Reply to Voice clip or Audio clip to reverse search that song.__"
        )
    dogevent = await eor(event, "__Downloading the audio clip...__")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, DocumentAttributeFilename):
                name = attr.file_name
        dl = FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edl(dogevent, f"**Error while reverse searching song:**\n__{e}__")
    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**Song:** `{song}`", reply_to=reply
    )
    await dogevent.delete()


# reverse search by  @Lal_bakthan
@doge.bot_cmd(
    pattern="szm$",
    command=("szm", plugin_category),
    info={
        "header": "To reverse search music file.",
        "description": "music file lenght must be around 10 sec so use ffmpeg plugin to trim it.",
        "usage": "{tr}szm",
    },
)
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await edl(event, "```Reply to an audio message.```")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    dogevent = await eor(event, "```Identifying the song```")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event=event, text="/start", chat=chat)
        await conv.get_response()
        await conv.send_message(reply_message)
        check = await conv.get_response()
        if not check.text.startswith("Audio received"):
            return await dogevent.edit(
                "An error while identifying the song. Try to use a 5-10s long audio message."
            )
        await dogevent.edit("Wait just a sec...")
        result = await conv.get_response()
        await conv.mark_read()
        await conv.cancel_all()
    namem = f"**Song Name: **`{result.text.splitlines()[0]}`\
        \n\n**Details: **__{result.text.splitlines()[2]}__"
    await dogevent.edit(namem)


@doge.bot_cmd(
    pattern="sng ?([\s\S]*)",
    command=("sng", plugin_category),
    info={
        "header": "Get Songs from @LyBot quickly",
        "usage": [
            "{tr}sng <song_name>",
            "{tr}sng <reply to a song name>",
        ],
        "examples": ["{tr}sng Erik Dalı"],
    },
)
async def lybot(e):
    "Get your song asap!"
    reply_to = await reply_id(e)
    args = e.pattern_match.group(1)
    if not args:
        if e.is_reply:
            reply = await e.get_reply_message()
            args = reply.text
        else:
            await edl(e, "`No input found`")
    eris = await eor(e, "`Searching for your song 🎵`")
    res = await e.client.inline_query(
        "lybot",
        args,
    )
    try:
        await res[0].click(
            e.chat_id,
            hide_via=True,
            reply_to=reply_to,
        )
        await eris.delete()
    except Exception as fx:
        await eris.edit(f"`{fx}`")
