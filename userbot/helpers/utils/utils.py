from asyncio import create_subprocess_exec, get_event_loop, run_coroutine_threadsafe
from asyncio.subprocess import PIPE
from functools import partial
from shlex import split
from typing import Tuple

from telethon.tl.functions.messages import SaveGifRequest
from telethon.tl.types import InputDocument

from ...core.logger import logging

LOGS = logging.getLogger(__name__)


# executing of terminal commands
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


async def unsavegif(event, teledoge):
    try:
        await event.client(
            SaveGifRequest(
                id=InputDocument(
                    id=teledoge.media.document.id,
                    access_hash=teledoge.media.document.access_hash,
                    file_reference=teledoge.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.info(str(e))
