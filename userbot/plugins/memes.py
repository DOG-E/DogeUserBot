# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
# catUserbot module for having some fun with people.
from asyncio import sleep
from random import choice, randint
from re import sub

from cowpy.cow import COWACTERS, get_cow
from nekos import fact, textcat, why
from requests import get
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins, MessageEntityMentionName

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    _dogeutils,
    doge,
    dogememes,
    edl,
    eor,
    mememaker,
    mention,
    parse_pre,
    reply_id,
)

plugin_category = "fun"


async def get_user(event):
    # Get the user from argument or replied message.
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None
    return replied_user


@doge.bot_cmd(
    pattern="(\w+)say ([\s\S]*)",
    command=("cowsay", plugin_category),
    info={
        "header": "A fun art plugin.",
        "types": [
            "default",
            "beavis",
            "bongcow",
            "budfrogs",
            "bunny",
            "cheese",
            "cower",
            "daemon",
            "dragonandcow",
            "eyes",
            "flamingsheep",
            "ghostbusters",
            "headincow",
            "hellokitty",
            "kiss",
            "kitty",
            "koala",
            "kosh",
            "lukekoala",
            "mechandcow",
            "meow",
            "milk",
            "moofasa",
            "moose",
            "mutilated",
            "ren",
            "satanic",
            "sheep",
            "skeleton",
            "small",
            "sodomized",
            "squirrel",
            "stegosaurus",
            "stimpy",
            "supermilker",
            "surgery",
            "telebears",
            "threeeyes",
            "turkey",
            "turtle",
            "tux",
            "udder",
            "vaderkoala",
            "vader",
            "www",
        ],
        "usage": [
            "{tr}cowsay <text>",
            "{tr}<type>say <text>",
        ],
        "examples": [
            "{tr}squirrelsay DogeUserBot",
            "{tr}milksay DogeUserBot",
            "{tr}ghostbustersghostbusterssay DogeUserBot",
        ],
    },
)
async def univsaye(cowmsg):
    "A fun art plugin."
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)
    if arg == "cow":
        arg = "default"
    if arg not in COWACTERS:
        return await edl(cowmsg, "check doge menu to know the correct options.")
    cheese = get_cow(arg)
    cheese = cheese()
    await eor(cowmsg, f"`{cheese.milk(text).replace('`', '´')}`")


