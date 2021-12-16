# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from re import compile

from telethon import Button
from telethon.events import CallbackQuery

from . import Config, Heroku, check_owner, doge, get_back_button, mention

plugin_category = "bot"


@doge.bot.on(CallbackQuery(data=compile(b"langmenu")))
@check_owner
async def setlang(event):
    langs = [
        Button.inline(
            "🇬🇧 Eɴɢʟɪsʜ",
            data="setlang_en",
        ),
        Button.inline(
            "🐾 Mᴇɴᴜ",
            data="mainmenu"
        ),
    ]
    langs.append([])
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {mention}\n\
        \n🌍 Mᴇᴠᴄᴜᴛ Dɪʟʟᴇʀ:**",
        buttons=langs,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"setlang_en")))
@check_owner
async def setlang_en(event):
    if Config.HEROKU_API_KEY is None:
        return await event.edit(
            "🚨 `HEROKU_API_KEY` değişken ayarınız eksik. Heroku'da gerekli değişkeni ayarlayın.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await event.edit(
            "🚨 `HEROKU_APP_NAME` değişken ayarınız eksik. Heroku'da gerekli değişkeni ayarlayın.",
        )
    hvar = app.config()
    await event.edit(
        "**⏳ Biraz bekleyin,\
        \n🇬🇧 Dili İngilizce'ye ayarlıyorum...\n\
        \n⏳ Just a moment,\
        \n🇬🇧 Language is setting to English...**",
        buttons=get_back_button("langmenu"),
    )
    hvar["UPSTREAM_REPO_BRANCH"] = "DOGE-EN"
