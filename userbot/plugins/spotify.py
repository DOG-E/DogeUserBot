# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
from asyncio import sleep
from json import loads
from json.decoder import JSONDecodeError
from os import environ, path, remove
from sys import setrecursionlimit

from requests import get, post
from spotify_token import start_session
from telegraph import Telegraph
from telethon.errors import AboutTooLongError
from telethon.events import NewMessage
from telethon.tl.functions.account import UpdateProfileRequest

from . import (
    BIO_PREFIX,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    Config,
    doge,
    edl,
    eor,
    fsmessage,
)

plugin_category = "misc"

telegraph = Telegraph()
SP_DC = Config.SP_DC
SP_KEY = Config.SP_KEY

# =================== CONSTANT ===================
SPO_BIO_ENABLED = "`Spotify current music to bio is now enabled.`"
SPO_BIO_DISABLED = "`Spotify current music to bio is now disabled. "
SPO_BIO_RUNNING = "`Spotify current music to bio is already running.`"
ERROR_MSG = "`Spotify module halted, got an unexpected error.`"
SPO_BIO_ERR = "```No option specified.```"
# ================================================


class SPOTIFY:
    def __init__(self):
        self.ARTIST = 0
        self.SONG = 0
        self.SPOTIFYCHECK = False
        self.RUNNING = False
        self.OLDEXCEPT = False
        self.PARSE = False


SPOTIFY_ = SPOTIFY()


async def get_spotify_token():
    sptoken = start_session(SP_DC, SP_KEY)
    access_token = sptoken[0]
    environ["spftoken"] = access_token


async def update_spotify_info():  # sourcery no-metrics
    oldartist = ""
    oldsong = ""
    while SPOTIFY_.SPOTIFYCHECK:
        try:
            SPOTIFY_.RUNNING = True
            spftoken = environ.get("spftoken", None)
            hed = {"Authorization": "Bearer " + spftoken}
            url = "https://api.spotify.com/v1/me/player/currently-playing"
            response = get(url, headers=hed)
            data = loads(response.content)
            artist = data["item"]["album"]["artists"][0]["name"]
            song = data["item"]["name"]
            SPOTIFY_.OLDEXCEPT = False
            oldsong = environ.get("oldsong", None)
            if song != oldsong and artist != oldartist:
                oldartist = artist
                environ["oldsong"] = song
                if BIO_PREFIX:
                    spobio = f"{BIO_PREFIX} 🎧: {artist} - {song}"
                else:
                    spobio = f"🎧: {artist} - {song}"
                try:
                    await doge(UpdateProfileRequest(about=spobio))
                except AboutTooLongError:
                    short_bio = f"🎧: {song}"
                    await doge(UpdateProfileRequest(about=short_bio))
                environ["errorcheck"] = "0"
        except KeyError:
            print(2)
            errorcheck = environ.get("errorcheck", None)
            if errorcheck == 0:
                await update_token()
            elif errorcheck == 1:
                SPOTIFY_.SPOTIFYCHECK = False
                await doge(UpdateProfileRequest(about=DEFAULT_BIO))
                print(ERROR_MSG)
                if BOTLOG:
                    await doge.send_message(BOTLOG_CHATID, ERROR_MSG)
        except JSONDecodeError:
            print(3)
            SPOTIFY_.OLDEXCEPT = True
            await sleep(6)
            await doge(UpdateProfileRequest(about=DEFAULT_BIO))
        except TypeError:
            print(4)
            await dirtyfix()
        except Exception as e:
            print(e)
        SPOTIFY_.SPOTIFYCHECK = False
        await sleep(2)
        await dirtyfix()
    SPOTIFY_.RUNNING = False


async def update_token():
    sptoken = start_session(SP_DC, SP_KEY)
    access_token = sptoken[0]
    environ["spftoken"] = access_token
    environ["errorcheck"] = "1"
    await update_spotify_info()


async def dirtyfix():
    SPOTIFY_.SPOTIFYCHECK = True
    await sleep(4)
    await update_spotify_info()


def msToStr(time):
    seconds = round((time / 1000) % 60)
    minutes = int((time / (1000 * 60)) % 60)
    text = str(minutes) + ":"
    if seconds < 10:
        text += "0" + str(seconds)
    else:
        text += str(seconds)
    return text


def generatePlayerStr(now, time):
    string = "─"
    arr = []
    for _ in range(0, 18):
        arr.append(string)
    index = int((now * 18) / time)
    if index >= len(arr):
        index = len(arr) - 1
    arr[index] = "⚪"
    return "".join(arr)


