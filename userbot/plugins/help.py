# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
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
                f"🚨 <code>{input_str}</code> <b>pluginini ya da komutunu bulamadım.</b>",
            )
            return None
        await edl(event, f"🚨 <code>{input_str}</code> <b>komutunu bulamadım.</b>")
        return None
    except Exception as e:
        await edl(
            event,
            f"<b>🚨 Hᴀᴛᴀ:</b>\
            \n➡️ <code>{e}</code>",
        )
        return None
    outstr = f"<b>🐶 Doɢᴇ UsᴇʀBoᴛ\
        \n\n⌨️ Koᴍᴜᴛ:</b> <code>{tr}{input_str}</code>\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"<b>🧩 Pʟᴜɢɪɴ:</b> <code>{plugin}</code>\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"<b>🗃 Kᴀᴛᴇɢoʀɪ:</b> <code>{category}</code>\n\n"
    outstr += f"<b>🐾 Bɪʟɢɪ:</b>\n{about[0]}"
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
            f"<b>🚨 Hᴀᴛᴀ:</b>\
            \n➡️ <code>{e}</code>",
        )
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != ".p")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"<b>🧩 Pʟᴜɢɪɴ:</b> <code>{input_str}</code>\n"
    outstr += f"<b>⌨️ Koᴍᴜᴛʟᴀʀ:</b> <code>{len(cmds)}</code>\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"<b>🗃 Kᴀᴛᴇɢoʀɪ:</b> <code>{category}</code>\n\n"
    for cmd in sorted(cmds):
        outstr += f"<b>🐾 Koᴍᴜᴛ:</b> <code>{tr}{cmd}</code>\n"
        try:
            outstr += f"<b>🔹 Bɪʟɢɪ:</b> {CMD_INFO[cmd][1]}\n\n"
        except IndexError:
            outstr += f"<b>🔹 Bɪʟɢɪ:</b> -\n\n"
    outstr += f"<b>💬 Kᴜʟʟᴀɴɪᴍɪ:</b> <code>{tr}doge (komut adı)</code>\
        \n\
        \n<b>🐾 Noᴛ:</b> Eğer plugin adı komut adıyla aynı ise şunu kullanın: <code>{tr}doge .c (komut adı)</code>."
    return outstr


async def grpinfo():
    outstr = ""
    outstr += f"<b>🐶 Doɢᴇ UsᴇʀBoᴛ\n\
        \n💬 Kᴜʟʟᴀɴɪᴍɪ:</b> <code>{tr}doge <plugin name></code>\n\
        \n🐾 Tüᴍ Pʟᴜɢɪɴʟᴇʀ:</b>\n\n"
    category = ["admin", "bot", "fun", "misc", "tool", "hub"]
    for dog in category:
        plugins = GRP_INFO[dog]
        outstr += f"<b>{hemojis[dog]} {dog.title()} </b>({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"<code>{plugin}</code>  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**🐶 Doɢᴇ UsᴇʀBoᴛ\n\
        \n🐾 Toᴛᴀʟ Lɪsᴛ Oғ Coᴍᴍᴀɴᴅs:** \n\
        \n"
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
    command=("help", plugin_category),
    info={
        "h": "To get guide for DogeUserBot.",
        "d": "To get information or guide for the command or plugin.",
        "note": "If command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide.",
        "f": {
            "c": "To get info of command.",
            "p": "To get info of plugin.",
            "a": "To get all plugins in text format.",
        },
        "u": [
            "{tr}doge (plugin/command name)",
            "{tr}doge .c (command name)",
            "{tr}doge .a",
        ],
        "e": ["{tr}doge alive", "{tr}doge .c ping"],
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
    await eor(event, outstr, parse_mode="html")


@doge.bot_cmd(
    pattern="([Dd]oge) ?(.c|.p)? ?([\s\S]*)?",
    command=("doge", plugin_category),
    info={
        "h": "To get guide for DogeUserBot.",
        "d": "To get information or guide for the command or plugin.",
        "note": "If command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide.",
        "f": {
            "c": "To get info of command.",
            "p": "To get info of plugin.",
        },
        "u": [
            "{tr}doge",
            "{tr}doge (plugin/command name)",
            "{tr}doge .c (command name)",
        ],
        "e": ["{tr}doge alive", "{tr}doge .c ping"],
    },
)
async def _(event):
    "🐶 To get guide for @DogeUserBot."
    flag = event.pattern_match.group(2)
    input_str = event.pattern_match.group(3)
    if flag and flag == ".c" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    else:
        outstr = await grpinfo()
    await eor(event, outstr, parse_mode="html")


@doge.bot_cmd(
    pattern="cmds(?:\s|$)([\s\S]*)",
    command=("cmds", plugin_category),
    info={
        "h": "To show list of cmds.",
        "d": "If no input is given then will show list of all commands.",
        "u": [
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
                f"**🚨 Hᴀᴛᴀ:**\
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
        link_preview=True,
    )


@doge.bot_cmd(
    pattern="[sS] ([\s\S]*)",
    command=("s", plugin_category),
    info={
        "h": "To search commands.",
        "e": "{tr}s song",
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
