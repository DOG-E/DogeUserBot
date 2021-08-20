from asyncio import sleep

from telethon.errors import FloodWaitError, MessageNotModifiedError
from telethon.events import CallbackQuery

from ..Config import Config
from ..sql_helper.globals import gvarstatus


def check_owner(func):
    async def wrapper(c_q: CallbackQuery):
        if c_q.query.user_id and (
            c_q.query.user_id == Config.OWNER_ID
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
                gvarstatus("HELP_TEXT")
                or "🐶 Doɢᴇ UsᴇʀBoᴛ\
                    \n\n\
                    🐾 wow!\
                    \nI'm not interested in you.\
                    \nYou aren't my master.\
                    \n\n\
                    🐕‍🦺 Adopt a @DogeUserBot too!"
            )
            await c_q.answer(
                HELP_TEXT,
                alert=True,
            )

    return wrapper
