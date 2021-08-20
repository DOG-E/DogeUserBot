from re import compile

from telethon import Button
from telethon.events import CallbackQuery

from ..core.decorators import check_owner
from ..core.logger import logging
from ..sql_helper.globals import addgvar
from . import doge

LOGS = logging.getLogger(__name__)


@doge.tgbot.on(CallbackQuery(data=compile(r"^chg_of_decision_")))
@check_owner
async def chg_of_decision_(event: CallbackQuery):
    buttons = [
        (
            Button.inline(text="⚠ Yᴇs ɪ'ᴍ +18", data="age_verification_true"),
            Button.inline(text="🔞 No ɪ'ᴍ ɴoᴛ", data="age_verification_false"),
        )
    ]
    await event.edit(
        text="**ARE YOU OLD ENOUGH FOR THIS?**",
        file="https://telegra.ph/file/238f2c55930640e0e8c56.jpg",
        buttons=buttons,
    )


@doge.tgbot.on(CallbackQuery(data=compile(r"^age_verification_true")))
@check_owner
async def age_verification_true(event: CallbackQuery):
    buttons = [
        (
            Button.inline(
                text="⬅ No, ɪ'ᴠᴇ ᴄʜᴀɴɢᴇᴅ oᴘɪɴɪoɴ",
                data="chg_of_decision_",
            ),
            Button.inline(
                text="✅ Yᴇs ɪ'ᴍ sᴜʀᴇ",
                data="yes_im_sure",
            ),
        )
    ]
    await event.edit(
        text="**Are you sure want to open this?**",
        file="https://telegra.ph/file/31836a76386fd3d49a099.jpg",
        buttons=buttons,
    )


@doge.tgbot.on(CallbackQuery(data=compile(r"^yes_im_sure")))
@check_owner
async def yes_im_sure(event: CallbackQuery):
    await event.answer("✅ Yes I'm sure!", alert=False)
    addgvar("PNSFW", True)
    buttons = [
        Button.inline(
            text="⛔ Cʟosᴇ",
            data="close_this",
        ),
    ]
    await event.edit(
        text="**All right.\nNow you can do whatever want.**",
        file="https://telegra.ph/file/efebf3a24dd260896d662.jpg",
        buttons=buttons,
    )


@doge.tgbot.on(CallbackQuery(data=compile(r"^age_verification_false")))
@check_owner
async def age_verification_false(event: CallbackQuery):
    buttons = [
        (
            Button.inline(
                text="⬅ I'ᴠᴇ ᴄʜᴀɴɢᴇᴅ oᴘɪɴɪoɴ",
                data="chg_of_decision_",
            ),
            Button.inline(
                text="⛔ Exɪᴛ",
                data="close_this",
            ),
        )
    ]
    await event.edit(
        text="**GO AWAY KID!**",
        file="https://telegra.ph/file/b7e740bbda31d43d510ab.jpg",
        buttons=buttons,
    )


@doge.tgbot.on(CallbackQuery(data=compile(r"^close_this")))
@check_owner
async def close_this(event: CallbackQuery):
    await event.answer("⛔ Closed!", alert=False)
    await event.delete()
