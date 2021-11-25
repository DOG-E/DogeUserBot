# Copyright (C) 2020 Adek Maulana
#
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from hashlib import md5 as hashlibmd5
from math import floor
from re import match, sub
from time import time
from typing import Dict, Tuple

from telethon.errors.rpcerrorlist import MessageNotModifiedError

from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)
_TASKS: Dict[str, Tuple[int, int]] = {}


async def md5(fname: str) -> str:
    hash_md5 = hashlibmd5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = round(seconds, 2)
    tmp = (
        ((str(days) + f" day(s), ") if days else "")
        + ((str(hours) + f" hour(s), ") if hours else "")
        + ((str(minutes) + f" minute(s), ") if minutes else "")
        + ((str(seconds) + f" second(s), ") if seconds else "")
    )
    return tmp[:-2]


def readable_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (
        ((str(int(days)) + f" day(s), ") if days else "")
        + ((str(int(hours)) + ":") if hours else "00:")
        + ((str(int(minutes)) + ":") if minutes else "00:")
        + (str(int(seconds)) if seconds else "00")
    )


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2 ** 20,
        "MB": 2 ** 20,
        "G": 2 ** 30,
        "GB": 2 ** 30,
        "T": 2 ** 40,
        "TB": 2 ** 40,
    }

    size = size.upper()
    if not match(r" ", size):
        size = sub(r"([KMGT])", r" \1", size)
    number, unit = [string.strip() for string in size.split()]
    return int(float(number) * units[unit])


async def progress(
    current,
    total,
    gdrive,
    start,
    prog_type,
    file_name=None,
    is_cancelled=False,
    delay=5,
):  # sourcery no-metrics
    if is_cancelled is True:
        raise CancelProcess
    task_id = f"{gdrive.chat_id}.{gdrive.id}"
    if current == total:
        if task_id not in _TASKS:
            return
        del _TASKS[task_id]
        try:
            await gdrive.edit("**⌛ Finalizing process...**")
        except MessageNotModifiedError:
            pass
        except Exception as e:
            LOGS.error(str(e))
        return
    now = time()
    if task_id not in _TASKS:
        _TASKS[task_id] = (now, now)
    start, last = _TASKS[task_id]
    elapsed_time = now - start
    oldtmp = ""
    if (now - last) >= delay:
        _TASKS[task_id] = (start, now)
        percentage = current * 100 / total
        speed = current / elapsed_time
        eta = round((total - current) / speed)
        elapsed_time = round(elapsed_time)
        if "upload" in prog_type.lower():
            status = "**📤 Uploading...**"
        elif "download" in prog_type.lower():
            status = "**📥 Downloading...**"
        else:
            status = "Unknown"
        progress_str = "{0}\n`[{1}{2}] {3}%`".format(
            status,
            "".join(Config.FINISHED_PROGRESS_STR for i in range(floor(percentage / 5))),
            "".join(
                Config.UNFINISHED_PROGRESS_STR
                for i in range(20 - floor(percentage / 5))
            ),
            round(percentage, 2),
        )
        tmp = (
            f"{progress_str}\n"
            f"`💾 {humanbytes(current)}/{humanbytes(total)}"
            f"🚀 {humanbytes(speed)}`\n"
            f"**⏲ Eᴛᴀ:** `{time_formatter(eta)}`\n"
            f"**⏱ Dᴜʀᴀᴛɪoɴ:** `{time_formatter(elapsed_time)}`"
        )
        if tmp != oldtmp:
            if file_name:
                await gdrive.edit(
                    f"**{prog_type}**\n\n"
                    f"**📋 Fɪʟᴇ Nᴀᴍᴇ:** `{file_name}`\n**📊 Sᴛᴀᴛᴜs:** {tmp}"
                )
            else:
                await gdrive.edit(f"**{prog_type}**\n\n" f"**📊 Sᴛᴀᴛᴜs:** {tmp}")
            oldtmp = tmp


class CancelProcess(Exception):
    """
    Cancel Process
    """
