# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import create_subprocess_exec, get_event_loop, run_coroutine_threadsafe
from asyncio.subprocess import PIPE
from functools import partial
from shlex import split
from typing import Tuple

from telethon.tl.functions.messages import SaveGifRequest
from telethon.tl.types import InputDocument

from ...core.logger import logging

LOGS = logging.getLogger(__name__)


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = split(cmd)
    process = await create_subprocess_exec(*args, stdout=PIPE, stderr=PIPE)
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
        LOGS.info(str(e))
