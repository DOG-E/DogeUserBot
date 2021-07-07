import nekos

from userbot import doge

from ..core.managers import edit_or_reply

plugin_category = "fun"


@doge.bot_cmd(
    pattern="tcat$",
    command=("tcat", plugin_category),
    info={
        "header": "Some random cat facial text art",
        "usage": "{tr}tcat",
    },
)
async def hmm(cat):
    "Some random cat facial text art"
    reactcat = nekos.textcat()
    await edit_or_reply(cat, reactcat)


@doge.bot_cmd(
    pattern="why$",
    command=("why", plugin_category),
    info={
        "header": "Sends you some random Funny questions",
        "usage": "{tr}why",
    },
)
async def hmm(dog):
    "Some random Funny questions"
    whydoge = nekos.why()
    await edit_or_reply(dog, whydoge)


@doge.bot_cmd(
    pattern="fact$",
    command=("fact", plugin_category),
    info={
        "header": "Sends you some random facts",
        "usage": "{tr}fact",
    },
)
async def hmm(dog):
    "Some random facts"
    factdoge = nekos.fact()
    await edit_or_reply(dog, factdoge)
