# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from base64 import b64decode

from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import InputStickerSetID, InputStickerSetShortName
from telethon.utils import get_display_name

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    MONTHS,
    _dogeutils,
    doge,
    edl,
    eor,
    fsmessage,
    gvar,
    media_type,
    newmsgres,
    sgvar,
)

plugin_category = "misc"


async def spam_function(event, teledoge, dog, sleeptimem, sleeptimet, DelaySpam=False):
    # sourcery no-metrics
    counter = int(dog[0])
    if len(dog) == 2:
        spam_message = str(dog[1])
        for _ in range(counter):
            if gvar("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await teledoge.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await sleep(sleeptimet)
    elif event.reply_to_msg_id and teledoge.media:
        for _ in range(counter):
            if gvar("spamwork") is None:
                return
            teledoge = await event.client.send_file(
                event.chat_id, teledoge, caption=teledoge.text
            )
            await _dogeutils.unsavegif(event, teledoge)
            await sleep(sleeptimem)
        if BOTLOG:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#SPAM\n"
                        + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message",
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} times with below message with delay {sleeptimet} seconds",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#DELAYSPAM\n"
                    + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) with {counter} times with below message with delay {sleeptimet} seconds",
                )

            teledoge = await event.client.send_file(BOTLOG_CHATID, teledoge)
            await _dogeutils.unsavegif(event, teledoge)
        return
    elif event.reply_to_msg_id and teledoge.text:
        spam_message = teledoge.text
        for _ in range(counter):
            if gvar("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#SPAM\n"
                    + f"Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat  with {counter} messages of \n"
                    + f"`{spam_message}`",
                )
    elif BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#DELAYSPAM\n"
                + f"Delay spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with delay {sleeptimet} seconds and with {counter} messages of \n"
                + f"`{spam_message}`",
            )


