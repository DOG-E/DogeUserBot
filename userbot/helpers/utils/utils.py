# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import (
    create_subprocess_exec,
    create_subprocess_shell,
    get_event_loop,
    run_coroutine_threadsafe,
)
from asyncio.subprocess import PIPE
from functools import partial
from shlex import split
from typing import Tuple

from telethon.tl.functions.messages import SaveGifRequest
from telethon.tl.types import InputDocument

from ...core.logger import logging

LOGS = logging.getLogger(__name__)


async def cmdrun(cmd):
    process = await create_subprocess_shell(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = split(cmd)
    process = await create_subprocess_exec(
        *args,
        stdout=PIPE,
        stderr=PIPE,
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


def run_async(loop, coro):
    return run_coroutine_threadsafe(coro, loop).result()


async def unsavegif(e, m):
    try:
        await e.client(
            SaveGifRequest(
                id=InputDocument(
                    id=m.media.document.id,
                    access_hash=m.media.document.access_hash,
                    file_reference=m.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
