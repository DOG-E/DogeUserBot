# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import doge, eor, lan, tr

plugin_category = "admin"

CHAT_FLOOD = sql.__load_flood_settings()
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@doge.bot_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    dogadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not dogadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"**{lan('autoantiflood')}**\
                \n@admin [{lan('userx')}](tg://user?id={event.message.sender_id}) {lan('adminreport')}\
                \n`{e}`",
            reply_to=event.message.id,
        )
        await sleep(4)
        await no_admin_privilege_message.edit(lan("antiflood1"))
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"""**{lan('autoantiflood')}**
[{lan('userx')}](tg://user?id={event.message.sender_id}) {lan('antiflood2')}""",
            reply_to=event.message.id,
        )


@doge.bot_cmd(
    pattern="setflood(?:\s|$)([\s\S]*)",
    command=("setflood", plugin_category),
    info={
        "header": lan("setfood1"),
        "description": lan("antiflood2"),
        "note": lan("antiflood3"),
        "usage": f"{tr}setflood {lan('count')}",
        "examples": [
            "{tr}setflood 10",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    lan("setflood4")
    input_str = event.pattern_match.group(1)
    event = await eor(event, lan("antiflood5"))
    await sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(lan("antiflood6").format(input_str))
    except Exception as e:
        await event.edit(str(e))


# Lang By Aylak - @atayist
# Copyright (C) 2021 - DOG-E
