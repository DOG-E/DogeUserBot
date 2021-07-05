# Created: @jisan7509 (@jisan09)
#
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from dogebot import doge

from ..core.managers import edit_or_reply
from ..helpers import fonts as emojify

plugin_category = "fun"


@doge.ub(
    pattern="emoji(?:\s|$)([\s\S]*)",
    command=("emoji", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with some default emojis.",
        "usage": "{tr}emoji <text>",
        "examples": ["{tr}emoji DogeUserBot"],
    },
)
async def default(event):
    "To get emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        await edit_or_reply(
            event, "__What am I Supposed to do with this idiot, Give me a text.__"
        )
        return
    result = ""
    for a in args:
        a = a.lower()
        if a in emojify.basemojitext:
            char = emojify.emojitext[emojify.basemojitext.index(a)]
            result += char
        else:
            result += a
    await edit_or_reply(event, result)


@doge.ub(
    pattern="cmoji(?:\s|$)([\s\S]*)",
    command=("cmoji", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with your custom emoji.",
        "usage": "{tr}cmoji <emoji> <text>",
        "examples": ["{tr}cmoji 🐾 DogeUserBot"],
    },
)
async def custom(event):
    "To get custom emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        return await edit_or_reply(
            event, "__What am I Supposed to do with this idiot, Give me a text.__"
        )
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "🐾"
    result = ""
    for a in arg:
        a = a.lower()
        if a in emojify.basemojitext:
            char = emojify.customojitext[emojify.basemojitext.index(a)].format(e=emoji)
            result += char
        else:
            result += a
    await edit_or_reply(event, result)
