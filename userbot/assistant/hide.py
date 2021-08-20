from json import load
from os import path
from re import compile

from telethon.events import CallbackQuery

from . import doge


@doge.tgbot.on(CallbackQuery(data=compile(b"hide_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if path.exists("./userbot/hide.txt"):
        jsondata = load(open("./userbot/hide.txt"))
        try:
            reply_pop_up_alert = jsondata[f"{timestamp}"]["text"]
        except KeyError:
            reply_pop_up_alert = "🚨 This message no longer exists in Doge server."
    else:
        reply_pop_up_alert = "🚨 This message no longer exists."
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
