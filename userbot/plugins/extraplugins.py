# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import path
from pathlib import Path

from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputMessagesFilterDocument

from ..utils import load_module
from . import BOTLOG_CHATID, PLUGIN_CHANNEL, Config, doge, install_pip

plugin_category = "bot"


if PLUGIN_CHANNEL:

    async def install():
        documentss = await doge.get_messages(
            PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(documentss.total)
        for module in range(total):
            plugin_to_install = documentss[module].id
            plugin_name = documentss[module].file.name
            if path.exists(f"userbot/plugins/{plugin_name}"):
                return
            downloaded_file_name = await doge.download_media(
                await doge.get_messages(PLUGIN_CHANNEL, ids=plugin_to_install),
                "userbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            check = 0
            while True:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(install())


if Config.DOGEPLUGIN:

    async def dogeplugininstall():
        try:
            documentss = await doge.get_messages(
                -1001482657964, None, filter=InputMessagesFilterDocument
            )
        except ValueError:
            try:
                await doge(JoinChannelRequest("@DogePlugin"))
                documentss = await doge.get_messages(
                    -1001482657964, None, filter=InputMessagesFilterDocument
                )
            except BaseException:
                await doge.send_message(
                    BOTLOG_CHATID,
                    "**🚨 I couldn't install plugins of @DogePlugin!\n\
                        \n\
                        🧩 Please join @DogePlugin channel,\n\
                        if you want extra plugins.**",
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
            check = 0
            while True:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(dogeplugininstall())


if Config.DOGEHUB:

    async def dogehubinstall():
        try:
            documentss = await doge.get_messages(
                -1001233006670, None, filter=InputMessagesFilterDocument
            )
        except ValueError:
            try:
                await doge(JoinChannelRequest("@DogeHUB"))
                documentss = await doge.get_messages(
                    -1001233006670, None, filter=InputMessagesFilterDocument
                )
            except BaseException:
                await doge.send_message(
                    BOTLOG_CHATID,
                    "**🚨 I couldn't install hub plugins of @DogeHUB!\n\
                        \n\
                        🍑 Please join @DogeHUB channel,\n\
                        if you want extra hub plugins.**",
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
            check = 0
            while True:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except ModuleNotFoundError as e:
                    install_pip(e.name)
                    check += 1
                    if check > 5:
                        break

    doge.loop.create_task(dogehubinstall())
