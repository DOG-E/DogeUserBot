from datetime import datetime
from inspect import stack as stacck
from re import compile, search
from sys import exc_info
from traceback import format_exc
from pathlib import Path

from .. import CMD_LIST, LOAD_PLUG, SUDO_LIST, dogeversion
from ..Config import Config
from ..core.data import _sudousers_list, blacklist_chats_list
from ..core.events import MessageEdited, NewMessage
from ..core.logger import logging
from ..core.session import doge
from ..helpers.utils.format import paste_message
from ..helpers.utils.utils import runcmd
from ..sql_helper.globals import gvarstatus

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
            if len(Config.CMDSET) == 2:
                dogreg = "^" + Config.CMDSET
                reg = Config.CMDSET[1]
            elif len(Config.CMDSET) == 1:
                dogreg = "^\\" + Config.CMDSET
                reg = Config.CMDSET
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
    if gvarstatus("blacklist_chats") is not None:
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
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            if len(Config.SUDO_CMDSET) == 2:
                dogreg = "^" + Config.SUDO_CMDSET
                reg = Config.SUDO_CMDSET[1]
            elif len(Config.SUDO_CMDSET) == 1:
                dogreg = "^\\" + Config.SUDO_CMDSET
                reg = Config.CMDSET
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
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = list(_sudousers_list())
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]
    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    # add blacklist chats, UB should not respond in these chats
    if gvarstatus("blacklist_chats") is not None:
        args["blacklist_chats"] = True
        args["chats"] = blacklist_chats_list()
    # add blacklist chats, UB should not respond in these chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    # check if the plugin should listen for outgoing 'messages'
    if gvarstatus("sudoenable") is not None:
        return NewMessage(**args)


def errors_handler(func):
    async def wrapper(check):
        try:
            await func(check)
        except BaseException:
            if Config.PRIVATE_GROUP_BOT_API_ID != 0:
                return
            date = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
            ftext = f"\nℹ DISCLAIMER:\
                        \nThis file is pasted ONLY here,\
                        \nwe logged only fact of error and date,\
                        \nwe respect your privacy,\
                        \nif you've any confidential data here,\
                        \nyou may not report this error.\
                        \nNo one will see your data.\
                        \n\
                        \n--------BEGIN DOGE USERBOT ERROR LOG--------\
                        \n\
                        \n🐶 Doge Version: {dogeversion}\
                        \n📅 Date: {date}\
                        \n👥 Group ID: {str(check.chat_id)}\
                        \n👤 Sender ID: {str(check.sender_id)}\
                        \n\
                        \n➡ Event Trigger:\n{str(check.text)}\
                        \n\
                        \nℹ Traceback Info:\n{str(format_exc())}\
                        \n\
                        \n🚨 Error Text:\n{str(exc_info()[1])}"
            new = {
                "error": str(exc_info()[1]),
                "date": datetime.now(),
            }

            ftext += "\n\
                        \n--------END DOGE USERBOT ERROR LOG--------"
            command = 'git log --pretty=format:"%an: %s" -5'
            ftext += "\n\n\n🐾 Last 5 Commits:\n"
            output = (await runcmd(command))[:2]
            result = output[0] + output[1]
            ftext += result
            pastelink = await paste_message(ftext, markdown=False)
            text = "**🐶 Doɢᴇ UsᴇʀBoᴛ Eʀʀoʀ Rᴇᴘoʀᴛ 🐾**\n\n"
            link = "[here](https://t.me/DogeSup)"
            text += "__💬 If you wanna you can report it.__\n\n"
            text += f"🐾 Forward this message {link}.\n\n"
            text += "__**🦴 Nothing is logged except of error and date!**__\n\n"
            text += f"**🚨 Error Report: **[{new['error']}]({pastelink})"
            await check.client.send_message(
                Config.PRIVATE_GROUP_BOT_API_ID, text, link_preview=False
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
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    if gvarstatus("blacklist_chats") is not None:
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
    if gvarstatus("blacklist_chats") is not None:
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
