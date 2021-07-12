import asyncio
import re
from random import choice, randint

from telethon.utils import get_display_name

from . import (
    ALIVE_NAME,
    _format,
    amongus_gen,
    doge,
    eor,
    get_impostor_img,
    get_user_from_event,
    mention,
    reply_id,
)

plugin_category = "extra"


@doge.bot_cmd(
    pattern="amongus(?:\s|$)([\s\S]*)",
    command=("amongus", plugin_category),
    info={
        "header": "Create a Sticker based on the popular game Among Us",
        "flags": {
            "1": "red",
            "2": "lime",
            "3": "green",
            "4": "blue",
            "5": "cyan",
            "6": "brown",
            "7": "purple",
            "8": "pink",
            "9": "orange",
            "10": "yellow",
            "11": "white",
            "12": "black",
        },
        "usage": [
            "{tr}amongus <text/reply>",
            "{tr}amongus -c<colur number> <text/reply>",
        ],
        "examples": [
            "{tr}amongus gather around",
            "{tr}amongus -c3 gather around",
        ],
    },
)
async def sayliecmd(event):
    text = event.pattern_match.group(1)
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.raw_text
    clr = re.findall(r"-c\d+", text)
    try:
        clr = clr[0]
        clr = clr.replace("-c", "")
        text = text.replace("-c" + clr, "")
        clr = int(clr)
        if clr > 12 or clr < 1:
            clr = randint(1, 12)
    except IndexError:
        clr = randint(1, 12)
    if not text:
        if not reply:
            return await eor(event, f"{mention} Was a traitor!")
        if not reply.text:
            return await eor(
                event,
                f"{_format.mentionuser(get_display_name(reply.sender) ,reply.sender.id)} Was a traitor!",
            )
    impostor_file = await amongus_gen(text, clr)
    await event.delete()
    await event.client.send_file(event.chat_id, impostor_file, reply_to=reply_to)


@doge.bot_cmd(
    pattern="impostor(?:\s|$)([\s\S]*)",
    command=("impostor", plugin_category),
    info={
        "header": "Fun images for impostor ",
        "usage": "{tr}impostor <username/userid/reply>",
    },
)
async def procces_img(event):
    "Fun images for impostor"
    remain = randint(1, 2)
    imps = ["wasn`t the impostor", "was the impostor"]
    text2 = f"\n{remain} impostor(s) remain."
    reply_to = await reply_id(event)
    user, reason = await get_user_from_event(event, noedits=True)
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    if not user:
        try:
            if args or reply:
                user = await event.client.get_entity(args or reply.sender_id)
            else:
                user = await event.client.get_me()
            text = f"{get_display_name(user)} {choice(imps)}."
            text += text2
        except Exception:
            text = args
    else:
        text = f"{get_display_name(user)} {choice(imps)}."
        text += text2
    impostor_file = await get_impostor_img(text)
    await event.delete()
    await event.client.send_file(event.chat_id, impostor_file, reply_to=reply_to)


@doge.bot_cmd(
    pattern="imp(|n) ([\s\S]*)",
    command=("imp", plugin_category),
    info={
        "header": "Find impostor with stickers animation.",
        "description": "Imp for impostor impn for not impostor",
        "usage": ["{tr}imp <name>", "{tr}impn <name>"],
        "examples": ["{tr}imp blabla", "{tr}impn blabla"],
    },
)
async def _(event):
    "Find impostor with stickers animation."
    USERNAME = f"tg://user?id={event.client.uid}"
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    text1 = await eor(event, "Uhmm... Something is wrong here!!")
    await asyncio.sleep(2)
    await text1.delete()
    stcr1 = await event.client.send_file(
        event.chat_id, "CAADAQADRwADnjOcH98isYD5RJTwAg"
    )
    text2 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** I have to call discussion"
    )
    await asyncio.sleep(3)
    await stcr1.delete()
    await text2.delete()
    stcr2 = await event.client.send_file(
        event.chat_id, "CAADAQADRgADnjOcH9odHIXtfgmvAg"
    )
    text3 = await event.reply(
        f"**[{ALIVE_NAME}]({USERNAME}) :** We have to eject the impostor or will lose "
    )
    await asyncio.sleep(3)
    await stcr2.delete()
    await text3.delete()
    stcr3 = await event.client.send_file(
        event.chat_id, "CAADAQADOwADnjOcH77v3Ap51R7gAg"
    )
    text4 = await event.reply(f"**Others :** Where??? ")
    await asyncio.sleep(2)
    await text4.edit(f"**Others :** Who?? ")
    await asyncio.sleep(2)
    await text4.edit(
        f"**[{ALIVE_NAME}]({USERNAME}) :** Its {name} , I saw {name}  using vent,"
    )
    await asyncio.sleep(3)
    await text4.edit(f"**Others :**Okay.. Vote {name} ")
    await asyncio.sleep(2)
    await stcr3.delete()
    await text4.delete()
    stcr4 = await event.client.send_file(
        event.chat_id, "CAADAQADLwADnjOcH-wxu-ehy6NRAg"
    )
    dogevent = await event.reply(f"{name} is ejected.......")
    await asyncio.sleep(2)
    await dogevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.5)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    await stcr4.delete()
    if cmd == "":
        await dogevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} was an impostor.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         0 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
        await asyncio.sleep(4)
        await dogevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADLQADnjOcH39IqwyR6Q_0Ag")
    elif cmd == "n":
        await dogevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ{name} was not an impostor.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         1 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
        await asyncio.sleep(4)
        await dogevent.delete()
        await event.client.send_file(event.chat_id, "CAADAQADQAADnjOcH-WOkB8DEctJAg")


@doge.bot_cmd(
    pattern="timp(|n) ([\s\S]*)",
    command=("timp", plugin_category),
    info={
        "header": "Find impostor with text animation.",
        "description": "timp for impostor timpn for not impostor",
        "usage": ["{tr}timp <name>", "{tr}timpn <name>"],
        "examples": ["{tr}timp blabla", "{tr}timpn blabla"],
    },
)
async def _(event):
    "Find impostor with text animation."
    name = event.pattern_match.group(2)
    cmd = event.pattern_match.group(1).lower()
    dogevent = await eor(event, f"{name} is ejected.......")
    await asyncio.sleep(2)
    await dogevent.edit("ඞㅤㅤㅤㅤ ㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤඞㅤㅤㅤㅤ ㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤ ඞㅤㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤ ඞㅤㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤ ඞㅤㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤㅤ ඞㅤㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤ ඞㅤㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤ ඞㅤ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ඞ")
    await asyncio.sleep(0.8)
    await dogevent.edit("ㅤㅤㅤㅤㅤㅤㅤㅤ ㅤ")
    await asyncio.sleep(0.2)
    if cmd == "":
        await dogevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} was an impostor.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         0 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
    elif cmd == "n":
        await dogevent.edit(
            f". 　　　。　　　　•　 　ﾟ　　。 　　.\n .　　　 　　.　　　　　。　　 。　. 　\n\n  . 　　 。   　     ඞ         。 . 　　 • 　　　　•\n\n  ﾟ {name} was not an impostor.      。　. 　 　       。　.                                        。　. \n                                   　.          。　  　. \n　'         1 Impostor remains    　 。　.  　　.                。　.        。 　     .          。 　            .               .         .    ,      。\n　　ﾟ　　　.　　.    ,　 　。　 　. 　 .     。"
        )
