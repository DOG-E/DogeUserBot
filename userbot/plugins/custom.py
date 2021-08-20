from googletrans import LANGUAGES
from telethon.events import NewMessage
from validators.url import url as validatorsurl

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    addgvar,
    delgvar,
    doge,
    edl,
    eor,
    fsmessage,
    gvarstatus,
    lan,
    logging,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)

vlist = [
    "AFK",
    "ALIVE_PIC",
    "ALIVE_TEXT",
    "ALIVE",
    "PNSFW",
    "DOGELANG",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "STARTTEXT",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "CUSTOM_STICKER_PACKNAME",
]
oldvars = {
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@doge.bot_cmd(
    pattern="(set|get|del)dv(?: |$)([\s\S]*)",
    command=("dv", plugin_category),
    info={
        "header": "Set vars in database or check or delete",
        "description": "Set, fetch or delete values or vars directly in database without restart or heroku vars.\n\nYou can set multiple pics by giving space after links in alive, ialive, pm permit.",
        "flags": {
            "set": "To set new var in database or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
        },
        "var name": "**[List of Database Vars]**# TODO",
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
async def dvdvdv(event):  # sourcery no-metrics
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edl(
            event, f"**📑 Give correct var name from the list:\n\n**{vnlist}", 60
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
            if not vinfo and vname == "ALIVE" or "AFK":
                return await edl(
                    event,
                    "**💠 Check @DogeTemp for alive templates.**",
                    45,
                )

            if not vinfo:
                return await edl(
                    event, f"Give some values which you want to save for **{vname}**"
                )

            check = vinfo.split(" ")
            for i in check:
                if "PIC" in vname and not validatorsurl(i):
                    return await edl(event, "**Give me a correct link...**")

            addgvar(vname, vinfo)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#SET_DATAVAR\
                    \n**{vname}** is updated newly in database as below",
                )
                await event.client.send_message(BOTLOG_CHATID, vinfo, silent=True)
            await edl(
                event, f"📑 Value of **{vname}** is changed to:- `{vinfo}`", time=20
            )
        if cmd == "get":
            var_data = gvarstatus(vname)
            await edl(event, f"📑 Value of **{vname}** is  `{var_data}`", time=20)
        elif cmd == "del":
            delgvar(vname)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#DEL_DATAVAR\
                    \n**{vname}** is deleted from database",
                )
            await edl(
                event,
                f"📑 Value of **{vname}** is now deleted & set to default.",
                time=20,
            )
    else:
        await edl(
            event, f"**📑 Give correct var name from the list :\n\n**{vnlist}", time=60
        )


@doge.bot_cmd(
    pattern="(custom|de[gğ]i[sş]tir) (pmpermit|pmblock|startmsg|afk)$",
    command=("custom", plugin_category),
    info={
        "header": "To customize your DogeUserBot.",
        "options": {
            "pmpermit": "To customize pmpermit text. ",
            "pmblock": "To customize pmpermit block message.",
            "startmsg": "To customize startmsg of bot when some one started it.",
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
            "{afktime}": "see afk time for afk command",
        },
        "usage": "{tr}custom <option> reply",
        "NOTE": "You can set,fetch or delete these by `{tr}setdv` , `{tr}getdv` & `{tr}deldv` as well.",
    },
)
async def custom_dogeuserbot(event):
    "To customize your DogeUserBot."
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if text is None:
        return await edl(event, "__Reply to custom text or url__")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "startmsg":
        addgvar("STARTTEXT", text)
    if input_str == "afk":
        addgvar("AFK", text)
    await eor(event, f"__Your custom {input_str} has been updated__")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#SET_DATAVAR\
                    \n**{input_str}** is updated newly in database as below",
        )
        await event.client.send_message(BOTLOG_CHATID, text, silent=True)


@doge.bot_cmd(
    pattern="lang (ai|tocr|trt|tts|xg) ([\s\S]*)",
    command=("lang", plugin_category),
    info={
        "header": "Set language for many command.",
        "description": "For langugage codes check [this link](https://telegra.ph/LANGUAGE-CODES-07-01)",
        "options": {
            "ai": "Set language for chatbot(ai)",
            "tocr": "Set language for tocr command",
            "trt": "Set language for trt command",
            "tts": "Set language for tts command",
            "xg": "Set language for Xiaomi plugin",
        },
        "usage": "{tr}lang option <language codes>",
        "examples": [
            "{tr}lang ai tr",
            "{tr}lang tocr tur",
            "{tr}lang trt tr",
            "{tr}lang tts tr",
            "{tr}lang xg tr",
        ],
    },
)
async def lang_set(value):
    "To set language for trt comamnd."
    arg = value.pattern_match.group(2).lower()
    input_str = value.pattern_match.group(1)
    if arg not in LANGUAGES:
        return await eor(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TRT`:\n\n`{LANGUAGES}`",
        )
    LANG = LANGUAGES[arg]
    if input_str == "trt":
        addgvar("TRT_LANG", arg)
        await eor(value, f"`Language for Translator changed to {LANG.title()}.`")
    elif input_str == "tts":
        addgvar("TTS_LANG", arg)
        await eor(value, f"`Language for Translated TTS changed to {LANG.title()}.`")
    elif input_str == "tocr":
        addgvar("TOCR_LANG", arg)
        await eor(value, f"`Language for Translated OCR changed to {LANG.title()}.`")
    elif input_str == "ai":
        addgvar("AI_LANG", arg)
        await eor(value, f"`Language for chatbot is changed to {LANG.title()}.`")
    elif input_str == "xg":
        XLANGLIST = [
            "ar",
            "be",
            "bg",
            "cn",
            "cs",
            "de",
            "en",
            "es",
            "fr",
            "id",
            "it",
            "mx",
            "nl",
            "pl",
            "pt",
            "ru",
            "sq",
            "tr",
        ]
        if not arg and arg not in XLANGLIST:
            return await edl(
                value,
                "@XiaomiGeekBot Language List:\
                        \n\
                        \n🇸🇦 `ar` - Arabic (العربية)\
                        \n🇧🇾 `be` - Belarusian (Беларуская)\
                        \n🇧🇬 `bg` - Bulgarian (български език)\
                        \n🇨🇳 `cn` - Chinese (中文)\
                        \n🇨🇿 `cs` - Czech (česky)\
                        \n🇩🇪 `de` - German (Deutsch)\
                        \n🇬🇧 `en` - English (English)\
                        \n🇪🇸 `es` - Spanish (español)\
                        \n🇲🇽 `mx` - Spanish (Mexico) (español)\
                        \n🇫🇷 `fr` - French (français)\
                        \n🇮🇩 `id` - Indonesian (Bahasa Indonesia)\
                        \n🇮🇹 `it` - Italian (Italiano)\
                        \n🇳🇱 `nl` - Dutch (Nederlands)\
                        \n🇵🇱 `pl` - Polish (polski)\
                        \n🇵🇹 `pt` - Portuguese (Brazil) (Português)\
                        \n🇷🇺 `ru` - Russian (русский язык)\
                        \n🇦🇱 `sq` - Albanian (Shqip)\
                        \n🇹🇷 `tr` - Turkish (Türkçe)\
                        \n\
                        \n",
                time=60,
            )

        dogevent = await eor(value, lan("processing"))
        chat = "@XiaomiGeeksBot"
        async with doge.conversation(chat) as conv:
            if arg == "ar":
                xl = "ar - Arabic (العربية)"
            elif arg == "be":
                xl = "be - Belarusian (Беларуская)"
            elif arg == "bg":
                xl = "bg - Bulgarian (български език)"
            elif arg == "cn":
                xl = "zh-CN - Chinese (中文)"
            elif arg == "cs":
                xl = "cs - Czech (česky)"
            elif arg == "de":
                xl = "de - German (Deutsch)"
            elif arg == "en":
                xl = "en - English (English)"
            elif arg == "es":
                xl = "es-ES - Spanish (español)"
            elif arg == "fr":
                xl = "fr - French (français)"
            elif arg == "id":
                xl = "id - Indonesian (Bahasa Indonesia)"
            elif arg == "it":
                xl = "it - Italian (Italiano)"
            elif arg == "mx":
                xl = "es-MX - Spanish (Mexico) (español)"
            elif arg == "nl":
                xl = "nl - Dutch (Nederlands)"
            elif arg == "pl":
                xl = "pl - Polish (polski)"
            elif arg == "pt":
                xl = "pt-BR - Portuguese (Brazil) (Português)"
            elif arg == "ru":
                xl = "ru - Russian (русский язык)"
            elif arg == "sq":
                xl = "sq - Albanian (Shqip)"
            elif arg == "tr":
                xl = "tr - Turkish (Türkçe)"
            await fsmessage(
                event=value,
                text=xl,
                chat=chat,
            )
            response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
            respond = await response
            await dogevent.edit(f"**Changed @XiaomiGeeksBot language:**\n{respond}")
            await conv.mark_read()
            await conv.cancel_all()

    if BOTLOG:
        if input_str == "trt":
            await value.client.send_message(
                BOTLOG_CHATID, f"`Language for Translator changed to {LANG.title()}.`"
            )
        elif input_str == "tts":
            await value.client.send_message(
                BOTLOG_CHATID, f"`Language for TTS changed to {LANG.title()}.`"
            )
        elif input_str == "tocr":
            await value.client.send_message(
                BOTLOG_CHATID,
                f"`Language for Translated OCR changed to {LANG.title()}.`",
            )
        elif input_str == "ai":
            await value.client.send_message(
                BOTLOG_CHATID, f"`Language for chatbot is changed to {LANG.title()}.`"
            )
        elif input_str == "xg":
            await value.client.send_message(
                BOTLOG_CHATID,
                f"`Language for @XiaomiGeekBot is changed to {LANG.title()}.`",
            )