@doge.bot_cmd(
    pattern="coin ?([\s\S]*)",
    command=("coin", plugin_category),
    info={
        "header": "Coin flipper.",
        "usage": [
            "{tr}coin <heads/tails>",
            "{tr}coin",
        ],
    },
)
async def _(event):
    "flips a coin."
    r = randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await eor(event, "The coin landed on: **Heads**. \n You were correct.")
        elif input_str == "tails":
            await eor(
                event,
                "The coin landed on: **Heads**. \n You weren't correct, try again ...",
            )
        else:
            await eor(event, "The coin landed on: **Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await eor(event, "The coin landed on: **Tails**. \n You were correct.")
        elif input_str == "heads":
            await eor(
                event,
                "The coin landed on: **Tails**. \n You weren't correct, try again ...",
            )
        else:
            await eor(event, "The coin landed on: **Tails**.")
    else:
        await eor(event, r"¯\_(ツ)_/¯")


@doge.bot_cmd(
    pattern="slap(?:\s|$)([\s\S]*)",
    command=("slap", plugin_category),
    info={
        "header": "To slap a person with random objects !!",
        "usage": "{tr}slap reply/username>",
    },
)
async def who(event):
    "To slap a person with random objects !!"
    replied_user = await get_user(event)
    if replied_user is None:
        return
    caption = await dogememes.slap(replied_user, event, mention)
    try:
        await eor(event, caption)
    except BaseException:
        await eor(
            event, "`Can't slap this person, need to fetch some sticks and stones !!`"
        )


@doge.bot_cmd(
    pattern="(yes|no|maybe|decide)$",
    command=("decide", plugin_category),
    info={
        "header": "To decide something will send gif according to given input or ouput.",
        "usage": [
            "{tr}yes",
            "{tr}no",
            "{tr}maybe",
            "{tr}decide",
        ],
    },
)
async def decide(event):
    "To send random gif associated with yes or no or maybe."
    decision = event.pattern_match.group(1).lower()
    message_id = event.reply_to_msg_id or None
    if decision != "decide":
        r = get(f"https://yesno.wtf/api?force={decision}").json()
    else:
        r = get("https://yesno.wtf/api").json()
    await event.delete()
    teledoge = await event.client.send_message(
        event.chat_id, str(r["answer"]).upper(), reply_to=message_id, file=r["image"]
    )
    await _dogeutils.unsavegif(event, teledoge)


@doge.bot_cmd(
    pattern="shout(?:\s|$)([\s\S]*)",
    command=("shout", plugin_category),
    info={
        "header": "shouts the text in a fun way",
        "usage": [
            "{tr}shout <text>",
        ],
    },
)
async def shout(args):
    "shouts the text in a fun way"
    input_str = args.pattern_match.group(1)
    if not input_str:
        return await edl(args, "__What should i shout?__")
    words = input_str.split()
    msg = ""
    for messagestr in words:
        text = " ".join(messagestr)
        result = [" ".join(text)]
        for pos, symbol in enumerate(text[1:]):
            result.append(symbol + " " + "  " * pos + symbol)
        result = list("\n".join(result))
        result[0] = text[0]
        result = "".join(result)
        msg += "\n" + result
        if len(words) > 1:
            msg += "\n\n----------\n"
    await eor(args, msg, parse_mode=parse_pre)


@doge.bot_cmd(
    pattern="owo ?([\s\S]*)",
    command=("owo", plugin_category),
    info={
        "header": "check yourself.",
        "usage": [
            "{tr}owo <text>",
        ],
    },
)
async def faces(owo):
    "UwU"
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(owo, "` UwU no text given! `")
    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(dogememes.UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(dogememes.UWUS)
    await eor(owo, reply_text)


@doge.bot_cmd(
    pattern="clap(?:\s|$)([\s\S]*)",
    command=("clap", plugin_category),
    info={
        "header": "Praise people!",
        "usage": [
            "{tr}clap <text>",
        ],
    },
)
async def claptext(event):
    "Praise people!"
    textx = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif textx.message:
        query = textx.message
    else:
        return await eor(event, "`Hah, I don't clap pointlessly!`")
    reply_text = "👏 "
    reply_text += query.replace(" ", " 👏 ")
    reply_text += " 👏"
    await eor(event, reply_text)


@doge.bot_cmd(
    pattern="smk(?:\s|$)([\s\S]*)",
    command=("smk", plugin_category),
    info={
        "header": "A shit module for ツ , who cares.",
        "usage": [
            "{tr}smk <text>",
        ],
    },
)
async def smrk(smk):
    "A shit module for ツ , who cares."
    textx = await smk.get_reply_message()
    if smk.pattern_match.group(1):
        message = smk.pattern_match.group(1)
    elif textx.message:
        message = textx.message
    else:
        await eor(smk, "ツ")
        return
    if message == "dele":
        await eor(smk, message + "te the hell" + "ツ")
    else:
        smirk = " ツ"
        reply_text = message + smirk
        await eor(smk, reply_text)


@doge.bot_cmd(
    pattern="f ([\s\S]*)",
    command=("f", plugin_category),
    info={
        "header": "Pay Respects.",
        "usage": [
            "{tr}f <emoji/character>",
        ],
    },
)
async def payf(event):
    "Pay Respects."
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8,
        paytext * 8,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 6,
        paytext * 6,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
        paytext * 2,
    )
    await eor(event, pay)


@doge.bot_cmd(
    pattern="wish(?:\s|$)([\s\S]*)",
    command=("wish", plugin_category),
    info={
        "header": "Shows the chance of your success.",
        "usage": [
            "{tr}wish <reply>",
            "{tr}wish <your wish>",
        ],
    },
)
async def wish_check(event):
    "Shows the chance of your success."
    wishtxt = event.pattern_match.group(1)
    chance = randint(0, 100)
    if wishtxt:
        reslt = f"**Your wish **__{wishtxt}__ **has been cast.** ✨\
              \n\n__Chance of success :__ **{chance}%**"
    elif event.is_reply:
        reslt = f"**Your wish has been cast. **✨\
                  \n\n__Chance of success :__ **{chance}%**"
    else:
        reslt = "What's your Wish? Should I consider you as Idiot by default ? 😜"
    await eor(event, reslt)


@doge.bot_cmd(
    pattern="lfy(?:\s|$)([\s\S]*)",
    command=("lfy", plugin_category),
    info={
        "header": "Let me Google that for you real quick !!",
        "usage": [
            "{tr}lfy <query>",
        ],
    },
)
async def _(event):
    "Let me Google that for you real quick !!"
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "`either reply to text message or give input to search`", 5
        )
    sample_url = f"https://da.gd/s?url=https://lmgtfy.com/?q={input_str.replace(' ', '+')}%26iie=1"
    response_api = get(sample_url).text
    if response_api:
        await eor(event, f"[{input_str}]({response_api.rstrip()})\n`Thank me Later 🙃` ")
    else:
        return await edl(event, "`something is wrong. please try again later.`", 5)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"LMGTFY query `{input_str}` was executed successfully",
        )


