from os import path
from pathlib import Path

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputMessagesFilterDocument

from ..utils import load_module
from . import BOTLOG_CHATID, Config, doge, install_pip

plugin_category = "bot"


if Config.PLUGIN_CHANNEL:

    async def install():
        documentss = await doge.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await doge.download_media(
                await doge.get_messages(Config.PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(install())


if Config.DOGEPLUGIN == True:

    async def dogeplugininstall():
        try:
            documentss = await doge.get_messages(
                -1001482657964, None, filter=InputMessagesFilterDocument
            )
        except ValueError:
            try:
                doge(JoinChannelRequest("@DogePlugin"))
            except:
                await doge.send_message(
                    BOTLOG_CHATID,
                    "**🚨 I couldn't install plugins of @DogePlugin!\n\
                        \n\
                        🧩 Please join @DogePlugin channel,\n\
                        if you want external plugins.**",
                )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await doge.download_media(
                await doge.get_messages(-1001482657964, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(dogeplugininstall())


if Config.DOGEHUB == True:

    async def dogehubinstall():
        try:
            documentss = await doge.get_messages(
                -1001233006670, None, filter=InputMessagesFilterDocument
            )
        except ValueError:
            try:
                doge(JoinChannelRequest("@DogeHub"))
            except:
                await doge.send_message(
                    BOTLOG_CHATID,
                    "**🚨 I couldn't install hub plugins of @DogeHub!\n\
                        \n\
                        🍑 Please join @DogeHub channel,\n\
                        if you want external hub plugins.**",
                )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await doge.download_media(
                await doge.get_messages(-1001233006670, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            flag = True
            check = 0
            while flag:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(dogehubinstall())
