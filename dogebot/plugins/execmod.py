# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from dogebot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _dogeutils, parse_pre, yaml_format

plugin_category = "tools"


@doge.doge_cmd(
    pattern="suicide$",
    command=("suicide", plugin_category),
    info={
        "header": "Deletes all the files and folder in the current directory.",
        "usage": "{tr}suicide",
    },
)
async def _(event):
    "To delete all files and folders in dogebot"
    cmd = "rm -rf .*"
    await _dogeutils.runcmd(cmd)
    OUTPUT = f"**SUICIDE BOMB:**\nSuccessfully deleted all folders and files in dogebot server"
    event = await edit_or_reply(event, OUTPUT)


@doge.doge_cmd(
    pattern="plugins$",
    command=("plugins", plugin_category),
    info={
        "header": "To list all plugins in dogebot.",
        "usage": "{tr}plugins",
    },
)
async def _(event):
    "To list all plugins in dogebot"
    cmd = "ls dogebot/plugins"
    o = (await _dogeutils.runcmd(cmd))[0]
    OUTPUT = f"**[Doge's](tg://need_update_for_some_feature/) PLUGINS:**\n{o}"
    await edit_or_reply(event, OUTPUT)


@doge.doge_cmd(
    pattern="env$",
    command=("env", plugin_category),
    info={
        "header": "To list all environment values in dogebot.",
        "description": "to show all heroku vars/Config values in your dogebot",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in dogebot"
    cmd = "env"
    o = (await _dogeutils.runcmd(cmd))[0]
    OUTPUT = (
        f"**[Doge's](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    await edit_or_reply(event, OUTPUT)


@doge.doge_cmd(
    pattern="noformat$",
    command=("noformat", plugin_category),
    info={
        "header": "To get replied message without markdown formating.",
        "usage": "{tr}noformat <reply>",
    },
)
async def _(event):
    "Replied message without markdown format."
    reply = await event.get_reply_message()
    if not reply or not reply.text:
        return await edit_delete(
            event, "__Reply to text message to get text without markdown formating.__"
        )
    await edit_or_reply(event, reply.text, parse_mode=parse_pre)


@doge.doge_cmd(
    pattern="when$",
    command=("when", plugin_category),
    info={
        "header": "To get date and time of message when it posted.",
        "usage": "{tr}when <reply>",
    },
)
async def _(event):
    "To get date and time of message when it posted."
    reply = await event.get_reply_message()
    if reply:
        try:
            result = reply.fwd_from.date
        except Exception:
            result = reply.date
    else:
        result = event.date
    await edit_or_reply(
        event, f"**This message was posted on :** `{yaml_format(result)}`"
    )
