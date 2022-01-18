# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from heroku3 import from_key
from telethon import Button
from telethon.events import CallbackQuery
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from . import HEROKU_API_KEY, HEROKU_APP_NAME, check_owner, compile, doge, get_back_button, gvar

disable_warnings(InsecureRequestWarning)
if HEROKU_API_KEY:
    heroku = from_key(HEROKU_API_KEY)
    app = heroku.app(HEROKU_APP_NAME)


@doge.bot.on(CallbackQuery(data=compile(b"langmenu")))
@check_owner
async def setlang(event: CallbackQuery):
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🌍 Mᴇᴠᴄᴜᴛ Dɪʟʟᴇʀ:**",
        buttons=Button.inline("🇬🇧 Eɴɢʟɪsʜ", data="setlang_en"),
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"setlang_(.*)")))
@check_owner
async def setlang_en(event: CallbackQuery):
    lang = event.pattern_match.group(1)
    if HEROKU_API_KEY is None:
        return await event.edit(
            "🚨 `HEROKU_API_KEY` değişken ayarınız eksik. Heroku'da gerekli değişkeni ayarlayın.",
            buttons=get_back_button("langmenu"),
        )
    if HEROKU_APP_NAME is None:
        return await event.edit(
            "🚨 `HEROKU_APP_NAME` değişken ayarınız eksik. Heroku'da gerekli değişkeni ayarlayın.",
            buttons=get_back_button("langmenu"),
        )
    await event.edit(
        "**⏳ Biraz bekleyin,\
        \n🇬🇧 Dili İngilizce'ye ayarlıyorum...\n\
        \n⏳ Just a moment,\
        \n🇬🇧 Language is setting to English...**",
    )
    if lang == "en":
        app.config()["UPSTREAM_REPO_BRANCH"] = "DOGE-EN"
