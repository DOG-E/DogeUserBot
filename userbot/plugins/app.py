# Credits: cHAuHaN - t.me/amnd33p
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from bs4 import BeautifulSoup
from requests import get

from . import doge, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="app ([\s\S]*)",
    command=("app", plugin_category),
    info={
        "h": "PlayStore'da herhangi bir uygulama arayın",
        "d": "Uygulamayı PlayStore'da arar, bağlantı verir ve ayrıntılarını getirir",
        "u": "{tr}app <isim>",
    },
)
async def app_search(event):
    "PlayStore'da herhangi bir uygulama arayın"
    app_name = event.pattern_match.group(1)
    event = await eor(event, "`Arıyorum...`")
    try:
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = get("https://play.google.com/store/search?q=" + final_name + "&c=apps")
        str(page.status_code)
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Geliştirici:</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Puanı:</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Özellikleri:</code> <a href='"
            + app_link
            + "'>Play Store'dan bak</a>"
        )
        await event.edit(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await event.edit(
            "`Herhangi bir şey bulamadım. Lütfen geçerli uygulama adı girin!`"
        )
    except Exception as err:
        await event.edit("**Hata:** `" + str(err) + "`")
