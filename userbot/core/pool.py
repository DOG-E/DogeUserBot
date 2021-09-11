# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import get_running_loop
from concurrent.futures import Future, ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, Callable

from motor.frameworks.asyncio import _EXECUTOR

from .logger import logging

_LOG = logging.getLogger(__name__)
_LOG_STR = "<<< ----  %s  ---- >>>"


def submit_thread(func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Future:
    """Submit thread to thread pool."""
    return _EXECUTOR.submit(func, *args, **kwargs)


def run_in_thread(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Run in a thread."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = get_running_loop()
        return await loop.run_in_executor(_EXECUTOR, partial(func, *args, **kwargs))

    return wrapper


def _get() -> ThreadPoolExecutor:
    return _EXECUTOR


def _stop():
    _EXECUTOR.shutdown()
    # pylint: disable=protected-access
    _LOG.info(_LOG_STR, f"Stopped Pool: {_EXECUTOR._max_workers} workers")


# pylint: disable=protected-access
_LOG.info(_LOG_STR, f"Started Pool: {_EXECUTOR._max_workers} workers")
