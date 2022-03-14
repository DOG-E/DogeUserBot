# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from inspect import stack as stacck
from pathlib import Path
from re import compile, search
from sys import exc_info
from traceback import format_exc

from .. import CMD_LIST, LOAD_PLUG, SUDO_LIST, tr
from ..Config import Config
from ..core.data import _sudousers_list, blacklist_chats_list
from ..core.events import MessageEdited, NewMessage
from ..core.logger import logging
from ..core.session import doge
from ..helpers.utils.format import paste_message
from ..sql_helper.globals import gvar

LOGS = logging.getLogger(__name__)


def admin_cmd(pattern=None, command=None, **args):  # sourcery no-metrics
    args["func"] = lambda e: e.via_bot_id is None
    stack = stacck()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            if len(tr) == 2:
                dogreg = "^" + tr
                reg = tr[1]
            elif len(tr) == 1:
                dogreg = "^\\" + tr
                reg = tr
            args["pattern"] = compile(dogreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        del args["allow_sudo"]
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    if gvar("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    return NewMessage(**args)


def sudo_cmd(pattern=None, command=None, **args):  # sourcery no-metrics
    args["func"] = lambda e: e.via_bot_id is None
    stack = stacck()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            if len((gvar("SUDO_CMDSET") or ".")) == 2:
                dogreg = "^" + (gvar("SUDO_CMDSET") or ".")
                reg = (gvar("SUDO_CMDSET") or ".")[1]
            elif len((gvar("SUDO_CMDSET") or ".")) == 1:
                dogreg = "^\\" + (gvar("SUDO_CMDSET") or ".")
                reg = tr
            args["pattern"] = compile(dogreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    if allow_sudo:
        args["from_users"] = list(_sudousers_list())
        args["incoming"] = True
        del args["allow_sudo"]
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    if gvar("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    if gvar("sudoenable") is not None:
        return NewMessage(**args)


def errors_handler(func):
    async def wrapper(check):
        try:
            await func(check)
        except BaseException:
            if Config.PRIVATE_GROUP_BOT_API_ID != 0:
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
                    \n----- USERBOT-HATA-RAPORU-BAŞLANGICI -----\
                    \n📅 Tarih: {d}\
                    \n👥 Grup ID: {cid}\
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
            ftext += "----- USERBOT-HATA-RAPORU-SONU -----"
            pastelink = await paste_message(ftext, markdown=False)
            text = "🐶 Doɢᴇ UsᴇʀBoᴛ Hᴀᴛᴀ Rᴀᴘᴏʀᴜ 🐾"
            text += "\n\n"
            text += f"**🚨 Hata Raporu:** [{new['error']}]({pastelink})"
            text += "\n\n"
            link = f"[BURAYA](https://t.me/DogeSup)"
            text += "__💬 Eğer isterseniz bunu bildirebilirisiniz.__"
            text += "\n\n"
            text += "🐾 Bu mesajı {} iletin.".format(link)
            text += "\n\n"
            text += "__**🦴 Hata ve tarih dışında hiçbir şey kaydedilmez!**__"
            text += "\n\n"
            text += f"**▫️ Tetikleyici Komut:** `{str(check.text)}`"
            await check.client.send_message(
                gvar("PRIVATE_GROUP_BOT_API_ID"), text, link_preview=True
            )

    return wrapper


def register(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = stacck()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", True)
    allow_sudo = args.get("allow_sudo", False)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    reg = compile("(.*)")
    if pattern is not None:
        try:
            cmd = search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
        del args["allow_sudo"]

    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    if gvar("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()

    def decorator(func):
        if not disable_edited:
            doge.add_event_handler(func, MessageEdited(**args))
        doge.add_event_handler(func, NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def command(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = stacck()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", None)
    allow_edited_updates = args.get("allow_edited_updates", False)
    args["incoming"] = args.get("incoming", False)
    args["outgoing"] = True
    if bool(args["incoming"]):
        args["outgoing"] = False
    try:
        if pattern is not None and not pattern.startswith("(?i)"):
            args["pattern"] = "(?i)" + pattern
    except BaseException:
        pass
    reg = compile("(.*)")
    if pattern is not None:
        try:
            cmd = search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        args["incoming"] = True
    del allow_sudo
    try:
        del args["allow_sudo"]
    except BaseException:
        pass
    if gvar("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()

    def decorator(func):
        if allow_edited_updates:
            doge.add_event_handler(func, MessageEdited(**args))
        doge.add_event_handler(func, NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except BaseException:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator
