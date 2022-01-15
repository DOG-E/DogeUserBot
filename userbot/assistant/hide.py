# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import load
from os import path
from re import compile

from telethon.events import CallbackQuery

from . import doge


@doge.bot.on(CallbackQuery(data=compile(b"hide_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if path.exists("./userbot/hide.txt"):
        jsondata = load(open("./userbot/hide.txt"))
        try:
            reply_pop_up_alert = jsondata[f"{timestamp}"]["text"]
        except KeyError:
            reply_pop_up_alert = "🚨 Bu mesaj artık Doge sunucusunda yok."
    else:
        reply_pop_up_alert = "🚨 Bu mesaj artık Doge sunucusunda yok."
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
