# Credits: @mrconfused (@sandy1709)
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from re import findall

from lyricsgenius import Genius

from . import GENIUS_API, doge, eor

plugin_category = "fun"


@doge.bot_cmd(
    pattern="lyrics(?:\s|$)([\s\S]*)",
    command=("lyrics", plugin_category),
    info={
        "h": "Song lyrics searcher using genius api.",
        "d": "if you want to provide artist name with song name then use this format {tr}lyrics <artist name> - <song name> . if you use this format in your query then flags won't work. by default it will show first query.",
        "f": {
            ".l": "to get list of search lists.",
            ".n": "To get paticular song lyrics.",
        },
        "note": "For functioning of this command set the GENIUS_API with {tr}setdog command. Get value from  https://genius.com/developers.",
        "u": [
            "{tr}lyrics <artist name> - <song name>",
            "{tr}lyrics .l <song name>",
            "{tr}lyrics .n<song number> <song name>",
        ],
        "e": [
            "{tr}lyrics Armaan Malik - butta bomma",
            "{tr}lyrics .l butta bomma",
            "{tr}lyrics .n2 butta bomma",
        ],
    },
)
async def lyrics(event):  # sourcery no-metrics
    "To fetch song lyrics"
    if GENIUS_API is None:
        return await eor(
            event,
            "`Set genius access token in API vars for functioning of this command`",
        )
    match = event.pattern_match.group(1)
    songno = findall(r".n\d+", match)
    listview = findall(r".l", match)
    try:
        songno = songno[0]
        songno = songno.replace(".n", "")
        match = match.replace(".n" + songno, "")
        songno = int(songno)
    except IndexError:
        songno = 1
    if songno < 1 or songno > 10:
        return await eor(
            event,
            "`song number must be in between 1 to 10 use .l flag to query results`",
        )
    match = match.replace(".l", "")
    listview = bool(listview)
    query = match.strip()
    genius = Genius(GENIUS_API)
    if "-" in query:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
        dogevent = await eor(event, f"`Searching lyrics for {artist} - {song}...`")
        try:
            songs = genius.search_song(song, artist)
        except TypeError:
            songs = None
        if songs is None:
            return await dogevent.edit(f"Song **{artist} - {song}** not found!")
        result = f"**Search query:** \n`{artist} - {song}`\n\n```{songs.lyrics}```"
    else:
        dogevent = await eor(event, f"`Searching lyrics for {query}...`")
        response = genius.search_songs(query)
        msg = f"**The songs found for the given query:** `{query}`\n\n"
        if len(response["hits"]) == 0:
            return await eor(
                dogevent, f"**I can't find lyrics for the given query:** `{query}`"
            )
        for i, an in enumerate(response["hits"], start=1):
            msg += f"{i}. `{an['result']['title']}`\n"
        if listview:
            result = msg
        else:
            result = f"**The song found for the given query:** `{query}`\n\n"
            if songno > len(response["hits"]):
                return await eor(
                    dogevent,
                    f"**Invalid song selection for the query select proper number**\n{msg}",
                )
            songtitle = response["hits"][songno - 1]["result"]["title"]
            result += f"`{genius.search_song(songtitle).lyrics}`"
    await eor(dogevent, result)
