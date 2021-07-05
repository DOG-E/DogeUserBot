# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import nekos

from dogebot import doge

from ..core.managers import edit_or_reply

plugin_category = "fun"


@doge.ub(
    pattern="tcat$",
    command=("tcat", plugin_category),
    info={
        "header": "Some random cat facial text art",
        "usage": "{tr}tcat",
    },
)
async def hmm(cat):
    "Some random cat facial text art"
    reactdog = nekos.textcat()
    await edit_or_reply(cat, reactdog)


@doge.ub(
    pattern="why$",
    command=("why", plugin_category),
    info={
        "header": "Sends you some random Funny questions",
        "usage": "{tr}why",
    },
)
async def hmm(dog):
    "Some random Funny questions"
    whydog = nekos.why()
    await edit_or_reply(dog, whydog)


@doge.ub(
    pattern="fact$",
    command=("fact", plugin_category),
    info={
        "header": "Sends you some random facts",
        "usage": "{tr}fact",
    },
)
async def hmm(dog):
    "Some random facts"
    factdog = nekos.fact()
    await edit_or_reply(dog, factdog)
