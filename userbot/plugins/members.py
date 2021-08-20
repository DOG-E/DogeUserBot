from asyncio import sleep
from csv import reader, writer
from random import randrange

from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPeerUser

from . import MMSGTEXT, doge, edl, eor, get_chatinfo, wowmygroup

plugin_category = "tool"


@doge.bot_cmd(
    pattern="(invite|ekle) ([\s\S]*)",
    command=("invite", plugin_category),
    info={
        "header": "Add the given user/users to the group where u used the command.",
        "description": "Adds only mentioned person or bot not all members",
        "usage": "{tr}invite <username(s)/userid(s)>",
        "examples": "{tr}invite @mutlcc @MissRose_bot",
    },
)
async def _(event):
    "To invite a user to chat."
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    AddChatUserRequest(
                        chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                    )
                )
            except Exception as e:
                return await edl(event, f"`{str(e)}`", 5)

    else:
        # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    InviteToChannelRequest(channel=event.chat_id, users=[user_id])
                )
            except Exception as e:
                return await edl(event, f"`{e}`", 5)

    await eor(event, f"`{to_add_users} is/are invited successfully`")


@doge.bot_cmd(
    pattern="inviteall ([\s\S]*)",
    command=("inviteall", plugin_category),
    info={
        "header": "Dredge up members from other groups by using the group username",
        "usage": "{tr}inviteall <group_username>",
        "example": "{tr}inviteall @DogeSup",
    },
)
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    chat = await event.get_chat()
    creator = chat.creator
    if not creator:
        return await edl(event, "`I am not owner here!`", 5)

    if not sender.id == me.id:
        dogevent = await eor(event, "`Processing...`")
    else:
        dogevent = await eor(event, "`Processing...`")
    dog = await get_chatinfo(event)
    s = 0
    f = 0
    error = "None"
    await dogevent.edit("**TerminalStatus**\n\n`Collecting Users...`")
    async for user in event.client.iter_participants(dog.full_chat.id):
        try:
            if error.startswith("Too"):
                return await dogevent.edit(
                    f"**Terminal Finished With Error**\n(`May Got Limit Error from telethon Please try agin Later`)\n**Error**: \n`{error}`\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people"
                )

            await event.client(InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await dogevent.edit(
                f"**Terminal Running...**\n\n• Invited `{s}` people \n• Failed to Invite `{f}` people\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await dogevent.edit(
        f"**Terminal Finished** \n\n• Successfully Invited `{s}` people \n• failed to invite `{f}` people"
    )


@doge.bot_cmd(
    pattern="getmember(s)$",
    command=("getmembers", plugin_category),
    info={
        "header": "Collect members data from the group.",
        "description": "This plugin is done before using the add member plugin.",
        "usage": "{tr}getmember",
    },
    groups_only=True,
)
async def getmembers(event):
    channel = event.chat_id
    chat = await event.get_chat()
    creator = chat.creator

    flag = await wowmygroup(event, MMSGTEXT)
    if flag:
        return

    if not creator:
        return await edl(event, "`I am not owner here!`", 5)

    dogevent = await eor(event, "`Please wait...`")
    saint = event.client
    members = await saint.get_participants(channel, aggressive=True)
    with open("members.csv", "w", encoding="UTF-8") as f:
        write = writer(f, delimiter=",", lineterminator="\n")
        write.writerow(["user_id", "hash"])
        for member in members:
            write.writerow([member.id, member.access_hash])
    await eor(dogevent, "`Successfully collect data members.`")


@doge.bot_cmd(
    pattern="addmember(s)$",
    command=("addmembers", plugin_category),
    info={
        "header": "Add your group members. (there's a limit)",
        "description": "This plugin is done after using the get member plugin.",
        "usage": "{tr}addmember",
    },
    groups_only=True,
)
async def addmembers(event):
    chat = await event.get_chat()
    creator = chat.creator

    flag = await wowmygroup(event, MMSGTEXT)
    if flag:
        return

    if not creator:
        return await edl(event, "`I am not owner here!`", 5)

    dogevent = await eor(event, "`The process of adding members, starting from 0`")
    user_to_add = None
    saint = event.client
    x = []
    with open("members.csv", encoding="UTF-8") as f:
        rows = reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            i = {"user_id": int(row[0]), "hash": int(row[1])}
            x.append(i)
    y = 0
    for i in x:
        y += 1
        if y % 30 == 0:
            await eor(dogevent, f"`Has reached 30 members, wait until {200/60} min.`")
            await sleep(200)

        if user_to_add is None:
            try:
                user_to_add = InputPeerUser(i["user_id"], i["hash"])
            except BaseException:
                pass
        try:
            await saint(InviteToChannelRequest(channel=chat, users=[user_to_add]))
            await sleep(randrange(5, 7))
            await eor(dogevent, f"`Prosess of adding {y} Members...`")
        except TypeError:
            y -= 1
            continue
        except UserAlreadyParticipantError:
            y -= 1
            continue
        except UserPrivacyRestrictedError:
            y -= 1
            continue
        except UserNotMutualContactError:
            y -= 1
            continue
