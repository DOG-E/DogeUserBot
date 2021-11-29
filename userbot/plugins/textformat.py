# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, edl, eor, parse_pre

plugin_category = "tool"


@doge.bot_cmd(
    pattern="upper(?: |$)([\s\S]*)",
    command=("upper", plugin_category),
    info={
        "h": "Text operation change to upper text",
        "u": "{tr}upper <input text /reply to text>",
        "e": "{tr}upper Reply to valid text or give valid text as input",
    },
)
async def some(event):
    """Text Format upper"""
    intxt = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not intxt and reply:
        intxt = reply.text
    if not intxt:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid text or give text as input...you moron!!**"
        )
    mystring = intxt.upper()
    await eor(event, mystring)


@doge.bot_cmd(
    pattern="lower(?: |$)([\s\S]*)",
    command=("lower", plugin_category),
    info={
        "h": "Text operation change to lower text",
        "u": "{tr}lower <input text /reply to text>",
        "e": "{tr}lower Reply to valid text or give valid text as input",
    },
)
async def good(event):
    """Text Format lower"""
    intxt = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not intxt and reply:
        intxt = reply.text
    if not intxt:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid text or give text as input...you moron!!**"
        )
    mystring = intxt.lower()
    await eor(event, mystring)


@doge.bot_cmd(
    pattern="title(?: |$)([\s\S]*)",
    command=("title", plugin_category),
    info={
        "h": "Text operation change to title text",
        "u": "{tr}title <input text /reply to text>",
        "e": "{tr}title Reply to valid text or give valid text as input",
    },
)
async def stuff(event):
    """Text Format title"""
    intxt = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not intxt and reply:
        intxt = reply.text
    if not intxt:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid text or give text as input...you moron!!**"
        )
    mystring = intxt.title()
    await eor(event, mystring)


@doge.bot_cmd(
    pattern="(|r)camel(?: |$)([\s\S]*)",
    command=("camel", plugin_category),
    info={
        "h": "Text operation change to camel text",
        "u": [
            "{tr}camel <input text /reply to text>",
            "{tr}rcamel <input text /reply to text>",
        ],
        "e": [
            "{tr}camel Reply to valid text or give valid text as input",
            "{tr}rcamel Reply to valid text or give valid text as input",
        ],
    },
)
async def here(event):
    """Text Format camel"""
    cmd = event.pattern_match.group(1).lower()
    intxt = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not intxt and reply:
        intxt = reply.text
    if not intxt:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid text or give text as input...you moron!!**"
        )
    if cmd == "r":
        shib = list(intxt.lower())[::2]
        dog = list(intxt.upper())[1::2]
    else:
        shib = list(intxt.upper())[::2]
        dog = list(intxt.lower())[1::2]
    mystring = "".join(f"{i}{j}" for i, j in zip(shib, dog))
    await eor(event, mystring)


@doge.bot_cmd(
    pattern="noformat$",
    command=("noformat", plugin_category),
    info={
        "h": "To get replied message without markdown formating.",
        "u": "{tr}noformat <reply>",
    },
)
async def _(event):
    "Replied message without markdown format."
    reply = await event.get_reply_message()
    if not reply or not reply.text:
        return await edl(
            event, "__Reply to text message to get text without markdown formating.__"
        )
    await eor(event, reply.text, parse_mode=parse_pre)
