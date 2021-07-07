#  Copyright (C) 2020  sandeep.n(π.$)
# credits to @mrconfused (@sandy1709)
import asyncio
import os
import re

from userbot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import (
    changemymind,
    deEmojify,
    fakegs,
    kannagen,
    moditweet,
    reply_id,
    trumptweet,
    tweets,
)

plugin_category = "fun"


@doge.bot_cmd(
    pattern="fakegs(?:\s|$)([\s\S]*)",
    command=("fakegs", plugin_category),
    info={
        "header": "Fake google search meme",
        "usage": "{tr}fakegs search query ; what you mean text",
        "examples": "{tr}fakegs DogeUserBot ; One of the Popular userbot",
    },
)
async def nekobot(dog):
    "Fake google search meme"
    text = dog.pattern_match.group(1)
    reply_to_id = await reply_id(dog)
    if not text:
        if dog.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            return await edit_delete(dog, "`What should i search in google.`", 5)
    dogg = await edit_or_reply(dog, "`Connecting to https://www.google.com/ ...`")
    text = deEmojify(text)
    if ";" in text:
        search, result = text.split(";")
    else:
        await edit_delete(
            dog,
            "__How should i create meme follow the syntax as show__ `.fakegs top text ; bottom text`",
            5,
        )
        return
    dogfile = await fakegs(search, result)
    await asyncio.sleep(2)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)


@doge.bot_cmd(
    pattern="trump(?:\s|$)([\s\S]*)",
    command=("trump", plugin_category),
    info={
        "header": "trump tweet sticker with given custom text",
        "usage": "{tr}trump <text>",
        "examples": "{tr}trump DogeUserBot is One of the Popular userbot",
    },
)
async def nekobot(dog):
    "trump tweet sticker with given custom text_"
    text = dog.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(dog, "**Trump : **`What should I tweet`", 5)
    dogg = await edit_or_reply(dog, "`Requesting trump to tweet...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    dogfile = await trumptweet(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)


@doge.bot_cmd(
    pattern="modi(?:\s|$)([\s\S]*)",
    command=("modi", plugin_category),
    info={
        "header": "modi tweet sticker with given custom text",
        "usage": "{tr}modi <text>",
        "examples": "{tr}modi DogeUserBot is One of the Popular userbot",
    },
)
async def nekobot(dog):
    "modi tweet sticker with given custom text"
    text = dog.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(dog, "**Modi : **`What should I tweet`", 5)
    dogg = await edit_or_reply(dog, "Requesting modi to tweet...")
    text = deEmojify(text)
    await asyncio.sleep(2)
    dogfile = await moditweet(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)


@doge.bot_cmd(
    pattern="cmm(?:\s|$)([\s\S]*)",
    command=("cmm", plugin_category),
    info={
        "header": "Change my mind banner with given custom text",
        "usage": "{tr}cmm <text>",
        "examples": "{tr}cmm DogeUserBot is One of the Popular userbot",
    },
)
async def nekobot(dog):
    text = dog.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(dog, "`Give text to write on banner, man`", 5)
    dogg = await edit_or_reply(dog, "`Your banner is under creation wait a sec...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    dogfile = await changemymind(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)


@doge.bot_cmd(
    pattern="kanna(?:\s|$)([\s\S]*)",
    command=("kanna", plugin_category),
    info={
        "header": "kanna chan sticker with given custom text",
        "usage": "{tr}kanna text",
        "examples": "{tr}kanna DogeUserBot is One of the Popular userbot",
    },
)
async def nekobot(dog):
    "kanna chan sticker with given custom text"
    text = dog.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(dog, "**Kanna : **`What should i show you`", 5)
    dogg = await edit_or_reply(dog, "`Kanna is writing your text...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    dogfile = await kannagen(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)


@doge.bot_cmd(
    pattern="tweet(?:\s|$)([\s\S]*)",
    command=("tweet", plugin_category),
    info={
        "header": "The desired person tweet sticker with given custom text",
        "usage": "{tr}tweet <username> ; <text>",
        "examples": "{tr}tweet iamsrk ; DogeUserBot is One of the Popular userbot",
    },
)
async def nekobot(dog):
    "The desired person tweet sticker with given custom text"
    text = dog.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edit_delete(
                dog,
                "what should I tweet? Give some text and format must be like `.tweet username ; your text` ",
                5,
            )
    if ";" in text:
        username, text = text.split(";")
    else:
        await edit_delete(
            dog,
            "__what should I tweet? Give some text and format must be like__ `.tweet username ; your text`",
            5,
        )
        return
    dogg = await edit_or_reply(dog, f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    await asyncio.sleep(2)
    dogfile = await tweets(text, username)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if os.path.exists(dogfile):
        os.remove(dogfile)
