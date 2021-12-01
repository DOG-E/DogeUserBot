# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from json import loads
from os import path
from random import choice
from uuid import uuid4
from zipfile import ZipFile

from ..utils.extdl import install_pip

try:
    from imdb import IMDb
except ModuleNotFoundError:
    install_pip("IMDbPY")
    from imdb import IMDb

from googletrans import Translator
from requests import get
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.events import NewMessage
from telethon.tl.functions.contacts import UnblockRequest

imdb = IMDb()
mov_titles = [
    "long imdb title",
    "long imdb canonical title",
    "smart long imdb canonical title",
    "smart canonical title",
    "canonical title",
    "localized title",
]


def sublists(input_list: list, width: int = 3):
    return [input_list[x : x + width] for x in range(0, len(input_list), width)]


def rand_key():
    return str(uuid4())[:8]


def reddit_thumb_link(preview, thumb=None):
    for i in preview:
        if "width=216" in i:
            thumb = i
            break
    if not thumb:
        thumb = preview.pop()
    return thumb.replace("\u0026", "&")


async def get_cast(casttype, movie):
    mov_casttype = ""
    if casttype in list(movie.keys()):
        i = 0
        for j in movie[casttype]:
            if i < 1:
                mov_casttype += str(j)
            elif i < 5:
                mov_casttype += ", " + str(j)
            else:
                break
            i += 1
    else:
        mov_casttype += "Not data"
    return mov_casttype


async def get_moviecollections(movie):
    result = ""
    if "box office" in movie.keys():
        for i in movie["box office"].keys():
            result += f"\n• <b>{i}:</b> <code>{movie['box office'][i]}</code>"
    else:
        result = f"<code>Veri Yok!</code>"
    return result


# Credits: AsenaDev - https://github.com/yusufusta/AsenaUserBot/blob/master/userbot/modules/sozluk.py#L45
def getSimilarWords(wordx, limit=5):
    similars = []
    if not path.exists("autocomplete.json"):
        words = get(f"https://sozluk.gov.tr/autocomplete.json")
        open("autocomplete.json", "a+").write(words.text)
        words = words.json()
    else:
        words = loads(open("autocomplete.json", "r").read())
    for word in words:
        if word["madde"].startswith(wordx) and not word["madde"] == wordx:
            if len(similars) > limit:
                break
            similars.append(word["madde"])
    similarsStr = ""
    for similar in similars:
        if similarsStr != "":
            similarsStr += ", "
        similarsStr += f"`{similar}`"
    return similarsStr


# https://github.com/ssut/py-googletrans/issues/234#issuecomment-722379788
async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


# Credits: Robotlog - https://github.com/robotlog/SiriUserBot/blob/master/userbot/helps/forc.py#L5
async def fsmessage(event, text, forward=False, chat=None):
    cHat = chat if chat else event.chat_id
    if not forward:
        try:
            e = await event.client.send_message(cHat, text)
        except YouBlockedUserError:
            await event.client(UnblockRequest(cHat))
            e = await event.client.send_message(cHat, text)
    else:
        try:
            e = await event.client.forward_messages(cHat, text)
        except YouBlockedUserError:
            await event.client(UnblockRequest(cHat))
            e = await event.client.forward_messages(cHat, text)
    return e


async def fsfile(event, file=None, chat=None):
    cHat = chat if chat else event.chat_id
    try:
        e = await event.send_file(cHat, file)
    except YouBlockedUserError:
        await event.client(UnblockRequest(cHat))
        e = await event.send_file(cHat, file)
    return e


async def newmsgres(conv, chat, timeout=None):
    if timeout:
        response = await conv.wait_event(
            NewMessage(incoming=True, from_users=chat), timeout=timeout
        )
    else:
        response = await conv.wait_event(NewMessage(incoming=True, from_users=chat))
    return response


async def clippy(borg, msg, chat_id, reply_to_id):
    chat = "@Clippy"
    async with borg.conversation(chat) as conv:
        await fsfile(borg, msg, chat)
        pic = await newmsgres(conv, chat)
        await borg.send_file(
            chat_id,
            pic.message.media,
            reply_to=reply_to_id,
        )
        await conv.mark_read()
        await conv.cancel_all()


async def mememaker(event, msg, dog, chat_id, reply_to_id):
    chat = "@TheMemeMakerBot"
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, msg, chat=chat)
        pic = await newmsgres(conv, chat)
        await dog.delete()
        await event.client.send_file(
            chat_id,
            pic.message.media,
            reply_to=reply_to_id,
        )
        await conv.mark_read()
        await conv.cancel_all()


async def xiaomeme(event, msg, dogevent):
    chat = "@XiaomiGeeksBot"
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, msg, chat=chat)
        xio = await newmsgres(conv, chat)
        await dogevent.delete()
        await event.client.forward_messages(event.chat_id, xio.message)
        await conv.mark_read()
        await conv.cancel_all()


async def sanga_seperator(sanga_list):
    for i in sanga_list:
        if i.startswith("🔗"):
            sanga_list.remove(i)
    s = 0
    for i in sanga_list:
        if i.startswith("Username History"):
            break
        s += 1
    usernames = sanga_list[s:]
    names = sanga_list[:s]
    return names, usernames


async def unzip(downloaded_file_name):
    with ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall("./temp")
    downloaded_file_name = path.splitext(downloaded_file_name)[0]
    return f"{downloaded_file_name}.gif"


async def hide_inlinebot(borg, bot_name, text, chat_id, reply_to_id, c_lick=0):
    sticcers = await borg.inline_query(bot_name, f"{text}")
    dog = await sticcers[c_lick].click("me", hide_via=True)
    if dog:
        await borg.send_file(int(chat_id), dog, reply_to=reply_to_id)
        await dog.delete()


async def hide_inlinebot_point(borg, bot_name, text, chat_id, reply_to_id, c_lick=0):
    sticcers = await borg.inline_query(bot_name, f"{text}.")
    dog = await sticcers[c_lick].click("me", hide_via=True)
    if dog:
        await borg.send_file(int(chat_id), dog, reply_to=reply_to_id)
        await dog.delete()


async def waifutxt(text, chat_id, reply_to_id, bot):
    animus = [
        0,
        1,
        2,
        3,
        4,
        9,
        15,
        20,
        22,
        27,
        29,
        32,
        33,
        34,
        37,
        38,
        41,
        42,
        44,
        45,
        47,
        48,
        51,
        52,
        53,
        55,
        56,
        57,
        58,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query("stickerizerbot", f"#{choice(animus)}{text}")
    dog = await sticcers[0].click("me", hide_via=True)
    if dog:
        await bot.send_file(int(chat_id), dog, reply_to=reply_to_id)
        await dog.delete()
