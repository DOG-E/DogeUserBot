# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from html_telegraph_poster import TelegraphPoster

from ..core.session import doge
from ..sql_helper.globals import gvar
from ..sql_helper.global_msg import gmsg
from ..helpers.resources.constants import DOGEAFK


CMSG = {}
MSG = {"AFK": f"{DOGEAFK}"}
for msg in ["AFK"]:
    delmsg = gmsg(msg)
    if delmsg == False:
        CMSG[msg] = MSG[msg]
    else:
        if delmsg.startswith("MEDIA_"):
            md = int(delmsg.split("MEDIA_")[1])
            md = doge.get_messages(gvar("PLUGIN_CHANNEL"), ids=md)
            CMSG[msg] = md
        else:
            CMSG[msg] = delmsg


def media_type(message):
    if message and message.photo:
        return "Photo"
    if message and message.audio:
        return "Audio"
    if message and message.voice:
        return "Voice"
    if message and message.video_note:
        return "Round Video"
    if message and message.gif:
        return "Gif"
    if message and message.sticker:
        return "Sticker"
    if message and message.video:
        return "Video"
    if message and message.document:
        return "Document"
    return None


async def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    post_client.create_api_token((gvar("TELEGRAPH_SHORT_NAME") or "@DogeUserBot"))
    post_page = post_client.post(
        title=page_title,
        author=(gvar("TELEGRAPH_SHORT_NAME") or "@DogeUserBot"),
        author_url="https://t.me/DogeUserBot",
        text=html_format_content,
    )
    return post_page["url"]