@doge.bot_cmd(
    pattern="gbun(?:\s|$)([\s\S]*)",
    command=("gbun", plugin_category),
    info={
        "header": "Fake gban action !!",
        "usage": ["{tr}gbun <reason>", "{tr}gbun"],
    },
)
async def gbun(event):
    "Fake gban action !!"
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n`"
    dogevent = await eor(event, "**Summoning out le Gungnir ❗️⚜️☠️**")
    await sleep(3.5)
    chat = await event.get_input_chat()
    async for _ in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.sender_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.sender_id
        # make meself invulnerable cuz why not xD
        if idd == 1035034432:
            await dogevent.edit(
                "`Wait a second, This is my master!`\n**How dare you threaten to ban my master nigger!**\n\n__Your account has been hacked! Pay 69$ to my master__ [π.$](tg://user?id=1035034432) __to release your account__😏"
            )
        else:
            jnl = (
                "`Warning!! `"
                "[{}](tg://user?id={})"
                "` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n\n`"
                "**user's Name: ** __{}__\n"
                "**ID : ** `{}`\n"
            ).format(firstname, idd, firstname, idd)
            if usname is None:
                jnl += "**Victim Nigga's username: ** `Doesn't own a username!`\n"
            else:
                jnl += "**Victim Nigga's username:** @{}\n".format(usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Reason: **" + gbunm
                jnl += gbunr
            else:
                no_reason = "__Reason: Potential spammer. __"
                jnl += no_reason
            await dogevent.edit(jnl)
    else:
        mention = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\nReason: Potential spammer. `"
        await dogevent.edit(mention)


@doge.bot_cmd(
    pattern="congo$",
    command=("congo", plugin_category),
    info={
        "header": " Congratulate the people..",
        "usage": "{tr}congo",
    },
)
async def _(e):
    "Congratulate the people."
    txt = choice(dogememes.CONGOREACTS)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="shg$",
    command=("shg", plugin_category),
    info={
        "header": "Shrug at it !!",
        "usage": "{tr}shg",
    },
)
async def shrugger(e):
    "Shrug at it !!"
    txt = choice(dogememes.SHGS)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="runs$",
    command=("runs", plugin_category),
    info={
        "header": "Run, run, RUNNN!.",
        "usage": "{tr}runs",
    },
)
async def runner_lol(e):
    "Run, run, RUNNN!"
    txt = choice(dogememes.RUNSREACTS)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="noob$",
    command=("noob", plugin_category),
    info={
        "header": "Whadya want to know? Are you a NOOB?",
        "usage": "{tr}noob",
    },
)
async def metoo(e):
    "Whadya want to know? Are you a NOOB?"
    txt = choice(dogememes.NOOBSTR)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="insult$",
    command=("insult", plugin_category),
    info={
        "header": "insult someone.",
        "usage": "{tr}insult",
    },
)
async def insult(e):
    "insult someone."
    txt = choice(dogememes.INSULT_STRINGS)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="love$",
    command=("love", plugin_category),
    info={
        "header": "Chutiyappa suru",
        "usage": "{tr}love",
    },
)
async def suru(chutiyappa):
    "Chutiyappa suru"
    txt = choice(dogememes.LOVESTR)
    await eor(chutiyappa, txt)


@doge.bot_cmd(
    pattern="dhoka$",
    command=("dhoka", plugin_category),
    info={
        "header": "Dhokha kha gya",
        "usage": "{tr}dhoka",
    },
)
async def katgya(chutiya):
    "Dhokha kha gya"
    txt = choice(dogememes.DHOKA)
    await eor(chutiya, txt)


@doge.bot_cmd(
    pattern="hey$",
    command=("hey", plugin_category),
    info={
        "header": "start a conversation with people",
        "usage": "{tr}hey",
    },
)
async def hoi(e):
    "start a conversation with people."
    txt = choice(dogememes.HELLOSTR)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="pro$",
    command=("pro", plugin_category),
    info={
        "header": "If you think you're pro, try this.",
        "usage": "{tr}pro",
    },
)
async def proo(e):
    "If you think you're pro, try this."
    txt = choice(dogememes.PRO_STRINGS)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="react ?([\s\S]*)",
    command=("react", plugin_category),
    info={
        "header": "Make your userbot react",
        "types": [
            "happy",
            "think",
            "wave",
            "wtf",
            "love",
            "teledoge",
            "dead",
            "sad",
            "dog",
        ],
        "usage": ["{tr}react <type>", "{tr}react"],
    },
)
async def _(e):
    "Make your userbot react."
    input_str = e.pattern_match.group(1)
    if input_str in "happy":
        emoticons = dogememes.FACEREACTS[0]
    elif input_str in "think":
        emoticons = dogememes.FACEREACTS[1]
    elif input_str in "wave":
        emoticons = dogememes.FACEREACTS[2]
    elif input_str in "wtf":
        emoticons = dogememes.FACEREACTS[3]
    elif input_str in "love":
        emoticons = dogememes.FACEREACTS[4]
    elif input_str in "teledoge":
        emoticons = dogememes.FACEREACTS[5]
    elif input_str in "dead":
        emoticons = dogememes.FACEREACTS[6]
    elif input_str in "sad":
        emoticons = dogememes.FACEREACTS[7]
    elif input_str in "dog":
        emoticons = dogememes.FACEREACTS[8]
    else:
        emoticons = dogememes.FACEREACTS[9]
    txt = choice(emoticons)
    await eor(e, txt)


@doge.bot_cmd(
    pattern="10iq$",
    command=("10iq", plugin_category),
    info={
        "header": "You retard !!",
        "usage": "{tr}10iq",
    },
)
async def iqless(e):
    "You retard !!"
    await eor(e, "♿")


@doge.bot_cmd(
    pattern="fp$",
    command=("fp", plugin_category),
    info={
        "header": "send you face pam emoji!",
        "usage": "{tr}fp",
    },
)
async def facepalm(e):
    "send you face pam emoji!"
    await eor(e, "🤦‍♂")


@doge.bot_cmd(
    pattern="bt$",
    command=("bt", plugin_category),
    info={
        "header": "Believe me, you will find this useful.",
        "usage": "{tr}bt",
    },
    groups_only=True,
)
async def bluetext(e):
    """Believe me, you will find this useful."""
    await eor(
        e,
        "/BLUETEXT /MUST /CLICK.\n"
        "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS?",
    )


@doge.bot_cmd(
    pattern="session$",
    command=("session", plugin_category),
    info={
        "header": "telethon session error code(fun)",
        "usage": "{tr}session",
    },
)
async def _(event):
    "telethon session error code(fun)."
    mentions = "**telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: \
        The authorization key (session file) was used under two different IP addresses simultaneously, \
        and can no longer be used. Use the same session exclusively, \
        or use different sessions (caused by GetMessagesRequest)**"
    await eor(event, mentions)


@doge.bot_cmd(
    pattern="tcat$",
    command=("tcat", plugin_category),
    info={
        "header": "Some random cat facial text art",
        "usage": "{tr}tcat",
    },
)
async def hmm(c):
    "Some random cat facial text art"
    await eor(c, textcat())


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
    await eor(dog, why())


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
    await eor(dog, fact())


@doge.bot_cmd(
    pattern="^\:/$",
    command=("\:", plugin_category),
    info={
        "header": "Animation command",
        "usage": "\:",
    },
)
async def kek(keks):
    "Animation command"
    keks = await eor(keks, ":\\")
    uio = ["/", "\\"]
    for i in range(5):
        await sleep(0.5)
        txt = ":" + uio[i % 2]
        await keks.edit(txt)


@doge.bot_cmd(
    pattern="^\-_-$",
    command=("-_-", plugin_category),
    info={
        "header": "Animation command",
        "usage": "-_-",
    },
)
async def lol(lel):
    "Animation command"
    lel = await eor(lel, "-__-")
    okay = "-__-"
    for _ in range(15):
        await sleep(0.5)
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@doge.bot_cmd(
    pattern="^\;_;$",
    command=(";_;", plugin_category),
    info={
        "header": "Animation command",
        "usage": ";_;",
    },
)
async def fun(e):
    "Animation command"
    e = await eor(e, ";__;")
    t = ";__;"
    for _ in range(15):
        await sleep(0.5)
        t = t[:-1] + "_;"
        await e.edit(t)


@doge.bot_cmd(
    pattern="oof$",
    command=("oof", plugin_category),
    info={
        "header": "Animation command",
        "usage": "{tr}oof",
    },
)
async def Oof(e):
    "Animation command."
    t = "Oof"
    dogevent = await eor(e, t)
    for _ in range(15):
        await sleep(0.5)
        t = t[:-1] + "of"
        await dogevent.edit(t)


@doge.bot_cmd(
    pattern="type ([\s\S]*)",
    command=("type", plugin_category),
    info={
        "header": "Type writter animation.",
        "usage": "{tr}type text",
    },
)
async def typewriter(typew):
    "Type writter animation."
    message = typew.pattern_match.group(1)
    sleep_time = 0.2
    typing_symbol = "|"
    old_text = ""
    typew = await eor(typew, typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


@doge.bot_cmd(
    pattern="repeat (\d*) ([\s\S]*)",
    command=("repeat", plugin_category),
    info={
        "header": "repeats the given text with given no of times.",
        "usage": "{tr}repeat <count> <text>",
        "examples": "{tr}repeat 10 DogeUserBot",
    },
)
async def _(event):
    "To repeat the given text."
    dog = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = dog[1]
    count = int(dog[0])
    repsmessage = (f"{message} ") * count
    await eor(event, repsmessage)


@doge.bot_cmd(
    pattern="meme",
    command=("meme", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}meme <emoji/text>",
            "{tr}meme",
        ],
    },
)
async def meme(event):
    "Animation command."
    memeVar = event.text
    sleepValue = 0.5
    memeVar = memeVar[6:]
    if not memeVar:
        memeVar = "✈️"
    event = await eor(event, "-------------" + memeVar)
    await sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await sleep(sleepValue)
    await event.edit("-------------" + memeVar)
    await sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await sleep(sleepValue)
    await event.edit(memeVar)


@doge.bot_cmd(
    pattern="give",
    command=("give", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}give <emoji/text>",
            "{tr}give",
        ],
    },
)
async def give(event):
    "Animation command."
    giveVar = event.text
    sleepValue = 0.5
    lp = giveVar[6:]
    if not lp:
        lp = " 🍭"
    event = await eor(event, lp + "        ")
    await sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)
    await sleep(sleepValue)
    await event.edit(lp + "        ")
    await sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)


@doge.bot_cmd(
    pattern="sadmin$",
    command=("sadmin", plugin_category),
    info={
        "header": "Shouts Admin Animation command",
        "usage": "{tr}sadmin",
    },
)
async def _(event):
    "Shouts Admin Animation command."
    animation_ttl = range(13)
    event = await eor(event, "sadmin")
    animation_chars = [
        "@aaaaaaaaaaaaadddddddddddddmmmmmmmmmmmmmiiiiiiiiiiiiinnnnnnnnnnnnn",
        "@aaaaaaaaaaaaddddddddddddmmmmmmmmmmmmiiiiiiiiiiiinnnnnnnnn",
        "@aaaaaaaaaaddddddddddmmmmmmmmmmiiiiiiiiiinnnnnnnnnn",
        "@aaaaaaaaddddddddmmmmmmmmiiiiiiiinnnnnnnn",
        "@aaaaaaddddddmmmmmmiiiiiinnnnnn",
        "@aaaaddddmmmmiiiinnnn",
        "@aaadddmmmiiinnn",
        "@admin",
    ]
    for i in animation_ttl:
        await sleep(1)
        await event.edit(animation_chars[i % 13])


# Template by @Infinity20998, modified by @o_s_h_o_r_a_j
@doge.bot_cmd(
    pattern="pf ?(.*)",
    command=("pf", plugin_category),
    info={
        "header": "Pay tribute to victim by pressing F(s)",
        "usage": [
            "{tr}pf <text>",
        ],
    },
)
async def payF(event):
    "Bullies the victim"
    await event.delete()
    bot = "@FsInChatBot"
    hidetxt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not hidetxt:
        return await edl(event, "__How can I bulli without text.__")
    results = await event.client.inline_query(bot, hidetxt)
    await results[0].click(event.chat_id, reply_to=reply_to_id)


# Created by @Jisan7509
@doge.bot_cmd(
    pattern="fox ?([\s\S]*)",
    command=("fox", plugin_category),
    info={
        "header": "fox meme",
        "description": "Send sneeky fox troll",
        "usage": "{tr}fox <text>",
    },
)
async def dog(event):
    "sneeky fox troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "`Give me some text to process...`")
    msg = f"/sf {input_text}"
    dog = await eor(event, "```Fox is on your way...```")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="talkme ?([\s\S]*)",
    command=("talkme", plugin_category),
    info={
        "header": "talk to me meme",
        "description": "Send talk to me troll",
        "usage": "{tr}talkme <text>",
    },
)
async def dog(event):
    "talk to me troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "`Give me some text to process...`")
    msg = f"/ttm {input_text}"
    dog = await eor(event, "```Wait making your hardcore meme...```")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="sbrain ?([\s\S]*)",
    command=("sbrain", plugin_category),
    info={
        "header": "brain say meme",
        "description": "Send you a sleeping brain meme.",
        "usage": "{tr}sbrain <text>",
    },
)
async def dog(event):
    "Sleeping brain meme."
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "`Give me some text to process...`")
    msg = f"/bbn {input_text}"
    dog = await eor(event, "```You can't sleep...```")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="sbob ?([\s\S]*)",
    command=("sbob", plugin_category),
    info={
        "header": "spongebob meme",
        "description": "Send you spongebob meme.",
        "usage": "{tr}sbob <text>",
    },
)
async def dog(event):
    "spongebob troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "`Give me some text to process...`")
    msg = f"/sp {input_text}"
    dog = await eor(event, "```Yaah wait for spongebob...```")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="child ?([\s\S]*)",
    command=("child", plugin_category),
    info={
        "header": "child meme",
        "description": "Send you child in trash meme.",
        "usage": "{tr}child <text>",
    },
)
async def dog(event):
    "child troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "`Give me some text to process...`")
    msg = f"/love {input_text}"
    dog = await eor(event, "```Wait for your son......```")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="toy ?([\s\S]*)",
    command=("toy", plugin_category),
    info={
        "header": "toy meme",
        "description": "Send soft toy troll",
        "usage": "{tr}toy <text>",
    },
)
async def dog(event):
    "toy troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "Give me some text to process...")
    msg = f"/sdp {input_text}"
    dog = await eor(event, " toy is on your way...")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="bt ?([\s\S]*)",
    command=("bt", plugin_category),
    info={
        "header": "brain meme",
        "description": "Send brain troll",
        "usage": "{tr}bt <text>",
    },
)
async def dog(event):
    "brain troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "Give me some text to process...")
    msg = f"/bbs {input_text}"
    dog = await eor(event, "Brain is on your way...")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="sbb ?([\s\S]*)",
    command=("sbb", plugin_category),
    info={
        "header": "spongebob meme",
        "description": "Send spongebob troll",
        "usage": "{tr}sbb <text>",
    },
)
async def dog(event):
    "spongebob troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "Give me some text to process...")
    msg = f"/iiho {input_text}"
    dog = await eor(event, " spongebob is on your way...")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)


@doge.bot_cmd(
    pattern="att ?([\s\S]*)",
    command=("att", plugin_category),
    info={
        "header": "animation meme",
        "description": "Send animation troll",
        "usage": "{tr}att <text>",
    },
)
async def dog(event):
    "animation troll"
    reply_to_id = await reply_id(event)
    input_text = event.pattern_match.group(1)
    if not input_text:
        return await edl(event, "Give me some text to process...")
    msg = f"/f {input_text}"
    dog = await eor(event, "Animation is on your way...")
    await mememaker(event, msg, dog, event.chat_id, reply_to_id)