def get_spotify_info(TIME=5):
    try:
        spftoken = environ.get("spftoken", None)
        hed = {"Authorization": "Bearer " + spftoken}
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        response = get(url, headers=hed)
        data = loads(response.content)
        item = data["item"]
        artistsStr = ""
        artists = []
        if len(item["artists"]) > 0:
            for i in item["artists"]:
                artists.append(str(i["name"]))
            artistsStr = ", ".join(artists)
            artistsStr = "\n__" + artistsStr + "__"
        song = f"**{item['name']}**"
        songinfo = song + artistsStr
        name = item["name"] + " - " + (", ".join(artists))
        image = "🔄"
        try:
            url = item["external_urls"]["spotify"]
            url = f"[Open on Spotify]({url})"
        except Exception:
            url = "Spotify now playing"
        nowtime = int(data["progress_ms"])
        totaltime = int(item["duration_ms"])
        if len(item["album"]["images"]) > 0:
            telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
            if path.exists("@DogeUserBot-Spotify.jpg"):
                remove("@DogeUserBot-Spotify.jpg")
            try:
                r = get(str(item["album"]["images"][0]["url"]))
                with open("@DogeUserBot-Spotify.jpg", "wb") as f:
                    f.write(r.content)
                with open("@DogeUserBot-Spotify.jpg", "rb") as f:
                    req = post(
                        "https://telegra.ph/upload",
                        files={
                            "Hey": ("Hey", f, "image/jpeg")
                        },  # image/gif, image/jpeg, image/jpg, image/png, video/mp4
                    ).json()
                    image = "[🔄](https://telegra.ph" + req[0]["src"] + ")"
            except Exception:
                pass
        if path.exists("@DogeUserBot-Spotify.jpg"):
            remove("@DogeUserBot-Spotify.jpg")
        art = []
        message = ""
        Stop = False
        for _ in range(0, TIME):
            nowstr = msToStr(nowtime)
            totalstr = msToStr(totaltime)
            progress = generatePlayerStr(nowtime, totaltime)
            mp = (
                progress
                + "\n\n◄◄⠀▐▐ ⠀►►⠀⠀⠀ "
                + nowstr
                + " / "
                + totalstr
                + f"⠀⠀⠀{image}🔀\n\n{url}"
            )
            if message == "":
                message = mp
            appendstr = songinfo + "\n\n" + mp
            if appendstr not in art:
                art.append(appendstr)
            nowtime += 1000
            if nowtime > totaltime:
                nowtime = totaltime
                Stop = True
            elif Stop is True or nowstr == totalstr:
                break
        arr = [message, name, art]
        return arr
    except KeyError:
        print(2)
        return "Error! Couldn't fetch the song playing on Spotify!"
    except JSONDecodeError:
        print(3)
        return "I'm not listening to anything on Spotify right now."
    except TypeError:
        print(4)
        return "Error! Couldn't fetch the song playing on Spotify!"
    except Exception as e:
        print(e)
        return "Error! Couldn't fetch the song playing on Spotify!"


@doge.bot_cmd(
    pattern="spotify (on|off)",
    command=("spotifybio", plugin_category),
    info={
        "header": "To enable or disable the Spotify current playing to bio.",
        "usage": [
            "{tr}spotify on",
            "{tr}spotify off",
        ],
    },
)
async def set_biostgraph(setstbio):
    arg = setstbio.pattern_match.group(1).lower()
    if arg == "on":
        setrecursionlimit(700000)
        if not SPOTIFY_.SPOTIFYCHECK:
            environ["errorcheck"] = "0"
            await setstbio.edit(SPO_BIO_ENABLED)
            await get_spotify_token()
            await dirtyfix()
        else:
            await setstbio.edit(SPO_BIO_RUNNING)
    elif arg == "off":
        SPOTIFY_.SPOTIFYCHECK = False
        SPOTIFY_.RUNNING = False
        await doge(UpdateProfileRequest(about=DEFAULT_BIO))
        await setstbio.edit(SPO_BIO_DISABLED)
    else:
        await setstbio.edit(SPO_BIO_ERR)


@doge.bot_cmd(
    pattern="spotifymp3",
    command=("spotifymp3", plugin_category),
    info={
        "header": "Send current Spotify playing song.",
        "usage": "{tr}spotifymp3",
    },
)
async def getmp3(event):
    dogevent = await eor(event, "I'm bringing a song I listened to on Spotify...")
    try:
        await get_spotify_token()
    except Exception:
        return await edl(
            dogevent,
            "__You haven't set the api value. Set Api var __`SP_DC` __and__ `SP_KEY` __in Heroku get value.",
        )
    info = get_spotify_info()
    if isinstance(info, list) is False:
        await eor(dogevent, info)
    else:
        msg = info[0]
        songinfo = info[1]
        msgs = info[2]
        chat = "@DeezerMusicBot"
        try:
            async with doge.conversation(chat) as conv:
                musics = await conv.wait_event(
                    NewMessage(incoming=True, from_users=chat)
                )
                await fsmessage(event, text=songinfo, chat=chat)
                await event.client.send_read_acknowledge(conv.chat_id)

                if musics.audio:
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client.send_message(
                        event.chat_id, msg, file=musics.message
                    )
                    await dogevent.delete()
                elif musics.buttons[0][0].text == "No results":
                    for item in enumerate(msgs):
                        await dogevent.edit(item[1], link_preview=True)
                        await sleep(1)
                    return
                else:
                    await musics.click(0)
                    songgg = await conv.wait_event(
                        NewMessage(incoming=True, from_users=chat)
                    )
                    await event.client.send_read_acknowledge(conv.chat_id)
                    await event.client.send_message(
                        event.chat_id, msg, file=songgg.message
                    )
                    await dogevent.delete()

        except Exception as e:
            print(e)
            for item in enumerate(msgs):
                await dogevent.edit(item[1], link_preview=True)
                await sleep(1)
