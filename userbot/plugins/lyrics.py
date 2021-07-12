# credits to @mrconfused (@sandy1709)
import os

import lyricsgenius
from tswift import Song

from userbot import doge

from ..core.managers import eor

plugin_category = "extra"

GENIUS = os.environ.get("GENIUS_API_TOKEN", None)


@doge.bot_cmd(
    pattern="lyrics ?([\s\S]*)",
    command=("lyrics", plugin_category),
    info={
        "header": "Song lyrics searcher",
        "usage": [
            "{tr}lyrics <song name>",
            "{tr}lyrics <artist name> - <song name>",
        ],
        "examples": [
            "{tr}lyrics butta bomma",
            "{tr}lyrics Armaan Malik - butta bomma",
        ],
    },
)
async def _(event):
    "Song lyrics searcher"
    dogevent = await eor(event, "`wi8..! I am searching your lyrics....`")
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply.text:
        query = reply.message
    else:
        return await dogevent.edit("`What I am Supposed to find `")
    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song! try with artist name along with song if still doesnt work try `.glyrics`"
    else:
        reply = "lyrics not found! try with artist name along with song if still doesnt work try `.glyrics`"
    await eor(dogevent, reply)


@doge.bot_cmd(
    pattern="glyrics ?([\s\S]*)",
    command=("glyrics", plugin_category),
    info={
        "header": "Song lyrics searcher using genius api",
        "note": "For functioning of this command set the GENIUS_API_TOKEN in heroku. Get value from  https://genius.com/developers.",
        "usage": "{tr}glyrics <artist name> - <song name>",
        "examples": "{tr}glyrics Armaan Malik - butta bomma",
    },
)
async def lyrics(lyric):
    "Song lyrics searcher using genius api"
    if lyric.pattern_match.group(1):
        query = lyric.pattern_match.group(1)
    else:
        return await eor(
            lyric,
            "Error: please use '-' as divider for <artist> and <song> \neg: `.glyrics Nicki Minaj - Super Bass`",
        )
    if r"-" not in query:
        return await eor(
            lyric,
            "Error: please use '-' as divider for <artist> and <song> \neg: `.glyrics Nicki Minaj - Super Bass`",
        )
    if GENIUS is None:
        return await eor(
            lyric,
            "`Provide genius access token to config.py or Heroku Var first kthxbye!`",
        )
    genius = lyricsgenius.Genius(GENIUS)
    try:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
    except Exception as e:
        return await eor(lyric, f"Error:\n`{e}`")
    if len(args) < 1:
        return await eor(lyric, "`Please provide artist and song names`")
    dogevent = await eor(lyric, f"`Searching lyrics for {artist} - {song}...`")
    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None
    if songs is None:
        return await dogevent.edit(f"Song **{artist} - {song}** not found!")
    reply = f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
    await eor(dogevent, reply)
