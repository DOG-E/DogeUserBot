# Credits: TeamUltroid - github.com/teamultroid
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# Callback:
# lang_menu
# set_(.*)
# ================================================================
from re import compile

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery
from telethon.utils import get_display_name
from . import (
    check_owner,
    doge,
    get_back_button,
    lan,
    lngs,
    logging,
    mention,
    sgvar,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


@doge.tgbot.on(CallbackQuery(data=compile(r"lang_menu")))
@check_owner
async def setlang(event):
    languages = lngs()
    dogelangs = [
        Button.inline(
            f"{languages[dogelang]['natively']}",
            data=f"set_{dogelang}",
        )
        for dogelang in languages
    ]
    buttons = list(zip(dogelangs[::2], dogelangs[1::2]))
    if len(dogelangs) % 2 == 1:
        buttons.append((dogelangs[-1],))
    buttons.append([Button.inline(f"🐾 {lan('btnmenu')}", data="mainmenu")])
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n{lan('menutext').format(mention)}\
        \n\
        \n🌍 {lan('doges_languages')}:**",
        buttons=buttons,
        link_preview=False,
    )


@doge.tgbot.on(CallbackQuery(data=compile(b"set_(.*)")))
@check_owner
async def setthelang(event):
    lang = event.data_match.group(1).decode("UTF-8")
    languages = lngs()
    sgvar("DOGELANG", lang)
    await event.edit(
        lan("changed_dogelang").format(languages[lang]["natively"]),
        buttons=get_back_button("lang_menu"),
    )
