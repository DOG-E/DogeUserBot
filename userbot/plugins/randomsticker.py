from os import remove
from random import choice
from urllib.parse import quote

from nekos import cat
from PIL.Image import open as Imopen
from requests import get
from telethon.functions.messages import GetStickerSetRequest
from telethon.types import InputStickerSetShortName
from telethon.utils import get_input_document

from . import doge, reply_id

plugin_category = "fun"


@doge.bot_cmd(
    pattern="cat$",
    command=("cat", plugin_category),
    info={
        "header": "To get random cat stickers.",
        "usage": "{tr}cat",
    },
)
async def _(event):
    "To get random cat stickers."
    await event.delete()
    reply_to_id = await reply_id(event)
    with open("temp.png", "wb") as f:
        f.write(get(cat()).content)
    img = Imopen("temp.png")
    img.save("temp.webp", "webp")
    img.seek(0)
    await event.client.send_file(
        event.chat_id, open("temp.webp", "rb"), reply_to=reply_to_id
    )
    remove("temp.webp")


# credit to @r4v4n4
@doge.bot_cmd(
    pattern="dab$",
    command=("dab", plugin_category),
    info={
        "header": "To get random dabbing pose stickers.",
        "usage": "{tr}dab",
    },
)
async def _(event):
    "To get random dabbing pose stickers."
    reply_to_id = await reply_id(event)
    blacklist = {
        1653974154589768377,
        1653974154589768312,
        1653974154589767857,
        1653974154589768311,
        1653974154589767816,
        1653974154589767939,
        1653974154589767944,
        1653974154589767912,
        1653974154589767911,
        1653974154589767910,
        1653974154589767909,
        1653974154589767863,
        1653974154589767852,
        1653974154589768677,
    }
    await event.delete()
    docs = [
        get_input_document(x)
        for x in (
            await event.client(
                GetStickerSetRequest(InputStickerSetShortName("DabOnHaters"))
            )
        ).documents
        if x.id not in blacklist
    ]
    await event.respond(file=choice(docs), reply_to=reply_to_id)


@doge.bot_cmd(
    pattern="brain$",
    command=("brain", plugin_category),
    info={
        "header": "To get random brain stickers.",
        "usage": "{tr}brain",
    },
)
async def handler(event):
    "To get random brain stickers."
    reply_to_id = await reply_id(event)
    blacklist = {}
    await event.delete()
    docs = [
        get_input_document(x)
        for x in (
            await event.client(
                GetStickerSetRequest(InputStickerSetShortName("supermind"))
            )
        ).documents
        if x.id not in blacklist
    ]
    await event.respond(file=choice(docs), reply_to=reply_to_id)


# By:- git: jaskaranSM tg: @Zero_cool7870
@doge.bot_cmd(
    pattern="pat$",
    command=("pat", plugin_category),
    info={
        "header": "To get random pat stickers.",
        "usage": "{tr}pat",
    },
)
async def lastfm(event):
    "To get random pat stickers."
    await event.delete()
    reply_to_id = await reply_id(event)
    resp = get("http://headp.at/js/pats.json")
    pats = resp.json()
    pat = "https://headp.at/pats/{}".format(quote(choice(pats)))
    with open("pat.webp", "wb") as f:
        f.write(get(pat).content)
    await event.client.send_file(event.chat_id, "pat.webp", reply_to=reply_to_id)
    remove("pat.webp")
