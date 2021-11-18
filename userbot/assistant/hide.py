# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# Callback:
# hide_(.*)
# ================================================================
from json import load
from os import path
from re import compile

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name
from . import doge, lan


@doge.tgbot.on(CallbackQuery(data=compile(b"hide_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if path.exists("./userbot/hide.txt"):
        jsondata = load(open("./userbot/hide.txt"))
        try:
            reply_pop_up_alert = jsondata[f"{timestamp}"]["text"]
        except KeyError:
            reply_pop_up_alert = f"🚨 {lan('errrnoservermsg')}"
    else:
        reply_pop_up_alert = f"🚨 {lan('errrnoservermsg')}"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
