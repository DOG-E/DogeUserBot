# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import requests
from validators.url import url

from dogebot import doge

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@doge.doge_cmd(
    pattern="dns(?:\s|$)([\s\S]*)",
    command=("dns", plugin_category),
    info={
        "header": "To get Domain Name System(dns) of the given link.",
        "usage": "{tr}dns <url/reply to url>",
        "examples": "{tr}dns google.com",
    },
)
async def _(event):
    "To get Domain Name System(dns) of the given link."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        dogestr = "http://" + input_str
        check = url(dogestr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    sample_url = f"https://da.gd/dns/{input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(event, f"DNS records of {input_str} are \n{response_api}")
    else:
        await edit_or_reply(
            event, f"__I can't seem to find `{input_str}` on the internet__"
        )


@doge.doge_cmd(
    pattern="short(?:\s|$)([\s\S]*)",
    command=("short", plugin_category),
    info={
        "header": "To short the given url.",
        "usage": "{tr}short <url/reply to url>",
        "examples": "{tr}short https://github.com/DOG-E/DogeUserBot",
    },
)
async def _(event):
    "shortens the given link"
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        dogestr = f"http://" + input_str
        check = url(dogestr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    sample_url = f"https://da.gd/s?url={input_str}"
    response_api = requests.get(sample_url).text
    if response_api:
        await edit_or_reply(
            event, f"Generated {response_api} for {input_str}.", link_preview=False
        )
    else:
        await edit_or_reply(event, "`Something is wrong, please try again later.`")


@doge.doge_cmd(
    pattern="unshort(?:\s|$)([\s\S]*)",
    command=("unshort", plugin_category),
    info={
        "header": "To unshort the given dagb shorten url.",
        "usage": "{tr}unshort <url/reply to url>",
        "examples": "{tr}unshort https://da.gd/u8WuL",
    },
)
async def _(event):
    "To unshort the given dagb shorten url."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        dogestr = "http://" + input_str
        check = url(dogestr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await edit_or_reply(
            event,
            f"Input URL: {input_str}\nReDirected URL: {r.headers['Location']}",
            link_preview=False,
        )
    else:
        await edit_or_reply(
            event,
            "Input URL {} returned status_code {}".format(input_str, r.status_code),
        )


# By Priyam Kalra
@doge.doge_cmd(
    pattern="hl(?:\s|$)([\s\S]*)",
    command=("hl", plugin_category),
    info={
        "header": "To hide the url with white spaces using hyperlink.",
        "usage": "{tr}hl <url/reply to url>",
        "examples": "{tr}hl https://da.gd/u8WuL",
    },
)
async def _(event):
    "To hide the url with white spaces using hyperlink."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "`Either reply to link or give link as input to get data`", 5
        )
    check = url(input_str)
    if not check:
        dogestr = "http://" + input_str
        check = url(dogestr)
    if not check:
        return await edit_delete(event, "`the given link is not supported`", 5)
    await edit_or_reply(event, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input_str + ")")
