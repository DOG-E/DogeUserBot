#  Copyright (C) 2020  sandeep.n(π.$)
# credits to @mrconfused (@sandy1709)
from asyncio import sleep
from os import path, remove
from re import sub

from telethon.tl.functions.users import GetFullUserRequest

from . import (
    ALIVE_NAME,
    changemymind,
    deEmojify,
    doge,
    edl,
    eor,
    fakegs,
    kannagen,
    lan,
    magik,
    mcaption,
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
        "examples": "{tr}fakegs DogeUserBot ; cool bot",
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
            return await edl(dog, "`What should i search in google.`", 5)
    dogg = await eor(dog, "`Connecting to https://www.google.com/ ...`")
    text = deEmojify(text)
    if ";" in text:
        search, result = text.split(";")
    else:
        await edl(
            dog,
            "__How should i create meme follow the syntax as show__ `.fakegs top text ; bottom text`",
            5,
        )
        return
    dogfile = await fakegs(search, result)
    await sleep(2)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if path.exists(dogfile):
        remove(dogfile)


@doge.bot_cmd(
    pattern="trump(?:\s|$)([\s\S]*)",
    command=("trump", plugin_category),
    info={
        "header": "trump tweet sticker with given custom text",
        "usage": "{tr}trump <text>",
        "examples": "{tr}trump DogeUserBot is cool bot",
    },
)
async def nekobot(dog):
    "trump tweet sticker with given custom text_"
    text = dog.pattern_match.group(1)
    text = sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edl(dog, "**Trump: **`What should I tweet`", 5)
    dogg = await eor(dog, "`Requesting trump to tweet...`")
    text = deEmojify(text)
    await sleep(2)
    dogfile = await trumptweet(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if path.exists(dogfile):
        remove(dogfile)


@doge.bot_cmd(
    pattern="cmm(?:\s|$)([\s\S]*)",
    command=("cmm", plugin_category),
    info={
        "header": "Change my mind banner with given custom text",
        "usage": "{tr}cmm <text>",
        "examples": "{tr}cmm DogeUserBot is cool bot",
    },
)
async def nekobot(dog):
    text = dog.pattern_match.group(1)
    text = sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edl(dog, "`Give text to write on banner, man`", 5)
    dogg = await eor(dog, "`Your banner is under creation wait a sec...`")
    text = deEmojify(text)
    await sleep(2)
    dogfile = await changemymind(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if path.exists(dogfile):
        remove(dogfile)


@doge.bot_cmd(
    pattern="kanna(?:\s|$)([\s\S]*)",
    command=("kanna", plugin_category),
    info={
        "header": "kanna chan sticker with given custom text",
        "usage": "{tr}kanna text",
        "examples": "{tr}kanna DogeUserBot is cool bot",
    },
)
async def nekobot(dog):
    "kanna chan sticker with given custom text"
    text = dog.pattern_match.group(1)
    text = sub("&", "", text)
    reply_to_id = await reply_id(dog)

    reply = await dog.get_reply_message()
    if not text:
        if dog.is_reply and not reply.media:
            text = reply.message
        else:
            return await edl(dog, "**Kanna : **`What should i show you`", 5)
    dogg = await eor(dog, "`Kanna is writing your text...`")
    text = deEmojify(text)
    await sleep(2)
    dogfile = await kannagen(text)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if path.exists(dogfile):
        remove(dogfile)


@doge.bot_cmd(
    pattern="tweet(?:\s|$)([\s\S]*)",
    command=("tweet", plugin_category),
    info={
        "header": "The desired person tweet sticker with given custom text",
        "usage": ["{tr}tweet <username> ; <text>", "{tr}tweet <text>"],
        "examples": "{tr}tweet iamsrk ; DogeUserBot is cool bot",
    },
)
async def nekobot(dog):
    "The desired person tweet sticker with given custom text"
    text = dog.pattern_match.group(1)
    text = sub("&", "", text)
    reply_to_id = await reply_id(dog)
    reply = await dog.get_reply_message()
    if ";" in text:
        username, text = text.split(";")
    elif not text and dog.is_reply and not reply.media:
        text = reply.message
        getuser = await dog.client(GetFullUserRequest(reply.from_id))
        username = getuser.user.first_name
    elif text and dog.is_reply:
        getuser = await dog.client(GetFullUserRequest(reply.from_id))
        username = getuser.user.first_name
        text = text
    elif text:
        text = text
        username = ALIVE_NAME
    else:
        return await edl(
            dog,
            "what should I tweet? Give some text and format must be like `.tweet much text` ",
            5,
        )
    dogg = await eor(dog, f"`Requesting {username} to tweet...`")
    text = deEmojify(text)
    await sleep(2)
    dogfile = await tweets(text, username)
    await dog.client.send_file(dog.chat_id, dogfile, reply_to=reply_to_id)
    await dogg.delete()
    if path.exists(dogfile):
        remove(dogfile)


@doge.bot_cmd(
    pattern="magik ?([\s\S]*)",
    command=("magik", plugin_category),
    info={
        "header": "Just do magik media",
        "description": "Reply to any picture and it will make magiked image.",
        "usage": [
            "{tr}magik <reply to a pic>",
        ],
    },
)
async def magiker(event):
    event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.photo:
        return await edl(event, "`Reply to a photo!`")

    dogevent = await eor(event, lan("processing"))
    teledoge = await magik(reply_message)
    await event.client.send_file(
        event.chat_id, teledoge, caption=mcaption, reply_to=reply_message
    )
    await dogevent.delete()
    remove(teledoge)
