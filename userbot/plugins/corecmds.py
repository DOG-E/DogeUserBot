# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from os import makedirs, path, remove
from pathlib import Path
from time import sleep

from telethon.tl.types import InputMessagesFilterDocument

from ..utils import load_module, remove_plugin
from . import (
    CMD_HELP,
    CMD_LIST,
    PLUGIN_CHANNEL,
    SUDO_LIST,
    TMP_DOWNLOAD_DIRECTORY,
    _dogeutils,
    doge,
    edl,
    eor,
    hmention,
    install_pip,
    reply_id,
    tr,
)

plugin_category = "bot"
thumb_image_path = path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@doge.bot_cmd(
    pattern="install$",
    command=("install", plugin_category),
    info={
        "h": "To install an external plugin.",
        "d": "Reply to any external plugin(supported by Doge) to install it in your bot.",
        "u": "{tr}install <reply plugin>",
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
                shortestname = shortname.replace(".py", "")
                try:
                    load_module(shortestname)
                except ModuleNotFoundError as mnfe:
                    remove(downloaded_file_name)
                    return await edl(
                        event,
                        f"**🚨 Eʀʀoʀ:**\
                        \n➡️ `{mnfe}`\
                        \n\
                        \n**🦴 Try to write** `{tr}finstall` **& reply.**",
                        15,
                    )

                try:
                    await reply_message.forward_to(PLUGIN_CHANNEL)
                except Exception:
                    remove(downloaded_file_name)
                    return await edl(
                        event,
                        f"**🚨 Eʀʀoʀ:**\
                        \n**➡️ To install the plugin, you must first set a PLUGIN_CHANNEL.\
                        \n\
                        \n🔮 If you want PLUGIN_CHANNEL to be set automatically;\
                        \n🦴 Write** `{tr}set var PLUGINS True`\
                        \n\
                        \n**or\
                        \n🐾 You can install the plugin temporarily by writing** `{tr}ptest`",
                        25,
                    )

                await edl(
                    event,
                    f"**🔮 Plugin installed {shortestname} successfully!\
                    \n\n🐾 If you want to learn about {shortestname} you have installed, write:**\
                    \n\n`{tr}doge .p {shortestname}`",
                    45,
                )
            else:
                remove(downloaded_file_name)
                return await edl(
                    event,
                    f"**🚨 Eʀʀoʀ:**\
                    \n`👀 This plugin is already installed.`\
                    \n\n🐾 If you want to learn about {reply_message.file.name.replace('.py', '')} you have installed, write:**\
                    \n\n`{tr}doge .p {reply_message.file.name.replace('.py', '')}`",
                    15,
                )
        except Exception as e:
            await edl(event, f"**🚨 Eʀʀoʀ:**\n`{e}`")
            try:
                remove(downloaded_file_name)
            except Exception:
                pass


@doge.bot_cmd(
    pattern="finstall$",
    command=("finstall", plugin_category),
    info={
        "h": "To force install an external plugin.",
        "d": "Reply to any external plugin(supported by Doge) to force install it in your bot.",
        "u": "{tr}finstall <reply plugin>",
    },
)
async def finstall(event):
    "To force install an external plugin."
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
                shortestname = shortname.replace(".py", "")
                try:
                    load_module(shortestname)
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    sleep(1)
                    load_module(shortestname)

                try:
                    await reply_message.forward_to(PLUGIN_CHANNEL)
                except Exception:
                    remove(downloaded_file_name)
                    return await edl(
                        event,
                        f"**🚨 Eʀʀoʀ:**\
                        \n**➡️ To install the plugin, you must first set a PLUGIN_CHANNEL.\
                        \n\
                        \n🔮 If you want PLUGIN_CHANNEL to be set automatically;\
                        \n🦴 Write** `{tr}set var PLUGINS True`\
                        \n\
                        \n**or\
                        \n🐾 You can install the plugin temporarily by writing** `{tr}ptest`",
                        25,
                    )

                await edl(
                    event,
                    f"**🔮 Plugin installed {shortestname} successfully!\
                    \n\n🐾 If you want to learn about {shortestname} you have installed, write:**\
                    \n\n`{tr}doge .p {shortestname}`",
                    45,
                )
            else:
                remove(downloaded_file_name)
                return await edl(
                    event,
                    f"**🚨 Eʀʀoʀ:**\
                    \n`👀 This plugin is already installed.`\
                    \n\n🐾 If you want to learn about {reply_message.file.name.replace('.py', '')} you have installed, write:**\
                    \n\n`{tr}doge .p {reply_message.file.name.replace('.py', '')}`",
                    15,
                )
        except Exception as e:
            await edl(event, f"**🚨 Eʀʀoʀ:**\n`{e}`")
            try:
                remove(downloaded_file_name)
            except Exception:
                pass


@doge.bot_cmd(
    pattern="ptest$",
    command=("ptest", plugin_category),
    info={
        "h": "To temporary install for test an external plugin.",
        "d": "Reply to any external plugin(supported by Doge) to temporary install for test it in your bot.",
        "note": "The plugin will be removed automatically when you restart Doge.",
        "u": "{tr}ptest <reply plugin>",
    },
)
async def ptest(event):
    "To install for test an external plugin."
    if event.reply_to_msg_id:
        try:
            if not path.exists("userbot/temp_plugins/"):
                makedirs("userbot/temp_plugins")
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/temp_plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            shortestname = shortname.replace(".py", "")
            try:
                load_module(shortestname)
            except ModuleNotFoundError as e:
                install_pip(e.name)
                sleep(1)
                load_module(shortestname, plugin_path="userbot/temp_plugins")
            await edl(
                event,
                f"**🔮 Plugin temporary installed {shortestname} successfully!\
                \n\n🐾 If you want to learn about {shortestname} you have installed, write:**\
                \n\n`{tr}doge .p {shortestname}`",
                45,
            )
        except Exception as e:
            await edl(event, f"**🚨 Eʀʀoʀ:**\n`{e}`")
            try:
                remove(downloaded_file_name)
            except Exception:
                pass


@doge.bot_cmd(
    pattern="load ([\s\S]*)",
    command=("load", plugin_category),
    info={
        "h": "To load a plugin again. if you have unloaded it",
        "d": "To load a plugin again which you unloaded by {tr}unload",
        "u": "{tr}load <plugin name>",
        "e": "{tr}load markdown",
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
        await edl(
            event,
            f"Couldn't load {shortname} because of the following error:\
            \n{e}",
        )


@doge.bot_cmd(
    pattern="send ([\s\S]*)",
    command=("send", plugin_category),
    info={
        "h": "To upload a plugin file to telegram chat",
        "u": "{tr}send <plugin name>",
        "e": "{tr}send markdown",
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
        await edl(event, f"**🚨 Eʀʀoʀ:** File not found!")


@doge.bot_cmd(
    pattern="unload ([\s\S]*)",
    command=("unload", plugin_category),
    info={
        "h": "To unload a plugin temporarily.",
        "d": "You can load this unloaded plugin by restarting or using {tr}load cmd. Useful for cases like seting notes in rose bot({tr}unload markdown).",
        "u": "{tr}unload <plugin name>",
        "e": "{tr}unload markdown",
    },
)
async def unload(event):
    "To unload a plugin temporarily."
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edl(event, f"Unloaded {shortname} successfully!")
    except Exception as e:
        await edl(event, f"Unloaded {shortname}:\n`{e}`")


@doge.bot_cmd(
    pattern="uninstall ([\s\S]*)",
    command=("uninstall", plugin_category),
    info={
        "h": "To uninstall a plugin temporarily.",
        "d": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "u": "{tr}uninstall <plugin name>",
        "e": "{tr}uninstall markdown",
    },
)
async def uninstall(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1)
    ppath = Path(f"userbot/plugins/{shortname}.py")
    if not path.exists(ppath):
        return await edl(event, f"There is no plugin with path {ppath} to uninstall it")
    remove(ppath)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        try:
            async for message in event.client.iter_messages(
                PLUGIN_CHANNEL,
                filter=InputMessagesFilterDocument,
                search=shortname,
            ):
                await message.delete()
        except Exception:
            pass
        await edl(event, f"{shortname} uninstalled successfully!", 20)
    except Exception as e:
        await edl(event, f"{shortname} uninstalled:\n`{e}`", 25)


@doge.bot_cmd(
    pattern="plist( .all)$",
    command=("plist", plugin_category),
    info={
        "h": "To list all or external plugins in userbot.",
        "f": {
            ".all": "List all of plugins.",
        },
        "u": ["{tr}plist", "{tr}plist .all"],
    },
)
async def plist(event):
    "To list all or external plugins in userbot"
    listcmd = event.pattern_match.group(1)
    if listcmd == " .all":
        cmd = "ls userbot/plugins"
        o = f"🐾 `{(await _dogeutils.runcmd(cmd))[0]}`"
        OUTPUT = f"**[🐶](tg://need_update_for_some_feature/) Plugins:**\n{o}"
        await eor(event, OUTPUT)
    else:
        if PLUGIN_CHANNEL != None:
            installed = (
                f"**[🐶](tg://need_update_for_some_feature/) External Plugins:**\n\n"
            )
            async for plugin in event.client.iter_messages(
                PLUGIN_CHANNEL, filter=InputMessagesFilterDocument
            ):
                try:
                    shortname = plugin.file.name.split(".")[1]
                except Exception:
                    continue

                if shortname == "py":
                    installed += f"🐾 {plugin.file.name}    🐾 {plugin.file.name}\n"
            await eor(event, installed)
        else:
            await edl(
                event,
                f"**🚨 Eʀʀoʀ:**\
                \n**➡️ To list externally installed plugins, you must first set a PLUGIN_CHANNEL.\
                \n\
                \n🔮 If you want PLUGIN_CHANNEL to be set automatically;\
                \n🦴 Write** `{tr}set var PLUGINS True`",
            )


@doge.bot_cmd(
    pattern="suicide$",
    command=("suicide", plugin_category),
    info={
        "h": "Deletes all the files and folder in the current directory.",
        "u": "{tr}suicide",
    },
)
async def suicide(event):
    "To delete all files and folders in userbot"
    cmd = "rm -rf .*"
    await _dogeutils.runcmd(cmd)
    OUTPUT = "**SUICIDE BOMB:**\nSuccessfully deleted all folders and files in userbot server!"
    event = await eor(event, OUTPUT)


@doge.bot_cmd(
    pattern="env$",
    command=("env", plugin_category),
    info={
        "h": "To list all environment values in userbot.",
        "d": "To show all Heroku vars/Config values in your userbot",
        "u": "{tr}env",
    },
)
async def env(event):
    "To show all config values in userbot"
    cmd = "env"
    o = (await _dogeutils.runcmd(cmd))[0]
    OUTPUT = f"**[🐶](tg://need_update_for_some_feature/) Environments:**\n\n\n{o}"
    await eor(event, OUTPUT)
