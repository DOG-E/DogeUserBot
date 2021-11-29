# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from . import BOT_USERNAME, doge, edl, eor, reply_id, tr

plugin_category = "bot"

hemojis = {
    "admin": "👮‍♂️",
    "bot": "🤖",
    "fun": "🎈",
    "misc": "🪀",
    "tool": "🧰",
    "hub": "🍑",
}


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == tr:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edl(
                event,
                f"**🚨 I couldn't find** `{input_str}` **plugin or command.**",
            )
            return None
        await edl(event, f"**🚨 I couldn't find** `{input_str}` **command.**")
        return None
    except Exception as e:
        await edl(
            event,
            f"**🚨 ERROR:**\
            \n➡️ `{e}`",
        )
        return None
    outstr = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
        \n\n⌨️ Coᴍᴍᴀɴᴅ:** `{tr}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**🧩 Pʟᴜɢɪɴ:** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**🗃 Cᴀᴛᴇɢoʀʏ:** `{category}`\n\n"
    outstr += f"**🐾 Iɴᴛʀo:**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event, flag):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edl(
            event,
            f"**🚨 ERROR:**\
            \n➡️ `{e}`",
        )
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != "-p")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"**🧩 Pʟᴜɢɪɴ:** `{input_str}`\n"
    outstr += f"**⌨️ Coᴍᴍᴀɴᴅs:** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**🗃 Cᴀᴛᴇɢoʀʏ:** `{category}`\n\n"
    for cmd in sorted(cmds):
        outstr += f"**🐾 Cᴍᴅ:** `{tr}{cmd}`\n"
        try:
            outstr += f"**🔹 Iɴғo:** __{CMD_INFO[cmd][1]}__\n\n"
        except IndexError:
            outstr += f"**🔹 Iɴғo:** -\n\n"
    outstr += f"**💬 Usᴀɢᴇ:** `{tr}doge <command name>`\
        \n\
        \n**🐾 Note:** If command name is same as plugin name then use this `{tr}doge .c <command name>`."
    return outstr


async def grpinfo():
    outstr = "**🐶 Doɢᴇ UsᴇʀBoᴛ\
        \n\n🐾 Aʟʟ Pʟᴜɢɪɴs:**\
        \n\n"
    outstr += f"**💬 Usᴀɢᴇ:** `{tr}doge <plugin name>`\n\n"
    category = ["admin", "bot", "fun", "misc", "tool", "hub"]
    for dog in category:
        plugins = GRP_INFO[dog]
        outstr += f"**{hemojis[dog]} {dog.title()} **({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**🐶 Doɢᴇ UsᴇʀBoᴛ\
        \n\n🐾 Toᴛᴀʟ Lɪsᴛ Oғ Coᴍᴍᴀɴᴅs:** \
        \n\n"
    category = ["admin", "bot", "fun", "misc", "tool", "hub"]
    for dog in category:
        plugins = GRP_INFO[dog]
        outstr += f"**{hemojis[dog]} {dog.title()} ** - {len(plugins)}\n\n"
        for plugin in plugins:
            cmds = PLG_INFO[plugin]
            outstr += f"🔹** {plugin.title()} has {len(cmds)} commands**\n"
            for cmd in sorted(cmds):
                outstr += f"  - `{tr}{cmd}`\n"
            outstr += "\n"
    outstr += f"**💬 Usᴀɢᴇ:** `{tr}doge .c <command name>`"
    return outstr


@doge.bot_cmd(
    pattern="([Dd]oge|help) ?(.c|.p|.a)? ?([\s\S]*)?",
    command=("doge", plugin_category),
    info={
        "header": "To get guide for DogeUserBot.",
        "description": "To get information or guide for the command or plugin.",
        "note": "If command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide.",
        "flags": {
            "c": "To get info of command.",
            "p": "To get info of plugin.",
            "all": "To get all plugins in text format.",
        },
        "usage": [
            "{tr}doge (plugin/command name)",
            "{tr}doge .c (command name)",
            "{tr}doge .all",
        ],
        "examples": ["{tr}doge alive", "{tr}doge .c ialive"],
    },
)
async def _(event):
    "🐶 To get guide for @DogeUserBot."
    flag = event.pattern_match.group(2)
    input_str = event.pattern_match.group(3)
    reply_to_id = await reply_id(event)
    if flag and flag == ".c" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    elif flag == ".a":
        outstr = await grpinfo()
    else:
        results = await event.client.inline_query(BOT_USERNAME, "help")
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
        return
    await eor(event, outstr)


@doge.bot_cmd(
    pattern="cmds(?:\s|$)([\s\S]*)",
    command=("cmds", plugin_category),
    info={
        "header": "To show list of cmds.",
        "description": "If no input is given then will show list of all commands.",
        "usage": [
            "{tr}cmds",
            "{tr}cmds <plugin name> for paticular plugin",
        ],
    },
)
async def _(event):
    "To get list of commands."
    input_str = event.pattern_match.group(1)
    if not input_str:
        outstr = await cmdlist()
    else:
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edl(event, "__🚨 Invalid plugin name recheck it.__")
        except Exception as e:
            return await edl(
                event,
                f"**🚨 ERROR:**\
                \n➡️ `{e}`",
            )
        outstr = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
            \n\n🐾 {input_str.title()} has {len(cmds)} commands:**\n"
        for cmd in cmds:
            outstr += f"  - `{tr}{cmd}`\n\n"
        outstr += f"**💬 Usᴀɢᴇ:** `{tr}doge .c <command name>`"
    await eor(
        event,
        outstr,
        aslink=True,
        linktext="🐶 Doɢᴇ UsᴇʀBoᴛ\
            \n\n🐾 Total list of commands: ",
    )


@doge.bot_cmd(
    pattern="[sS] ([\s\S]*)",
    command=("s", plugin_category),
    info={
        "header": "To search commands.",
        "examples": "{tr}s song",
    },
)
async def _(event):
    "To search commands."
    cmd = event.pattern_match.group(1)
    found = [i for i in sorted(list(CMD_INFO)) if cmd in i]
    if found:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
            \n\n🐾 I found {len(found)} commands for:** `{cmd}`\
            \n\n{out_str}"
        out += f"\n\
            \n__💬 For more info check__ `{tr}doge .c <command>`"
    else:
        out = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
            \n\n🙁 I can't find any such command:** `{cmd}`\
            \n\n🐾 You can get info about other plugins with `{tr}doge`"
    await eor(event, out)
