import asyncio

from telethon.utils import get_display_name

from .. import *
from . import _dogeutils

months = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}


async def spam_function(event, teledoge, dog, sleeptimem, sleeptimet, DelaySpam=False):
    # sourcery no-metrics
    counter = int(dog[0])
    if len(dog) == 2:
        spam_message = str(dog[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await teledoge.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and teledoge.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            teledoge = await event.client.send_file(
                event.chat_id, teledoge, caption=teledoge.text
            )
            await _dogeutils.unsavegif(event, teledoge)
            await asyncio.sleep(sleeptimem)
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
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
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
