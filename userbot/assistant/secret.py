from json import load
from os import path
from re import compile

from telethon.events import CallbackQuery

from . import doge


@doge.tgbot.on(CallbackQuery(data=compile(b"s_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if path.exists("./userbot/secrets.txt"):
        jsondata = load(open("./userbot/secrets.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, doge.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "🐶 Doɢᴇ UsᴇʀBoᴛ\
                    \n\n🐾 Why were you looking at this,\
                    \ngo and do your own thing."
        except KeyError:
            reply_pop_up_alert = "🚨 This message no longer exists in Doge server."
    else:
        reply_pop_up_alert = "🚨 This message no longer exists."
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