@doge.bot_cmd(
    pattern="spam ([\s\S]*)",
    command=("spam", plugin_category),
    info={
        "h": "Floods the text in the chat !! with given number of times,",
        "d": "Sends the replied media/message <count> times !! in the chat",
        "u": ["{tr}spam <count> <text>", "{tr}spam <count> reply to message"],
        "e": "{tr}spam 10 hi",
    },
)
async def spammer(event):
    "Floods the text in the chat !!"
    teledoge = await event.get_reply_message()
    dog = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(dog[0])
    except Exception:
        return await edl(
            event, "__Use proper syntax to spam. For syntax refer doge menu.__"
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    sgvar("spamwork", True)
    await spam_function(event, teledoge, dog, sleeptimem, sleeptimet)


@doge.bot_cmd(
    pattern="spspam$",
    command=("spspam", plugin_category),
    info={
        "h": "To spam the chat with stickers.",
        "d": "To spam chat with all stickers in that replied message sticker pack.",
        "u": "{tr}spspam",
    },
)
async def stickerpack_spam(event):
    "To spam the chat with stickers."
    reply = await event.get_reply_message()
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edl(
            event, "`reply to any sticker to send all stickers in that pack`"
        )
    hmm = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    try:
        stickerset_attr = reply.document.attributes[1]
        dogevent = await eor(
            event, "`Fetching details of the sticker pack, please wait..`"
        )
    except BaseException:
        await edl(event, "`This is not a sticker. Reply to a sticker.`", 5)
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await edl(
            dogevent,
            "`I guess this sticker is not part of any pack so i can't kang this sticker pack try kang for this sticker`",
        )
    try:
        hmm = Get(hmm)
        await event.client(hmm)
    except BaseException:
        pass
    reqd_sticker_set = await event.client(
        GetStickerSetRequest(
            stickerset=InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    sgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvar("spamwork") is None:
            return
        await event.client.send_file(event.chat_id, m)
        await sleep(0.7)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with pack ",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SPSPAM\n"
                + f"Sticker Pack Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with pack",
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@doge.bot_cmd(
    pattern="cspam ([\s\S]*)",
    command=("cspam", plugin_category),
    info={
        "h": "Spam the text letter by letter",
        "d": "Spam the chat with every letter in given text as new message.",
        "u": "{tr}cspam <text>",
        "e": "{tr}cspam DogeUserBot",
    },
)
async def tmeme(event):
    "Spam the text letter by letter."
    cspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = cspam.replace(" ", "")
    await event.delete()
    sgvar("spamwork", True)
    for letter in message:
        if gvar("spamwork") is None:
            return
        await event.respond(letter)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with: `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#CSPAM\n"
                + f"Letter Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with: `{message}`",
            )


@doge.bot_cmd(
    pattern="wspam ([\s\S]*)",
    command=("wspam", plugin_category),
    info={
        "h": "Spam the text word by word.",
        "d": "Spams the chat with every word in given text as new message.",
        "u": "{tr}wspam <text>",
        "e": "{tr}wspam I am using DogeUserBot",
    },
)
async def tmeme(event):
    "Spam the text word by word"
    wspam = str("".join(event.text.split(maxsplit=1)[1:]))
    message = wspam.split()
    await event.delete()
    sgvar("spamwork", True)
    for word in message:
        if gvar("spamwork") is None:
            return
        await event.respond(word)
    if BOTLOG:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in [User](tg://user?id={event.chat_id}) chat with: `{message}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#WSPAM\n"
                + f"Word Spam was executed successfully in {get_display_name(await event.get_chat())}(`{event.chat_id}`) chat with: `{message}`",
            )


@doge.bot_cmd(
    pattern="(delayspam|dspam) ([\s\S]*)",
    command=("delayspam", plugin_category),
    info={
        "h": "To spam the chat with count number of times with given text and given delay sleep time.",
        "d": "For example if you see this dspam 2 10 hi. Then you will send 10 hi text messages with 2 seconds gap between each message.",
        "u": [
            "{tr}delayspam <delay> <count> <text>",
            "{tr}dspam <delay> <count> <text>",
        ],
        "e": ["{tr}delayspam 2 10 hi", "{tr}dspam 2 10 hi"],
    },
)
async def spammer(event):
    "To spam with custom sleep time between each message"
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await edl(
            event, "__Use proper syntax to spam. For syntax refer doge menu.__"
        )
    dog = input_str[1:]
    try:
        int(dog[0])
    except Exception:
        return await edl(
            event, "__Use proper syntax for delay spam. For syntax refer doge menu.__"
        )
    await event.delete()
    sgvar("spamwork", True)
    await spam_function(event, reply, dog, sleeptimem, sleeptimet, DelaySpam=True)


# Credits to robotlog ~ https://github.com/robotlog/SiriUserBot/blob/d2231b436b7dae9e4075d22c747666df9f13819e/userbot/modules/sinfo.py#L35
@doge.bot_cmd(
    pattern="limitc$",
    command=("limitc", plugin_category),
    info={
        "h": "Check the limit status of your Telegram account.",
        "d": "You shouldn't break Telegram's rules to avoid being restricted by any limit.",
        "u": "{tr}limitc",
    },
)
async def limitchecker(event):
    "To limit check from Telegram with @SpamInfo"
    dogevent = await eor(event, "**⏳ I'm checking limit for your account...**")
    chat = "@SpamBot"
    lstatus = None
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, text="/start", chat=chat)
        lstatus = await newmsgres(conv, chat)
        if lstatus.text.startswith(
            "Dear"
            or "عَزِيز"
            or "Thân yêu"
            or "Querido"
            or "亲爱的"
            or "Drag"
            or "Milovaný"
            or "Kære"
            or "Dierbaar"
            or "Rakas"
            or "Aimé"
            or "Cher"
            or "Lieb"
            or "αγαπητός"
            or "Caro"
            or "親愛な"
            or "사랑하는"
            or "Kjær"
            or "Kochany"
            or "дорогой"
            or "Kär"
            or "ซึ่งเป็นที่รักยิ่ง"
            or "Шановний"
        ):
            gstatus = lstatus.text.split("until ")[1].split(", ")[0]
            ldays, lmonths, lyears = (
                gstatus.split(" ")[0],
                MONTHS[gstatus.split(" ")[1]],
                gstatus.split(" ")[2],
            )
            lhours = (
                lstatus.text.split(":")[0].split(", ")[1]
                + ":"
                + lstatus.text.split(":")[1].split("UTC.")[0]
            )
            collecx = f"**📅 Your account limit will expire on {ldays} {lmonths} {lyears} {lhours}.**"
            await eor(dogevent, collecx)
        elif lstatus.text.startswith("Good news"):
            await eor(
                dogevent,
                "**🐾 You don't have any limits.\n\n😏 I think you're the freest person on Telegram!**",
            )
        else:
            await event.client.forward_messages(event.chat_id, lstatus)
            await dogevent.delete()
        await conv.mark_read()
        await conv.cancel_all()
