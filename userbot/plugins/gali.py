"""
Created By @Jisan7509
GF created by @KshitijGagan
"""

from asyncio import sleep

from . import doge, eor

plugin_category = "hub"


@doge.bot_cmd(
    pattern="gf$",
    command=("gf", plugin_category),
    info={
        "header": "bad animation, try yourself ",
        "usage": "{tr}gf",
    },
)
async def kakashi(event):
    "Bad stuff"
    animation_interval = 5
    animation_ttl = range(21)
    kakashi = await eor(event, "BSDK tera gf h na ek ...!")
    animation_chars = [
        "`Ruk jaa , Abhi teri GF ko Fuck karta hu `",
        "`Making your Gf warm 🔥`",
        "`Pressing her boobs 🤚😘`",
        "`Stimulating her pussy🖕`",
        "`Fingering her pussy 💧😍👅 `",
        "`Asking her to taste my DICK🍌`",
        "`Requested accepted😻💋, Ready to taste my DICK🍌`",
        "`Getting her ready to fuck 👀`",
        "`Your GF Is Ready To Fuck`",
        "`Fucking Your GF😈😈\n\n\nYour GF's Pussy Get Red\nTrying new SEX position to make her Squirt\n\nAlmost Done. 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Pussy Get White\nShe squirted like a shower💧💦👅\n\nAlmost Done..\n\nFucked Percentage... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Pussy Get Red\nDoing Extreme SEX with her👄\n\nAlmost Done...\n\nFucked Percentage... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Pussy Get Red\nWarming her Ass🍑 to Fuck!🍑🍑\n\nAlmost Done....\n\nFucked Percentage... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's ASS🍑 Get Red\nInserted my Penis🍌 in her ASS🍑\n\nAlmost Done.....\n\nFucked Percentage... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's ASS🍑 Get Red\ndoing extreme sex with her\n\nAlmost Done......\n\nFucked Percentage... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Boobs🤚😘 are Awesome\nPressing her tight Nipples🤚👀\n\nAlmost Done.......\n\nFucked Percentage... 84%\n███████████████████▒▒▒▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Lips Get Horny\nDoing French Kiss with your GF👄💋\n\nAlmost Done........\n\nFucked Percentage... 89%\n██████████████████████▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Boobs🤚😘 are Awesome\nI am getting ready to cum in her Mouth👄\n\nAlmost Done.......\n\nFucked Percentage... 90%\n██████████████████████▒▒▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's Boobs🤚😘 are Awesome\nFinally, I have cummed in her Mouth👅👄\n\nAlmost Done.......\n\nFucked Percentage... 96%\n████████████████████████▒ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's is Awesome\nShe is Licking my Dick🍌 in the Awesome Way✊🤛🤛👅👄\n\nAlmost Done.......\n\nFucked Percentage... 100%\n█████████████████████████ `",
        "`Fucking Your GF😈😈\n\n\nYour GF's ASS🍑 Get Red\nCummed On her Mouth👅👄\n\nYour GF got Pleasure\n\nResult: Now I Have 1 More SEX Partner 👍👍`",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await kakashi.edit(animation_chars[i % 21])


@doge.bot_cmd(
    pattern="fk ([\s\S]*)",
    command=("fk", plugin_category),
    info={
        "header": "bad animation, try yourself ",
        "usage": "{tr}fk <text>",
    },
)
async def kakashi(event):
    "Bad stuff"
    name = event.pattern_match.group(1)
    animation_interval = 3
    animation_ttl = range(11)
    kakashi = await eor(event, "👁👁")
    animation_chars = [
        f"👁👁\n  👄  =====> Abey {name} Chutiya",
        f"👁👁\n  👅  =====> Abey {name} Gay",
        f"👁👁\n  💋  =====> Abey {name} Lodu",
        f"👁👁\n  👄  =====> Abey {name} Gandu",
        f"👁👁\n  💋  =====> Abey {name} Randi",
        f"👁👁\n  👄  =====> Abey {name} Betichod",
        f"👁👁\n  👅  =====> Abey {name} Behenchod",
        f"👁👁\n  💋  =====> Abey {name} NaMard",
        f"👁👁\n  👄  =====> Abey {name} Lavde",
        f"👁👁\n  👅  =====> Abey {name} Bhosdk",
        f"👁👁\n  👄  =====> Hi {name} Mc, How Are You Bsdk...",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await kakashi.edit(animation_chars[i % 11])


@doge.bot_cmd(
    pattern="chod$",
    command=("chod", plugin_category),
    info={
        "header": "bad animation, try yourself ",
        "usage": "{tr}chod",
    },
)
async def kakashi(event):
    "Bad stuff"
    animation_interval = 5
    animation_ttl = range(11)
    kakashi = await eor(event, "1 2 3..Searching Randi..")
    animation_chars = [
        "`Randi Founded`",
        "`Your Mom Is Going To Fuck`",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 84%\n█████████████████████▒▒▒▒ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nAlmost Done...\n\nFucked Percentage... 100%\n█████████████████████████ `",
        "`Fucking Your Mom\n\n\nYour Mom's Pussy Get Red\nCumming On Pussy\n\nYour mom get Pregnant\n\nResult: Now You Have 1 More Younger Brother `",
    ]
    for i in animation_ttl:
        await sleep(animation_interval)
        await kakashi.edit(animation_chars[i % 11])


@doge.bot_cmd(
    pattern="kis$",
    command=("kis", plugin_category),
    info={
        "header": "shows you fun kissing animation",
        "usage": "{tr}kis",
    },
)
async def _(event):
    "fun animation"
    dogevent = await eor(event, "`kiss`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵💋👰"]
    for i in animation_ttl:
        await sleep(animation_interval)
        await dogevent.edit(animation_chars[i % 4])


@doge.bot_cmd(
    pattern="fuk$",
    command=("fuk", plugin_category),
    info={
        "header": "shows you fun fucking animation",
        "usage": "{tr}fuk",
    },
)
async def _(event):
    "fun animation"
    dogevent = await eor(event, "`fuking....`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
    for i in animation_ttl:
        await sleep(animation_interval)
        await dogevent.edit(animation_chars[i % 4])


@doge.bot_cmd(
    pattern="fuuk$",
    command=("fuuk", plugin_category),
    info={
        "header": "shows you fun fucking animation",
        "usage": "{tr}fuuk",
    },
)
async def _(event):
    "fun animation"
    dogevent = await eor(event, "`fuuking....`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🍆       🍑", "🍆     🍑", "🍆  🍑", "🍆🍑💦"]
    for i in animation_ttl:
        await sleep(animation_interval)
        await dogevent.edit(animation_chars[i % 4])


@doge.bot_cmd(
    pattern="sex$",
    command=("sex", plugin_category),
    info={
        "header": "shows you fun sex animation",
        "usage": "{tr}sex",
    },
)
async def _(event):
    "fun animation"
    dogevent = await eor(event, "`sex`")
    animation_interval = 0.2
    animation_ttl = range(100)
    animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵👼👰"]
    for i in animation_ttl:
        await sleep(animation_interval)
        await dogevent.edit(animation_chars[i % 4])
