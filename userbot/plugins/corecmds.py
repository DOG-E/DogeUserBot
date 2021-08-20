from os import path, remove
from datetime import datetime
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, PLUGIN_CHANNEL, SUDO_LIST, Config, _dogeutils, doge, edl, eor, hmention, reply_id, tr

plugin_category = "bot"
thumb_image_path = path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@doge.bot_cmd(
    pattern="install$",
    command=("install", plugin_category),
    info={
        "header": "To install an external plugin.",
        "description": "Reply to any external plugin(supported by Doge) to install it in your bot.",
        "usage": "{tr}install",
    },
)
async def install(event):
    "To install an external plugin."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await event.client.download_media(
                reply_message,
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await reply_message.forward_to(PLUGIN_CHANNEL)
                await edl(
                    event,
                    f"**🔮 Plugin installed {path.basename(downloaded_file_name)} successfully!\
                    \n\n\
                    ✨ If you want to learn about {path.basename(downloaded_file_name)} you have installed, write** `{tr}doge {path.basename(downloaded_file_name)}`.",
                    90,
                )
            else:
                remove(downloaded_file_name)
                await edl(
                    event, "Errors! This plugin is already installed/pre-installed."
                )
        except Exception as e:
            await edl(event, f"**Error:**\n`{e}`")
            remove(downloaded_file_name)


@doge.bot_cmd(
    pattern="ptest$",
    command=("ptest", plugin_category),
    info={
        "header": "To temporary install for test an external plugin.",
        "description": "Reply to any external plugin(supported by Doge) to temporary install for test it in your bot.",
        "note": "The plugin will be removed automatically when you restart Doge.",
        "usage": "{tr}ptest",
    },
)
async def install(event):
    "To install for test an external plugin."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edl(
                    event,
                    f"**🔮 Plugin temporary installed {path.basename(downloaded_file_name)} successfully!\
                    \n\n\
                    ✨ If you want to learn about {path.basename(downloaded_file_name)} you have installed, write** `{tr}doge {path.basename(downloaded_file_name)}`.",
                )
            else:
                remove(downloaded_file_name)
                await edl(
                    event,
                    f"**🚨 Error!\
                    \n🚧 This plugin is already installed or pre-installed.\
                    \n\n\
                    ✨ If you want to learn about {path.basename(downloaded_file_name)} you have installed, write** `{tr}doge {path.basename(downloaded_file_name)}`.",
                    60,
                )
        except Exception as e:
            await edl(event, f"**Error:**\n`{e}`")
            remove(downloaded_file_name)


@doge.bot_cmd(
    pattern="load ([\s\S]*)",
    command=("load", plugin_category),
    info={
        "header": "To load a plugin again. if you have unloaded it",
        "description": "To load a plugin again which you unloaded by {tr}unload",
        "usage": "{tr}load <plugin name>",
        "examples": "{tr}load markdown",
    },
)
async def load(event):
    "To load a plugin again. if you have unloaded it"
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edl(event, f"`Loaded successfully {shortname}`")
    except Exception as e:
        await eor(
            event,
            f"Couldn't load {shortname} because of the following error:\
                \n{e}",
        )


@doge.bot_cmd(
    pattern="send ([\s\S]*)",
    command=("send", plugin_category),
    info={
        "header": "To upload a plugin file to telegram chat",
        "usage": "{tr}send <plugin name>",
        "examples": "{tr}send markdown",
    },
)
async def send(event):
    "To uplaod a plugin file to telegram chat"
    reply_to_id = await reply_id(event)
    thumb = thumb_image_path if path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = f"./userbot/plugins/{input_str}.py"
    if path.exists(the_plugin_file):
        start = datetime.now()
        doog = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await doog.edit(
            f"<b><i>➥ Plugin Name: {input_str}</i></b>\n<b><i>➥ Uploaded in {ms} seconds.</i></b>\n<b><i>➥ Uploaded by: {hmention}</i></b>",
            parse_mode="html",
        )
    else:
        await eor(event, "Error 404: File not found!")


@doge.bot_cmd(
    pattern="unload ([\s\S]*)",
    command=("unload", plugin_category),
    info={
        "header": "To unload a plugin temporarily.",
        "description": "You can load this unloaded plugin by restarting or using {tr}load cmd. Useful for cases like seting notes in rose bot({tr}unload markdown).",
        "usage": "{tr}unload <plugin name>",
        "examples": "{tr}unload markdown",
    },
)
async def unload(event):
    "To unload a plugin temporarily."
    shortname = event.pattern_match.group(1).lower
    try:
        remove_plugin(shortname)
        await eor(event, f"Unloaded {shortname} successfully!")
    except Exception as e:
        await eor(event, f"Unloaded {shortname}:\n{e}")


@doge.bot_cmd(
    pattern="uninstall ([\s\S]*)",
    command=("uninstall", plugin_category),
    info={
        "header": "To uninstall a plugin temporarily.",
        "description": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1).lower
    path = Path(f"userbot/plugins/{shortname}.py")
    if not path.exists(path):
        return await edl(event, f"There is no plugin with path {path} to uninstall it")
    remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        async for message in event.client.iter_messages(
            PLUGIN_CHANNEL,
            filter=InputMessagesFilterDocument,
            search=shortname,
        ):
            await message.delete()
        await eor(event, f"{shortname} uninstalled successfully!")
    except Exception as e:
        await eor(
            event,
            f"{shortname} uninstalled:\
                \n{e}"
        )


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
    OUTPUT = "**SUICIDE BOMB:**\nSuccessfully deleted all folders and files in userbot server"
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
    OUTPUT = f"**[Doge's](tg://need_update_for_some_feature/) PLUGINS:**\n{o}"
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
        f"**[Doge's](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    await eor(event, OUTPUT)
