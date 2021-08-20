"""Get a Image Post from Reddit"""
# 👍 https://github.com/D3vd for his awesome API
#
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @DeletedUser420]
# All rights reserved.


from requests import get

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    _dogeutils,
    age_verification,
    doge,
    edl,
    logging,
    reply_id,
)

plugin_category = "fun"
LOGS = logging.getLogger(__name__)

API = "https://meme-api.herokuapp.com/gimme"


@doge.bot_cmd(
    pattern="reddit(?:\s|$)([\s\S]*)",
    command=("reddit", plugin_category),
    info={
        "header": "get a random reddit post.",
        "usage": "{tr}reddit <subreddit>",
        "examples": "{tr}reddit dankmemes",
    },
)
async def reddit_fetch(event):
    """Random reddit post"""
    reply_to = await reply_id(event)
    sub_r = event.pattern_match.group(1)
    subreddit_api = f"{API}/{sub_r}" if sub_r else API
    try:
        cn = get(subreddit_api)
        r = cn.json()
    except ValueError:
        return await edl(event, "Value error!.")

    if "code" in r:
        if BOTLOG:
            code = r["code"]
            code_message = r["message"]
            await event.client.send_message(
                BOTLOG_CHATID, f"**Error Code: {code}**\n`{code_message}`"
            )
            await edl(event, f"**Error Code: {code}**\n`{code_message}`")
    else:
        if "url" not in r:
            return await edl(
                event,
                "Coudn't Find a post with Image, Please Try Again",
            )

        postlink = r["postLink"]
        subreddit = r["subreddit"]
        title = r["title"]
        media_url = r["url"]
        author = r["author"]
        upvote = r["ups"]
        captionx = f"**{title}**\n"
        captionx += f"`Posted by u/{author}`\n"
        captionx += f"↕️ `{upvote}`\n"
        if r["spoiler"]:
            captionx += "⚠️ Post marked as SPOILER\n"
        if r["nsfw"]:
            captionx += "🔞 Post marked Adult \n"
            if await age_verification(event, reply_to):
                return

        await event.delete()
        captionx += f"Source: [r/{subreddit}]({postlink})"
        teledoge = await event.client.send_file(
            event.chat_id, media_url, caption=captionx, reply_to=reply_to
        )
        if media_url.endswith(".gif"):
            await _dogeutils.unsavegif(event, teledoge)
