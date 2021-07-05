# Credits to @sandy1709 (@mrconfused)
#
# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Forked, developed and edited for @DogeUserbot
#
from git import Repo
from telethon.tl.functions.channels import ExportMessageLinkRequest as GetLink

from ..core.updater import dev_doge, updater
from . import *

LOGS = logging.getLogger(__name__)

plugin_category = "tools"


@doge.doge_cmd(
    pattern="update$",
    command=("update", plugin_category),
    info={
        "header": "To update Doge.",
        "description": "I recommend you to do update deploy atlest once a week.",
        "usage": "{tr}update",
    },
)
async def _(event):
    xx = await edit_or_reply(event, "`Checking for updates...`")
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await tgbot.send_message(
            "• **Update Available** •",
            buttons=Button.inline("Changelogs", data="changes"),
        )
        Link = (await tgbot(GetLink(x.chat_id, x.id))).link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/DOG-E/DogeUserBot/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@doge.doge_cmd(
    pattern="devdoge$",
    command=("devdoge", plugin_category),
    info={
        "header": "To switch to devdoge repo",
        "usage": "{tr}devdoge",
    },
)
async def variable(var):
    await dev_doge(var)
