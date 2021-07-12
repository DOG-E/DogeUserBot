import os
import random

import requests
from bs4 import BeautifulSoup

from . import doge, edl, eor, reply_id, wall_download

plugin_category = "misc"


@doge.bot_cmd(
    pattern="wall([\s\S]*)",
    command=("wall", plugin_category),
    info={
        "header": "Sends wallpaper",
        "usage": [
            "{tr}wall <query>",
            "{tr}wall <query> ; <1-10>",
        ],
        "examples": [
            "{tr}wall doge",
            "{tr}wall doge ; 2",
        ],
    },
)
async def wallpapers(event):
    "Sends wallpaper"
    query = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    limit = 1
    if not query:
        await edl(event, "**Give some text ⁉️**", 10)
    if ";" in query:
        query, limit = query.split(";")
    if int(limit) > 10:
        return await edl(event, f"**Wallpaper search limit is 1-10**", 10)
    await eor(event, "🔍 `Searching...`")
    r = requests.get(
        f"https://wall.alphacoders.com/search.php?search={query.replace(' ','+')}"
    )
    soup = BeautifulSoup(r.content, "lxml")
    walls = soup.find_all("img", class_="img-responsive")
    if not walls:
        return await edl(event, f"**Can't find anything with {query}**", 10)
    i = count = 0
    piclist = []
    piclinks = []
    captionlist = []
    await eor(event, "⏳ `Processing..`")
    url2 = "https://api.alphacoders.com/content/get-download-link"
    for x in walls:
        wall = random.choice(walls)["src"][8:-4]
        server = wall.split(".")[0]
        fileid = wall.split("-")[-1]
        data = {
            "content_id": fileid,
            "content_type": "wallpaper",
            "file_type": "jpg",
            "image_server": server,
        }
        res = requests.post(url2, data=data)
        a = res.json()["link"]
        if "We are sorry," not in requests.get(a).text and a not in piclinks:
            await eor(event, "📥** Downloading...**")
            pic = await wall_download(a, query)
            if pic is None:
                return await edl(event, "__Sorry i can't download wallpaper.__")
            piclist.append(pic)
            piclinks.append(a)
            captionlist.append("")
            count += 1
            i = 0
        else:
            i += 1
        await eor(event, f"**📥 Downloaded : {count}/{limit}\n\n❌ Errors : {i}/5**")
        if count == int(limit):
            break
        if i == 5:
            await eor(event, "`Max search error limit exceed..`")
    try:
        await eor(event, "`Sending...`")
        captionlist[-1] = f"**➥ Query :-** `{query.title()}`"
        await event.client.send_file(
            event.chat_id,
            piclist,
            caption=captionlist,
            reply_to=reply_to_id,
            force_document=True,
        )
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
    for i in piclist:
        os.remove(i)
