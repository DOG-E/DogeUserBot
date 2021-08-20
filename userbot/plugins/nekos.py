"""NEKOS MODULE FOR PEPEBOT
Plugin Made by [NIKITA](https://t.me/kirito6969)
**DON'T EVEN TRY TO CHANGE CREDITS**'
"""
from os import remove

from fake_useragent import UserAgent
from nekos import img as nimg
from PIL.Image import open as Imopen
from requests import get
from simplejson.errors import JSONDecodeError

from . import (
    PMSGTEXT,
    _dogeutils,
    age_verification,
    doge,
    edl,
    eor,
    hub,
    lan,
    reply_id,
    wowmygroup,
)

plugin_category = "hub"


def user_agent():
    return UserAgent().random


@doge.bot_cmd(
    pattern="nn ?([\s\S]*)",
    command=("nn", plugin_category),
    info={
        "header": "Contains NSFW \nSearch images from nekos",
        "usage": "{tr}nn <argument from choice>",
        "examples": "{tr}nn neko",
        "Choice": hub.nsfw(hub.hemtai),
    },
)
async def _(event):
    "Search images from nekos"
    reply_to = await reply_id(event)
    choose = event.pattern_match.group(1)
    if choose not in hub.hemtai:
        return await edl(
            event,
            f"**Wrong category!! Choose from here:**\n\n{hub.nsfw(hub.hemtai)}",
            60,
        )
    if await age_verification(event, reply_to):
        return
    dogevent = await eor(event, lan("processing"))
    flag = await wowmygroup(event, PMSGTEXT)
    if flag:
        return
    target = nimg(f"{choose}")
    nohorny = await event.client.send_file(
        event.chat_id, file=target, caption=f"**{choose}**", reply_to=reply_to
    )
    await _dogeutils.unsavegif(event, nohorny)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="dva$",
    command=("dva", plugin_category),
    info={
        "header": "Search dva images",
        "usage": "{tr}dva",
    },
)
async def dva(event):
    "Search dva images"
    reply_to = await reply_id(event)
    if await age_verification(event, reply_to):
        return
    try:
        nsfw = get(
            "https://api.computerfreaker.cf/v1/dva",
            headers={"User-Agent": user_agent()},
        ).json()
        url = nsfw.get("url")
    except JSONDecodeError:
        return await edl(event, "`uuuf.. seems like api down, try again later.`")
    if not url:
        return await edl(event, "`uuuf.. No URL found from the API`")
    await event.client.send_file(event.chat_id, file=url, reply_to=reply_to)
    await event.delete()


@doge.bot_cmd(
    pattern="nsfw$",
    command=("nsfw", plugin_category),
    info={
        "header": "NSFW \nSearch nsfw from nekos",
        "usage": "{tr}nsfw",
    },
)
async def avatarlewd(event):
    "NSFW. Search nsfw from nekos"
    reply_to = await reply_id(event)
    if await age_verification(event, reply_to):
        return
    flag = await wowmygroup(event, PMSGTEXT)
    if flag:
        return
    with open("temp.png", "wb") as f:
        target = "nsfw_avatar"
        f.write(get(nimg(target)).content)
    img = Imopen("temp.png")
    img.save("temp.webp", "webp")
    await event.client.send_file(
        event.chat_id, file=open("temp.webp", "rb"), reply_to=reply_to
    )
    remove("temp.webp")
    await event.delete()


@doge.bot_cmd(
    pattern="lewdn$",
    command=("lewdn", plugin_category),
    info={
        "header": "NSFW \nSearch lewd nekos",
        "usage": "{tr}lewdn",
    },
)
async def lewdn(event):
    "NSFW.Search lewd nekos"
    reply_to = await reply_id(event)
    if await age_verification(event, reply_to):
        return
    flag = await wowmygroup(event, PMSGTEXT)
    if flag:
        return
    nsfw = get("https://nekos.life/api/lewd/neko").json()
    url = nsfw.get("neko")
    if not url:
        return await edl(event, "`Uff.. No NEKO found from the API`")
    await event.client.send_file(event.chat_id, file=url, reply_to=reply_to)
    await event.delete()


@doge.bot_cmd(
    pattern="gasm$",
    command=("gasm", plugin_category),
    info={
        "header": "NSFW \nIt's gasm",
        "usage": "{tr}gasm",
    },
)
async def gasm(event):
    "NSFW. It's gasm"
    reply_to = await reply_id(event)
    if await age_verification(event, reply_to):
        return
    flag = await wowmygroup(event, PMSGTEXT)
    if flag:
        return
    with open("temp.png", "wb") as f:
        target = "gasm"
        f.write(get(nimg(target)).content)
    img = Imopen("temp.png")
    img.save("temp.webp", "webp")
    await event.client.send_file(
        event.chat_id, file=open("temp.webp", "rb"), reply_to=reply_to
    )
    remove("temp.webp")
    await event.delete()


@doge.bot_cmd(
    pattern="ifu$",
    command=("ifu", plugin_category),
    info={
        "header": "Search waifus from nekos",
        "usage": "{tr}ifu",
    },
)
async def waifu(event):
    "Search waifus from nekos"
    reply_to = await reply_id(event)
    with open("temp.png", "wb") as f:
        target = "waifu"
        f.write(get(nimg(target)).content)
    img = Imopen("temp.png")
    img.save("temp.webp", "webp")
    await event.client.send_file(
        event.chat_id, file=open("temp.webp", "rb"), reply_to=reply_to
    )
    remove("temp.webp")
    await event.delete()
