# Credits: cHAuHaN - t.me/amnd33p
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from bs4 import BeautifulSoup
from requests import get

from . import ALIVE_NAME, doge, eor, lan, tr

plugin_category = "tool"


@doge.bot_cmd(
    pattern="app ([\s\S]*)",
    command=("app", plugin_category),
    info={
        "header": lan("app1"),
        "description": lan("app2"),
        "usage": f"{tr}app {lan('app3')}",
    },
)
async def app_search(event):
    lan("app4")
    app_name = event.pattern_match.group(1)
    event = await eor(event, lan("app5"))
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
            f"\n\n<code>{lan('app6')}:</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += f"\n<code>{lan('app7')}:</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            f"\n<code>{lan('app8')}:</code> <a href='" + app_link + f"'>{lan('app9')}</a>"
        )
        app_details += f"\n\n===> {ALIVE_NAME} <==="
        await event.edit(app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await event.edit(lan("app10"))
    except Exception as err:
        await event.edit(f"{lan('app11')}: " + str(err))
