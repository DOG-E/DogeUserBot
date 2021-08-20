from os import listdir, mkdir, path, remove
from random import choice
from shutil import rmtree

from bs4 import BeautifulSoup
from requests import get, post

from ..helpers.google_image_download import googleimagesdownload
from . import doge, edl, eor, lan, logging, reply_id

plugin_category = "misc"
LOGS = logging.getLogger(path.basename(__name__))


async def wall_download(piclink, query):
    try:
        if not path.isdir("./temp"):
            mkdir("./temp")
        picpath = f"./temp/{query.title().replace(' ', '')}.jpg"
        if path.exists(picpath):
            i = 1
            while path.exists(picpath) and i < 11:
                picpath = f"./temp/{query.title().replace(' ', '')}-{i}.jpg"
                i += 1
        with open(picpath, "wb") as f:
            f.write(get(piclink).content)
        return picpath
    except Exception as e:
        LOGS.info(str(e))
        return None


@doge.bot_cmd(
    pattern="wal(?:\s|$)([\s\S]*)",
    command=("wal", plugin_category),
    info={
        "header": "Searches and uploads wallpaper",
        "usage": ["{tr}wal <query>", "{tr}wal <query> , <1-10>"],
        "examples": ["{tr}wal dog", "{tr}wal dog , 2"],
    },
)
async def noods(event):
    "Wallpaper searcher"
    query = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    limit = 1
    if not query:
        return await edl(event, "`what should i search`")
    if "," in query:
        query, limit = query.split(",")
    if int(limit) > 10:
        return await edl(event, "`Wallpaper search limit is 1-10`")
    dogevent = await eor(event, "🔍 `Searching...`")
    r = get(f"https://wall.alphacoders.com/search.php?search={query.replace(' ','+')}")
    soup = BeautifulSoup(r.content, "lxml")
    walls = soup.find_all("img", class_="img-responsive")
    if not walls:
        return await edl(dogevent, f"**Can't find anything with** `{query}`")
    i = count = 0
    piclist = []
    piclinks = []
    captionlist = []
    await eor(dogevent, lan("processing"))
    url2 = "https://api.alphacoders.com/content/get-download-link"
    for x in walls:
        wall = choice(walls)["src"][8:-4]
        server = wall.split(".")[0]
        fileid = wall.split("-")[-1]
        data = {
            "content_id": fileid,
            "content_type": "wallpaper",
            "file_type": "jpg",
            "image_server": server,
        }
        res = post(url2, data=data)
        a = res.json()["link"]
        if "We are sorry," not in get(a).text and a not in piclinks:
            await eor(dogevent, "📥** Downloading...**")
            pic = await wall_download(a, query)
            if pic is None:
                return await edl(dogevent, "__Sorry i can't download wallpaper.__")
            piclist.append(pic)
            piclinks.append(a)
            captionlist.append("")
            count += 1
            i = 0
        else:
            i += 1
        await eor(dogevent, f"**📥 Downloaded: {count}/{limit}\n\n❌ Errors: {i}/5**")
        if count == int(limit):
            break
        if i == 5:
            await eor(dogevent, "`Max search error limit exceed..`")
    try:
        await eor(dogevent, "`Sending...`")
        captionlist[-1] = f"**➥ Query:-** `{query.title()}`"
        await event.client.send_file(
            event.chat_id,
            piclist,
            caption=captionlist,
            reply_to=reply_to_id,
            force_document=True,
        )
        await dogevent.delete()
    except Exception as e:
        LOGS.info(str(e))
    for i in piclist:
        remove(i)


@doge.bot_cmd(
    pattern="wall(?:\s|$)([\s\S]*)",
    command=("wall", plugin_category),
    info={
        "header": "Searches and uploads wallpaper from google",
        "usage": ["{tr}wall <query>", "{tr}wall <query> , <1-10>"],
        "examples": ["{tr}wall dog", "{tr}wall dog , 2"],
    },
)
async def gwallpapers(event):
    wn_input = event.pattern_match.group(1)
    if not wn_input:
        return await edl(event, "`Give me something to search..`")
    limit = 1
    if "," in wn_input:
        wn_input, limit = wn_input.split(",")
    if int(limit) > 10:
        return await edl(event, "`Wallpaper search limit is 1-10`")

    dogevent = await eor(event, "`Processing Keep Patience...`")
    wallname = f"hd {wn_input}"
    googleimages = googleimagesdownload()
    args = {
        "keywords": wallname,
        "limit": limit,
        "format": "jpg",
        "output_directory": "./downloads/",
    }
    googleimages.download(args)
    dog = choice(listdir(path.abspath(f"./downloads/{wallname}/")))
    await event.client.send_file(event.chat_id, f"./downloads/{wallname}/{dog}")
    rmtree(f"./downloads/{wallname}/")
    await dogevent.delete()
