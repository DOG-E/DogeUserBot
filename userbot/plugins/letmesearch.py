# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from requests import get

from . import HEROKU_APP_NAME, doge, edl, eor

plugin_category = "misc"


@doge.bot_cmd(
    pattern="lmg ([\s\S]*)",
    command=("lmg", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}lmg <Query>",
    },
)
async def _(event):
    "Searches the given query in Google and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = (
        f"https://da.gd/s?url=http://google.com/search?q={input_str.replace(' ', '+')}"
    )
    response_api = get(sample_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **Google** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)


@doge.bot_cmd(
    pattern="lmy ([\s\S]*)",
    command=("lmy", plugin_category),
    info={
        "header": "Searches the given query in youtube and shows you the link of that query.",
        "usage": "{tr}lmy <Query>",
    },
)
async def _(event):
    "Searches the given query in youtube and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://www.youtube.com/results?search_query={input_str.replace(' ', '+')}"
    response_api = get(sample_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **youtube** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)


@doge.bot_cmd(
    pattern="ddg ([\s\S]*)",
    command=("ddg", plugin_category),
    info={
        "header": "Searches the given query in Duck duck go and shows you the link of that query.",
        "usage": "{tr}ddg <Query>",
    },
)
async def _(event):
    "Searches the given query in Duck duck go and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://duckduckgo.com/?q={input_str.replace(' ', '+')}&t=h_&ia=about"
    response_api = get(sample_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **duckduckgo** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)


@doge.bot_cmd(
    pattern="lmvar ([\s\S]*)",
    command=("lmvar", plugin_category),
    info={
        "header": "Searches the given app name in heroku and show that app vars page link .",
        "usage": ["{tr}lmvar <app name>", "{tr}lmvar"],
    },
)
async def lmvar(event):
    "Searches the given app name in heroku and show that app vars page link ."
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = HEROKU_APP_NAME
        sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/settings"
    else:
        sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/settings"
    response_api = get(sample_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **var** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)


@doge.bot_cmd(
    pattern="lmdyno ([\s\S]*)",
    command=("lmdyno", plugin_category),
    info={
        "header": "Searches the given app name in heroku and shows you dyno page link of that app.",
        "usage": ["{tr}lmdyno <query>", "{tr}lmdyno"],
    },
)
async def lmdyno(event):
    "Searches the given app name in heroku and shows you dyno page link of that app."
    input_str = event.pattern_match.group(1)
    billings_url = "https://da.gd/s?url=https://dashboard.heroku.com/account/billing"
    if not input_str:
        input_str = HEROKU_APP_NAME
        sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str}/resources"
    else:
        sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str}/resources"
    response_api = get(sample_url).text
    respons_api = get(billings_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **dyno** that for you:\
                \n👉 [{input_str}]({response_api.rstrip()})\
                \n👉 [Dyno hours]({respons_api.rstrip()})\
                \n`Thank me later 😉`"
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)


@doge.bot_cmd(
    pattern="archive ([\s\S]*)",
    command=("archive", plugin_category),
    info={
        "header": "Searches the given query in web archive and shows you the link of that query.",
        "usage": "{tr}archive <Query>",
    },
)
async def _(event):
    "Searches the given query in web archive and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://web.archive.org/web/*/{input_str.replace(' ', '+')}"
    response_api = get(sample_url).text
    event = await eor(event, "`Searching...`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me run your link on wayback machine that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edl(event, "`Something went wrong. Please try again later.`", 5)
