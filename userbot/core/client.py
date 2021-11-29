# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from datetime import datetime
from inspect import stack as stacck
from pathlib import Path
from re import compile
from sys import exc_info
from traceback import format_exc, format_exception
from typing import Dict, List, Union

from telethon import TelegramClient, events
from telethon.errors import (
    AlreadyInConversationError,
    BotInlineDisabledError,
    BotResponseTimeoutError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

from ..Config import Config
from ..helpers.utils.events import checking
from ..helpers.utils.format import paste_message
from ..sql_helper.globals import gvar
from . import BOT_INFO, CMD_INFO, GRP_INFO, LOADED_CMDS, PLG_INFO
from .cmdinfo import _format_about
from .data import _sudousers_list, blacklist_chats_list, sudo_enabled_cmds
from .events import *
from .fasttelethon import download_file, upload_file
from .logger import logging
from .managers import edl
from .pluginManager import get_message_link, restart_script

LOGS = logging.getLogger(__name__)


class REGEX:
    def __init__(self):
        self.regex = ""
        self.regex1 = ""
        self.regex2 = ""


REGEX_ = REGEX()
sudo_enabledcmds = sudo_enabled_cmds()


class DogeUserBotClient(TelegramClient):
    def bot_cmd(
        self: TelegramClient,
        pattern: str or tuple = None,
        info: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
        or tuple = None,
        groups_only: bool = False,
        private_only: bool = False,
        allow_sudo: bool = True,
        edited: bool = True,
        forword=False,
        disable_errors: bool = False,
        command: str or tuple = None,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
        kwargs.setdefault("forwards", forword)
        if gvar("blacklist_chats") is not None:
            kwargs["blacklist_chats"] = True
            kwargs["chats"] = blacklist_chats_list()
        stack = stacck()
        previous_stack_frame = stack[1]
        file_test = Path(previous_stack_frame.filename)
        file_test = file_test.stem.replace(".py", "")
        if command is not None:
            command = list(command)
            if not command[1] in BOT_INFO:
                BOT_INFO.append(command[1])
            try:
                if file_test not in GRP_INFO[command[1]]:
                    GRP_INFO[command[1]].append(file_test)
            except BaseException:
                GRP_INFO.update({command[1]: [file_test]})
            try:
                if command[0] not in PLG_INFO[file_test]:
                    PLG_INFO[file_test].append(command[0])
            except BaseException:
                PLG_INFO.update({file_test: [command[0]]})
            if not command[0] in CMD_INFO:
                CMD_INFO[command[0]] = [_format_about(info)]
        if pattern is not None:
            if (
                pattern.startswith(r"\#")
                or not pattern.startswith(r"\#")
                and pattern.startswith(r"^")
            ):
                REGEX_.regex1 = REGEX_.regex2 = compile(pattern)
            else:
                reg1 = "\\" + Config.CMDSET
                reg2 = "\\" + Config.SUDO_CMDSET
                REGEX_.regex1 = compile(reg1 + pattern)
                REGEX_.regex2 = compile(reg2 + pattern)

        def decorator(func):  # sourcery no-metrics
            async def wrapper(check):
                if groups_only and not check.is_group:
                    return await edl(check, "`🐾 Bunun bir grup olduğunu sanmıyorum.`")

                if private_only and not check.is_private:
                    return await edl(
                        check, "`🐾 Bunun kişisel bir sohbet olduğunu sanmıyorum.`"
                    )

                try:
                    await func(check)
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("🚨 Mesaj önceki mesajla aynı.")
                except MessageIdInvalidError:
                    LOGS.error("🚨 Mesaj silindi ya da bulunamadı.")
                except BotInlineDisabledError:
                    await edl(check, "`🚨 Botunuzun satır içi modu kapalı.`")
                except ChatSendStickersForbiddenError:
                    await edl(
                        check,
                        "`🚨 Bu sohbette çıkartma gönderemiyorum.`",
                    )
                except BotResponseTimeoutError:
                    await edl(
                        check,
                        "`🚨 Bottan yanıt alamadım.`",
                    )
                except ChatSendMediaForbiddenError:
                    await edl(
                        check,
                        "`🚨 Bu sohbette medya gönderemiyorum.`",
                    )
                except AlreadyInConversationError:
                    await edl(
                        check,
                        "`🚨 Mevcut sohbetle zaten bir konuşma gerçekleşiyor. 🔃 Bir süre sonra tekrar deneyin.`",
                    )
                except ChatSendInlineForbiddenError:
                    await edl(
                        check,
                        "`🚨 Bu sohbette satır içi mesajlar gönderemiyorum.`",
                    )
                except FloodWaitError as e:
                    LOGS.error(
                        f"🚨 {e.seconds} saniye flood wait nedeniyle engellendi. Lütfen {e.seconds} saniye bekleyin ve tekrar deneyin."
                    )
                    await check.delete()
                    await sleep(e.seconds + 5)
                except BaseException as e:
                    LOGS.exception(e)
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = "💥💥💥💥 UYARI 💥💥💥💥\
                        \n💠 Bu metin sadece buraya yazıldı,\
                        \n💠 Yalnızca bu hata ve gerçekleştiği tarihi kaydettik,\
                        \n💠 Gizliliğinize saygı duyuyoruz,\
                        \n💠 Burada herhangi bir gizli veri varsa,\
                        \n💠 Bu hatayı bildirmeyebilirsiniz.\
                        \n💠 Kimse verilerinizi göremez.\
                        \n\
                        \n⚠️⚠️⚠️ USERBOT-HATA-RAPORU-BAŞLANGICI ⚠️⚠️⚠️\
                        \n📅 Tarih: {d}\
                        \n👥 Grup ID'si: {cid}\
                        \n👤 Gönderici ID: {sid}\
                        \n🔗 Mesaj Linki: {msg}\
                        \n\
                        \n➡️ Tetikleyici Komut:\
                        \n{t}\
                        \n\
                        \nℹ️ Geri İzleme Mekanizması:\
                        \n{f}\
                        \n\
                        \n🚨 Hata Metni:\
                        \n{e}".format(
                            d=date,
                            cid=str(check.chat_id),
                            sid=str(check.sender_id),
                            msg=await check.client.get_msg_link(check),
                            t=str(check.text),
                            f=str(format_exc()),
                            e=str(exc_info()[1]),
                        )
                        new = {
                            "error": str(exc_info()[1]),
                            "date": datetime.now(),
                        }
                        ftext += "\n\n"
                        ftext += "⚠️⚠️⚠️ USERBOT-HATA-RAPORU-SONU ⚠️⚠️⚠️"
                        pastelink = await paste_message(
                            ftext,
                            pastetype="t",
                            markdown=False,
                            title="🐶 Doɢᴇ UsᴇʀBoᴛ Hᴀᴛᴀ Rᴀᴘᴏʀᴜ 🐾",
                        )
                        text = "**🐶 Doɢᴇ UsᴇʀBoᴛ Hᴀᴛᴀ Rᴀᴘᴏʀᴜ 🐾**"
                        text += "\n\n"
                        text += f"**🚨 Hata Raporu:** [{new['error']}]({pastelink})"
                        text += "\n\n"
                        link = f"[BURAYA](https://t.me/DogeSup)"
                        text += "__💬 Eğer isterseniz buraya bildirebilirisiniz.__"
                        text += "\n\n"
                        text += "🐾 Bu mesajı {} ilet.".format(link)
                        text += "\n\n"
                        text += (
                            "__**🦴 Hata ve tarih dışında hiçbir şey kaydedilmez!**__"
                        )
                        text += "\n\n"
                        text += f"**▫️ Tetikleyici Komut:** `{str(check.text)}`"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=True
                        )

            from .session import doge

            if func.__doc__ is not None:
                CMD_INFO[command[0]].append((func.__doc__).strip())
            if pattern is not None:
                if command is not None:
                    if command[0] in LOADED_CMDS and wrapper in LOADED_CMDS[command[0]]:
                        return None
                    try:
                        LOADED_CMDS[command[0]].append(wrapper)
                    except BaseException:
                        LOADED_CMDS.update({command[0]: [wrapper]})
                if edited:
                    doge.add_event_handler(
                        wrapper,
                        MessageEdited(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
                doge.add_event_handler(
                    wrapper,
                    NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                )
                if allow_sudo and gvar("sudoenable") is not None:
                    if command is None or command[0] in sudo_enabledcmds:
                        if edited:
                            doge.add_event_handler(
                                wrapper,
                                MessageEdited(
                                    pattern=REGEX_.regex2,
                                    from_users=_sudousers_list(),
                                    **kwargs,
                                ),
                            )
                        doge.add_event_handler(
                            wrapper,
                            NewMessage(
                                pattern=REGEX_.regex2,
                                from_users=_sudousers_list(),
                                **kwargs,
                            ),
                        )
            else:
                if file_test in LOADED_CMDS and func in LOADED_CMDS[file_test]:
                    return None
                try:
                    LOADED_CMDS[file_test].append(func)
                except BaseException:
                    LOADED_CMDS.update({file_test: [func]})
                if edited:
                    doge.add_event_handler(func, events.MessageEdited(**kwargs))
                doge.add_event_handler(func, events.NewMessage(**kwargs))
            return wrapper

        return decorator

    def shiba_cmd(
        self: TelegramClient,
        disable_errors: bool = False,
        edited: bool = False,
        **kwargs,
    ) -> callable:  # sourcery no-metrics
        kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)

        def decorator(func):
            async def wrapper(check):
                try:
                    await func(check)
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModifiedError:
                    LOGS.error("🚨 Mesaj önceki mesajla aynı.")
                except MessageIdInvalidError:
                    LOGS.error("🚨 Mesaj silindi ya da bulunamadı.")
                except BaseException as e:
                    LOGS.exception(e)
                    if not disable_errors:
                        if Config.PRIVATE_GROUP_BOT_API_ID == 0:
                            return
                        date = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                        ftext = "💥💥💥💥 UYARI 💥💥💥💥\
                        \n💠 Bu metin sadece buraya yazıldı,\
                        \n💠 Yalnızca bu hata ve gerçekleştiği tarihi kaydettik,\
                        \n💠 Gizliliğinize saygı duyuyoruz,\
                        \n💠 Burada herhangi bir gizli veri varsa,\
                        \n💠 Bu hatayı bildirmeyebilirsiniz.\
                        \n💠 Kimse verilerinizi göremez.\
                        \n\
                        \n⚠️⚠️⚠️ ASİSTAN-HATA-RAPORU-BAŞLANGICI ⚠️⚠️⚠️\
                        \n📅 Tarih: {d}\
                        \n👥 Grup ID'si: {cid}\
                        \n👤 Gönderici ID: {sid}\
                        \n🔗 Mesaj Linki: {msg}\
                        \n\
                        \n➡️ Tetikleyici Komut:\
                        \n{t}\
                        \n\
                        \nℹ️ Geri İzleme Mekanizması:\
                        \n{f}\
                        \n\
                        \n🚨 Hata Metni:\
                        \n{e}".format(
                            d=date,
                            cid=str(check.chat_id),
                            sid=str(check.sender_id),
                            msg=await check.client.get_msg_link(check),
                            t=str(check.text),
                            f=str(format_exc()),
                            e=str(exc_info()[1]),
                        )
                        new = {
                            "error": str(exc_info()[1]),
                            "date": datetime.now(),
                        }
                        ftext += "\n\n"
                        ftext += "⚠️⚠️⚠️ ASİSTAN-HATA-RAPORU-SONU ⚠️⚠️⚠️"
                        pastelink = await paste_message(
                            ftext,
                            pastetype="t",
                            markdown=False,
                            title="🐶 Doɢᴇ Asɪsᴛᴀɴ Hᴀᴛᴀ Rᴀᴘᴏʀᴜ 🐾",
                        )
                        text = "**🐶 Doɢᴇ Asɪsᴛᴀɴ Hᴀᴛᴀ Rᴀᴘᴏʀᴜ 🐾**"
                        text += "\n\n"
                        text += f"**🚨 Hata Raporu:** [{new['error']}]({pastelink})"
                        text += "\n\n"
                        link = f"[BURAYA](https://t.me/DogeSup)"
                        text += "__💬 Eğer isterseniz buraya bildirebilirisiniz.__"
                        text += "\n\n"
                        text += "🐾 Bu mesajı {} ilet.".format(link)
                        text += "\n\n"
                        text += (
                            "__**🦴 Hata ve tarih dışında hiçbir şey kaydedilmez!**__"
                        )
                        text += "\n\n"
                        text += f"**▫️ Tetikleyici Komut:** `{str(check.text)}`"
                        await check.client.send_message(
                            Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=True
                        )

            from .session import doge

            if edited is True:
                doge.tgbot.add_event_handler(func, events.MessageEdited(**kwargs))
            else:
                doge.tgbot.add_event_handler(func, events.NewMessage(**kwargs))

            return wrapper

        return decorator

    async def get_traceback(self, exc: Exception) -> str:
        return "".join(
            format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        )

    def _kill_running_processes(self) -> None:
        """Tüm çalışan asyncio alt işlemkerini durdurur"""
        for _, process in self.running_processes.items():
            try:
                process.kill()
                LOGS.debug("Devam eden %d durduruldu.", process.pid)
            except Exception as e:
                LOGS.debug(e)
        self.running_processes.clear()


DogeUserBotClient.fast_download_file = download_file
DogeUserBotClient.fast_upload_file = upload_file
DogeUserBotClient.reload = restart_script
DogeUserBotClient.get_msg_link = get_message_link
DogeUserBotClient.check_testcases = checking
try:
    send_message_check = TelegramClient.send_message
except AttributeError:
    DogeUserBotClient.send_message = send_message
    DogeUserBotClient.send_file = send_file
    DogeUserBotClient.edit_message = edit_message
