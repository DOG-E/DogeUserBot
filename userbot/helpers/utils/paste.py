# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import dumps

from requests import post
from telegraph import Telegraph

from ...Config import Config
from ...core.logger import logging
from ..tools import post_to_telegraph

LOGS = logging.getLogger("DogeUserBot")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}
telegraph = Telegraph()
r = telegraph.create_account(
    short_name=Config.TELEGRAPH_SHORT_NAME, author_url="https://t.me/DogeUserBot"
)
auth_url = r["auth_url"]


async def t_paste(msg, title=None):
    """
    To Paste the given message/text/code to Telegraph
    """
    c = title if title else "🐶 Doge UserBot 🐾"
    try:
        t = telegraph.create_page(title=c, content=[f"{msg}"])
        response = t["url"]
        try:
            from ...core.session import doge

            await doge.send_message(
                Config.BOTLOG_CHATID,
                f"Created new Telegraph account {auth_url} for the current session.\n\n**Don't give this URL to anyone, even if they say they are from Telegram!**",
            )
        except Exception as e:
            LOGS.info(str(e))
        return response
    except Exception:
        try:
            response = await post_to_telegraph(c, msg)
            return response
        except Exception as e:
            return {"error": str(e)}


async def p_paste(message, extension=None):
    """
    To Paste the given message/text/code to paste.pelkum.dev
    """
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = post(url=siteurl, data=dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        try:
            from ...core.session import doge

            await doge.send_message(
                Config.BOTLOG_CHATID,
                f"**You have created a new paste in pasty bin.**\n\nLink to pasty is [HERE]({purl}).\n\nYou can delete that paste by using this token `{response['deletionToken']}`",
            )
        except Exception as e:
            LOGS.info(str(e))
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    er = "pasty.lus.pm"
    return {"error": f"`🚨 Unable to reach {er}!`"}


async def s_paste(message, extension="txt"):
    """
    To Paste the given message/text/code to spaceb.in
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = post(siteurl, data={"content": message, "extension": extension})
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    er = "spacebin"
    return {"error": f"`🚨 Unable to reach {er}!`"}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    try:
        response = post(url=siteurl, data=dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"nekobin.com/{response['result']['key']}.{extension}"
            if extension
            else f"nekobin.com/{response['result']['key']}"
        )
        return {
            "url": purl,
            "raw": f"nekobin.com/raw/{response['result']['key']}",
            "bin": "Neko",
        }
    er = "nekobin"
    return {"error": f"`🚨 Unable to reach {er}!`"}


async def d_paste(message, extension=None):
    """
    To Paste the given message/text/code to dogbin
    """
    siteurl = "https://catbin.up.railway.app/documents"
    data = {"content": message}
    try:
        response = post(url=siteurl, data=dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://catbin.up.railway.app/{response['key']}.{extension}"
            if extension
            else f"https://catbin.up.railway.app/{response['key']}"
        )
        return {
            "url": purl,
            "raw": f"https://catbin.up.railway.app/raw/{response['key']}",
            "bin": "Dog",
        }
    er = "catbin"
    return {"error": f"`🚨 Unable to reach {er}!`"}


async def pastetext(text_to_print, pastetype=None, extension=None, title=None):
    response = {"error": "`🚨 Something went wrong!`"}
    if pastetype is not None:
        if pastetype == "p":
            response = await p_paste(text_to_print, extension)
        elif pastetype == "t" and title:
            response = await t_paste(text_to_print, title)
        elif pastetype == "t":
            response = await t_paste(text_to_print)
        elif pastetype == "s" and extension:
            response = await s_paste(text_to_print, extension)
        elif pastetype == "s":
            response = await s_paste(text_to_print)
        elif pastetype == "d":
            response = await d_paste(text_to_print, extension)
        elif pastetype == "n":
            response = await n_paste(text_to_print, extension)
    if "error" in response:
        if title:
            response = await t_paste(text_to_print, title)
        else:
            response = await t_paste(text_to_print)
    if "error" in response:
        response = await p_paste(text_to_print, extension)
    if "error" in response:
        response = await n_paste(text_to_print, extension)
    if "error" in response:
        if extension:
            response = await s_paste(text_to_print, extension)
        else:
            response = await s_paste(text_to_print)
    if "error" in response:
        response = await d_paste(text_to_print, extension)
    return response
