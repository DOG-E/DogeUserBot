# By @kirito6969 for PepeBot
# Don't edit credits Madafaka
"""
This module can search images in danbooru and send in to the chat!
──「 **Danbooru Search** 」──
"""

from os import remove
from urllib.request import urlretrieve

from requests import get

from . import PMSGTEXT, age_verification, doge, edl, eor, lan, reply_id, wowmygroup

plugin_category = "hub"


@doge.bot_cmd(
    pattern="ani(m|nsfw) ?([\s\S]*)",
    command=("ani", plugin_category),
    info={
        "header": "Contains NSFW 🔞.\nTo search images in danbooru!",
        "usage": [
            "{tr}anim <query>",
            "{tr}aninsfw <nsfw query>",
        ],
        "examples": [
            "{tr}anim naruto",
            "{tr}aninsfw naruto",
        ],
    },
)
async def danbooru(event):
    "Get anime charecter pic or nsfw"
    reply_to = await reply_id(event)
    if await age_verification(event, reply_to):
        return
    dogevent = await eor(event, lan("processing"))
    flag = await wowmygroup(event, PMSGTEXT)
    if flag:
        return
    rating = "Explicit" if "nsfw" in event.pattern_match.group(1) else "Safe"
    search_query = event.pattern_match.group(2)
    params = {
        "limit": 1,
        "random": "true",
        "tags": f"Rating:{rating} {search_query}".strip(),
    }
    with get("http://danbooru.donmai.us/posts.json", params=params) as response:
        if response.status_code == 200:
            response = response.json()
        else:
            return await edl(
                dogevent,
                f"**An error occurred, response code: **`{response.status_code}`",
            )

    if not response:
        return await edl(dogevent, f"**No results for query:** __{search_query}__")
    valid_urls = [
        response[0][url]
        for url in ["file_url", "large_file_url", "source"]
        if url in response[0].keys()
    ]
    if not valid_urls:
        return await edl(
            dogevent, f"**Failed to find URLs for query:** __{search_query}__"
        )
    for image_url in valid_urls:
        try:
            await event.client.send_file(event.chat_id, image_url, reply_to=reply_to)
            await dogevent.delete()
            return
        except Exception as e:
            await edl(dogevent, f"{e}")
    await edl(dogevent, f"**Failed to fetch media for query:** __{search_query}__")


@doge.bot_cmd(
    pattern="boobs(?:\s|$)([\s\S]*)",
    command=("boobs", plugin_category),
    info={
        "header": "NSFW 🔞\nYou know what it is, so do I !",
        "usage": "{tr}boobs",
        "examples": "{tr}boobs",
    },
)
async def boobs(e):
    "Search boobs"
    reply_to = await reply_id(e)
    if await age_verification(e, reply_to):
        return
    a = await eor(e, "`Sending boobs...`")
    flag = await wowmygroup(e, PMSGTEXT)
    if flag:
        return
    nsfw = get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urlretrieve(f"http://media.oboobs.ru/{nsfw}", "boobs.jpg")
    await e.client.send_file(e.chat_id, "boobs.jpg", reply_to=reply_to)
    remove("boobs.jpg")
    await a.delete()


@doge.bot_cmd(
    pattern="butts(?:\s|$)([\s\S]*)",
    command=("butts", plugin_category),
    info={
        "header": "NSFW 🔞\nBoys and some girls likes to Spank this 🍑",
        "usage": "{tr}butts",
        "examples": "{tr}butts",
    },
)
async def butts(e):
    "Search beautiful butts"
    reply_to = await reply_id(e)
    if await age_verification(e, reply_to):
        return
    a = await eor(e, "`Sending beautiful butts...`")
    flag = await wowmygroup(e, PMSGTEXT)
    if flag:
        return
    nsfw = get("http://api.obutts.ru/butts/10/1/random").json()[0]["preview"]
    urlretrieve(f"http://media.obutts.ru/{nsfw}", "butts.jpg")
    await e.client.send_file(e.chat_id, "butts.jpg", reply_to=reply_to)
    remove("butts.jpg")
    await a.delete()
