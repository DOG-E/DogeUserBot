from asyncio import create_subprocess_exec, get_event_loop
from asyncio.subprocess import PIPE
from os import _exit, environ, execle
from re import compile
from sys import executable as sysexecutable

from telethon import TelegramClient

from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from .logger import logging

LOGS = logging.getLogger(__name__)

package_patern = compile(r"([\w-]+)(?:=|<|>|!)")
github_patern = compile(r"(?:https?)?(?:www.)?(?:github.com/)?([\w\-.]+/[\w\-.]+)/?")
github_raw_pattern = compile(
    r"(?:https?)?(?:raw.)?(?:githubusercontent.com/)?([\w\-.]+/[\w\-.]+)/?"
)
trees_pattern = "https://api.github.com/repos/{}/git/trees/master"
raw_pattern = "https://raw.githubusercontent.com/{}/master/{}"


async def get_pip_packages(requirements):
    """Get a list of all the pacakage's names."""
    if requirements:
        packages = requirements
    else:
        cmd = await create_subprocess_exec(
            sysexecutable.replace(" ", "\\ "),
            "-m",
            "pip",
            "freeze",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, _ = await cmd.communicate()
        packages = stdout.decode("utf-8")
    tmp = package_patern.findall(packages)
    return [package.lower() for package in tmp]


async def install_pip_packages(packages):
    """Install pip packages."""
    args = ["-m", "pip", "install", "--upgrade", "--user"]
    cmd = await create_subprocess_exec(
        sysexecutable.replace(" ", "\\ "),
        *args,
        *packages,
        stdout=PIPE,
        stderr=PIPE,
    )
    await cmd.communicate()
    return cmd.returncode == 0


def run_async(func: callable):
    """Run async functions with the right event loop."""
    loop = get_event_loop()
    return loop.run_until_complete(func)


async def restart_script(client: TelegramClient, teledoge):
    """Restart the current script."""
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [teledoge.chat_id, teledoge.id])
    except Exception as e:
        LOGS.error(e)
    executable = sysexecutable.replace(" ", "\\ ")
    args = [executable, "-m", "userbot"]
    execle(executable, *args, environ)
    _exit(143)


async def get_message_link(client, event):
    chat = await event.get_chat()
    if event.is_private:
        return f"tg://openmessage?user_id={chat.id}&message_id={event.id}"
    return f"https://t.me/c/{chat.id}/{event.id}"
