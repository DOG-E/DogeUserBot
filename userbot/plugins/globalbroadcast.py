# © Copyright 2021 Lynx-Userbot LLC Company.
# GPL-3.0 License From Github
# WARNING !!
# Credits by @TeamUltroid
from . import doge, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="ggsend(?:\s|$)([\s\S]*)",
    command=("ggsend", plugin_category),
    info={
        "header": "Send messages to all groups you are in.",
        "usage": "{tr}ggsend <Text>",
        "examples": "{tr}ggsend Hello",
    },
)
async def gcast(event):
    """Adds given chat to global group cast."""
    dogeinput = event.pattern_match.group(1)
    if not dogeinput:
        return await eor(dogeinput, "`Please Give A Message.`")
    tt = event.text
    msg = tt[8:]
    dogevent = await eor(event, "`Sending Group Messages Globally... 📢`")
    err = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group and not x.is_user:
            chat = x.id
            try:
                done += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                err += 1
    await dogevent.edit(
        f"**✔️ Succesfully** Send Message To: `{done}` Group.\n**❌ Fail** Send Message To: `{err}` Group."
    )


@doge.bot_cmd(
    pattern="gusend(?:\s|$)([\s\S]*)",
    command=("gusend", plugin_category),
    info={
        "header": "Send messages to all users. <Private Message>",
        "usage": "{tr}gusend <Text>",
        "examples": "{tr}gusend Hello",
    },
)
async def gucast(event):
    """Adds given chat to global user cast."""
    dogeinput = event.pattern_match.group(1)
    if not dogeinput:
        return await eor(dogeinput, "`Please Give A Message`")
    tt = event.text
    msg = tt[8:]
    dogevent = await eor(event, "`Sending Private Messages Globally... 📢`")
    err = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                err += 1
    await dogevent.edit(
        f"**✔️ Successfully** Send Message To: `{done}` Users.\n**❌ Fail** Send Message To: `{err}` Users."
    )
