# Created by @Jisan7509
from random import sample

from requests import get

from . import _dogeutils, doge, edl, eor, reply_id

plugin_category = "fun"


@doge.bot_cmd(
    pattern="gifs(?:\s|$)([\s\S]*)",
    command=("gifs", plugin_category),
    info={
        "header": "Sends random gifs",
        "usage": "Search and send your desire gif randomly and in bulk",
        "examples": [
            "{tr}gifs doge",
            "{tr}gifs doge ; <1-20>",
        ],
    },
)
async def some(event):
    """Sends random gifs of your query"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not inpt:
        await edl(event, "`Give an input to search...`")
    count = 1
    if ";" in inpt:
        inpt, count = inpt.split(";")
    if int(count) < 0 and int(count) > 20:
        await edl(event, "`Give value in range 1-20`")
    dogevent = await eor(event, "`Sending gif....`")
    res = get("https://giphy.com/")
    res = res.text.split("GIPHY_FE_WEB_API_KEY =")[1].split("\n")[0]
    api_key = res[2:-1]
    r = get(
        f"https://api.giphy.com/v1/gifs/search?q={inpt}&api_key={api_key}&limit=50"
    ).json()
    list_id = [r["data"][i]["id"] for i in range(len(r["data"]))]
    rlist = sample(list_id, int(count))
    for items in rlist:
        nood = await event.client.send_file(
            event.chat_id,
            f"https://media.giphy.com/media/{items}/giphy.gif",
            reply_to=reply_to_id,
        )
        await _dogeutils.unsavegif(event, nood)
    await dogevent.delete()
