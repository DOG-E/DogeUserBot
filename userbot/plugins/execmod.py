from userbot import doge

from ..core.managers import edl, eor
from ..helpers.utils import _dogeutils, yaml_format

plugin_category = "tools"


@doge.bot_cmd(
    pattern="suicide$",
    command=("suicide", plugin_category),
    info={
        "header": "Deletes all the files and folder in the current directory.",
        "usage": "{tr}suicide",
    },
)
async def _(event):
    "To delete all files and folders in userbot"
    cmd = "rm -rf .*"
    await _dogeutils.runcmd(cmd)
    OUTPUT = f"**SUICIDE BOMB:**\nSuccessfully deleted all folders and files in userbot server"
    event = await eor(event, OUTPUT)


@doge.bot_cmd(
    pattern="plugins$",
    command=("plugins", plugin_category),
    info={
        "header": "To list all plugins in userbot.",
        "usage": "{tr}plugins",
    },
)
async def _(event):
    "To list all plugins in userbot"
    cmd = "ls userbot/plugins"
    o = (await _dogeutils.runcmd(cmd))[0]
    OUTPUT = f"**[Dog's](tg://need_update_for_some_feature/) PLUGINS:**\n{o}"
    await eor(event, OUTPUT)


@doge.bot_cmd(
    pattern="env$",
    command=("env", plugin_category),
    info={
        "header": "To list all environment values in userbot.",
        "description": "to show all heroku vars/Config values in your userbot",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in userbot"
    cmd = "env"
    o = (await _dogeutils.runcmd(cmd))[0]
    OUTPUT = (
        f"**[Dog's](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    await eor(event, OUTPUT)


@doge.bot_cmd(
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
    await eor(
        event, f"**This message was posted on :** `{yaml_format(result)}`"
    )
