# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from telethon.errors import FloodWaitError, MessageNotModifiedError
from telethon.events import CallbackQuery

from ..Config import Config
from ..sql_helper.globals import gvar
from .logger import logging

LOGS = logging.getLogger(__name__)


def check_owner(func):
    async def wrapper(c_q: CallbackQuery):
        if c_q.query.user_id and (
            c_q.query.user_id == int(gvar("OWNER_ID"))
            or c_q.query.user_id in Config.SUDO_USERS
        ):
            try:
                await func(c_q)
            except FloodWaitError as e:
                await sleep(e.seconds + 5)
            except MessageNotModifiedError:
                pass
        else:
            HELP_TEXT = (
                gvar("HELP_TEXT")
                or "🐶 Doɢᴇ UsᴇʀBoᴛ\n\n🐾 Hey! Sen benim sahibim değilsin!.\n\n🐕‍🦺 Kendine bir @DogeUserBot sahiplen!"
            )
            await c_q.answer(HELP_TEXT, alert=True)

    return wrapper


def sudo_owner(func):
    async def wrapper(event):
        if event.sender_id and (
            event.sender_id == int(gvar("OWNER_ID"))
            or event.sender_id in Config.SUDO_USERS
        ):
            try:
                await func(event)
            except FloodWaitError as e:
                await sleep(e.seconds + 5)
            except MessageNotModifiedError:
                pass
        else:
            return
    return wrapper
