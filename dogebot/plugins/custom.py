# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from urlextract import URLExtract
from validators.url import url

from dogebot import doge
from dogebot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()
vlist = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEXT",
    "ALIVE_TEMPLATE",
    "ALLOW_NSFW",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "START_TEXT",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "CUSTOM_STICKER_PACKNAME",
]

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@doge.doge_cmd(
    pattern="(set|get|del)dv(?:\s|$)([\s\S]*)",
    command=("dv", plugin_category),
    info={
        "header": "Set vars in database or Check or Delete",
        "description": "Set , Fetch or Delete values or vars directly in database without restart or heroku vars.\n\nYou can set multiple pics by giving space after links in alive, ialive, pm permit.",
        "flags": {
            "set": "To set new var in database or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "var name": "[list of vars](https://)",
        "usage": [
            "{tr}setdv <var name> <var value>",
            "{tr}getdv <var name>",
            "{tr}deldv <var name>",
        ],
        "examples": [
            "{tr}setdv ALIVE_PIC <pic link>",
            "{tr}setdv ALIVE_PIC <pic link 1> <pic link 2>",
            "{tr}getdv ALIVE_PIC",
            "{tr}deldv ALIVE_PIC",
        ],
    },
)
async def customize(event):  # sourcery no-metrics
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(
            event, f"**📑 Give correct var name from the list :\n\n**{vnlist}", time=60
        )
    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if vname in vlist:
        if vname in oldvars:
            vname = oldvars[vname]
        if cmd == "set":
            if not vinfo and vname == "ALIVE_TEMPLATE":
                return await edit_delete(event, f"Check @DogeAlive \nfor alives")
            if not vinfo:
                return await edit_delete(
                    event, f"Give some values which you want to save for **{vname}**"
                )
            check = vinfo.split(" ")
            for i in check:
                if (("PIC" in vname) or ("pic" in vname)) and not url(i):
                    return await edit_delete(event, "**Give me a correct link...**")
            addgvar(vname, vinfo)
            await edit_delete(
                event, f"📑 Value of **{vname}** is changed to :- `{vinfo}`", time=20
            )
        if cmd == "get":
            var_data = gvarstatus(vname)
            await edit_delete(
                event, f"📑 Value of **{vname}** is  `{var_data}`", time=20
            )
        elif cmd == "del":
            delgvar(vname)
            await edit_delete(
                event,
                f"📑 Value of **{vname}** is now deleted & set to default.",
                time=20,
            )
    else:
        await edit_delete(
            event, f"**📑 Give correct var name from the list :\n\n**{vnlist}", time=60
        )


@doge.doge_cmd(
    pattern="custom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("custom", plugin_category),
    info={
        "header": "To customize your DogeUserBot.",
        "options": {
            "pmpermit": "To customize pmpermit text. ",
            "pmblock": "To customize pmpermit block message.",
            "startmsg": "To customize startmsg of bot when some one started it.",
            "pmpic": "To customize pmpermit pic. Reply to media url or text containing media.",
        },
        "custom": {
            "{mention}": "mention user",
            "{first}": "first name of user",
            "{last}": "last name of user",
            "{fullname}": "fullname of user",
            "{username}": "username of user",
            "{userid}": "userid of user",
            "{my_first}": "your first name",
            "{my_last}": "your last name ",
            "{my_fullname}": "your fullname",
            "{my_username}": "your username",
            "{my_mention}": "your mention",
            "{totalwarns}": "totalwarns",
            "{warns}": "warns",
            "{remwarns}": "remaining warns",
        },
        "usage": [
            "{tr}custom <option> reply",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_dogeuserbot(event):
    "To customize your DogeUserBot."
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if not reply and text:
        return await edit_delete(event, "__Reply to custom text or url__")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "startmsg":
        addgvar("START_TEXT", text)
    if input_str == "pmpic":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(event, "`the given link is not supported`", 5)
        addgvar("pmpermit_pic", urls)
    await edit_or_reply(event, f"__Your custom {input_str} has been updated__")


@doge.doge_cmd(
    pattern="delcustom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("delcustom", plugin_category),
    info={
        "header": "To delete customization of your DogeUserBot.",
        "options": {
            "pmpermit": "To delete custom pmpermit text",
            "pmblock": "To delete custom pmpermit block message",
            "pmpic": "To delete custom pmpermit pic.",
            "startmsg": "To delete custom start message of bot when some one started it.",
        },
        "usage": [
            "{tr}delcustom <option>",
        ],
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_DogeUserBot(event):
    "To delete customization of your DogeUserBot."
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(event, "__You haven't customzied your pmpermit.__")
        delgvar("pmpermit_txt")
    if input_str == "pmblock":
        if gvarstatus("pmblock") is None:
            return await edit_delete(event, "__You haven't customzied your pmblock.__")
        delgvar("pmblock")
    if input_str == "pmpic":
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(event, "__You haven't customzied your pmpic.__")
        delgvar("pmpermit_pic")
    if input_str == "startmsg":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "__You haven't customzied your start msg in bot.__"
            )
        delgvar("START_TEXT")
    await edit_or_reply(
        event, f"__Successfully deleted your customization of {input_str}.__"
    )
