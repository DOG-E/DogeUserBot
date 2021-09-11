# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from googletrans import LANGUAGES
from telegraph import Telegraph, resize_image, upload_file
from telegraph.exceptions import TelegraphException
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto, PeerUser

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    TELEGRAPH_SHORT_NAME,
    TEMP_DIR,
    dgvar,
    doge,
    edl,
    eor,
    fsmessage,
    gvar,
    lan,
    logging,
    newmsgres,
    sgvar,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)

telegraph = Telegraph()
r = telegraph.create_account(short_name=TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

vlist = [
    "ALIVE_PIC",
    "IALIVE_PIC",
    "DEFAULT_PIC",
    "DIGITAL_PIC",
    "HELP_PIC",
    "PM_PIC",
    "AFK",
    "AFKBIO",
    "AFKRBIO",
    "ALIVE",
    "ALIVE_NAME",
    "ALIVE_TEXT",
    "AUTONAME",
    "AUTOUS",
    "CHANGE_TIME",
    "CUSTOM_STICKER_PACKNAME",
    "DEFAULT_BIO",
    "HELP_EMOJI",
    "HELP_TEXT",
    "MAX_FLOOD_IN_PMS",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "PM_BLOCK",
    "PM_TEXT",
    "SNIP_CMDSET",
    "START_TEXT",
    "PERMISSION_TO_ALL_GLOBAL_DATA_VARIABLES",
]
alist = [
    "ANTISPAMBOT_BAN",
    "CURRENCY_API",
    "DEEPAI_API",
    "FBAN_GROUP_ID",
    "G_DRIVE_CLIENT_ID",
    "G_DRIVE_CLIENT_SECRET",
    "G_DRIVE_DATA",
    "G_DRIVE_FOLDER_ID",
    "G_DRIVE_INDEX_LINK",
    "GENIUS_API",
    "GITHUB_ACCESS_TOKEN",
    "GIT_REPO_NAME",
    "IBM_WATSON_CRED_URL",
    "IBM_WATSON_CRED_PASSWORD",
    "IPDATA_API",
    "LASTFM_API",
    "LASTFM_USERNAME",
    "LASTFM_PASSWORD_PLAIN",
    "LASTFM_SECRET",
    "OCRSPACE_API",
    "PRIVATE_CHANNEL_ID",
    "RANDOMSTUFF_API",
    "REMOVEBG_API",
    "SPAMWATCH_API",
    "SPOTIFY_DC",
    "SPOTIFY_KEY",
    "SS_API",
    "TG_2STEP_VERIFICATION_CODE",
    "WATCH_COUNTRY",
    "WEATHER_API",
    "WEATHER_CITY",
]


@doge.bot_cmd(
    pattern="([Ss]|[Gg]|[Dd])dog(?: |$)([\s\S]*)",
    command=("dog", plugin_category),
    info={
        "header": "Set vars in database or check or delete",
        "description": "Set, fetch or delete values or vars directly in database without restart or Heroku vars.\
        \nYou can set multiple pics by giving space after links in alive, ialive, pm permit.",
        "flags": {
            "s": "To set new var in database or modify the old var",
            "g": "To show the already existing var value.",
            "d": "To delete the existing value",
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
        "usage": [
            "{tr}sdog <var name> <var value>",
            "{tr}gdog <var name>",
            "{tr}ddog <var name>",
        ],
        "examples": [
            "{tr}sdog ALIVE_PIC <pic link>",
            "{tr}sdog ALIVE_PIC <pic link 1> <pic link 2>",
            "{tr}gdog ALIVE_PIC",
            "{tr}ddog ALIVE_PIC",
        ],
    },
)
async def dbsetter(event):  # sourcery no-metrics
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    apilist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(alist, start=1))
    if not vname:
        return await eor(
            event,
            f"**🪀 Give correct VAR name from the list:\n\n**{vnlist}\n\n\n**🔮 Give correct API name from the list:\n\n**{apilist}",
        )

    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        try:
            animated = reply.document.mime_type == "application/x-tgsticker"
        except:
            animated = None
        try:
            size = reply.file.size / 1024
            if (size >= 5000) or animated:
                await eor(event, "`Making message link...`")
                if reply.chat.username and type(reply.peer_id) != PeerUser:
                    username = reply.chat.username
                    msg_id = reply.id
                    vinfo = f"https://t.me/{username}/{msg_id}"
                else:
                    if reply.media:
                        custom = await reply.forward_to(BOTLOG_CHATID)
                        vinfo = f"{custom.id}"
            elif (type(reply.media) == MessageMediaDocument) or (
                type(reply.media) == MessageMediaPhoto
            ):
                await eor(event, "`Creating link...`")
                downloaded_file_name = await event.client.download_media(
                    reply, TEMP_DIR
                )
                try:
                    if downloaded_file_name.endswith((".webp")):
                        resize_image(downloaded_file_name)
                    media_urls = upload_file(downloaded_file_name)
                    vinfo = f"https://telegra.ph{media_urls[0]}"

                except AttributeError:
                    return await eor(event, f"{lan('errr')} `While making link.`")

                except TelegraphException as exc:
                    return await eor(event, f"{lan('errr')}\n➡️ `{str(exc)}`")

        except AttributeError:
            vinfo = reply.text

    if vname in vlist:
        if cmd == "s":
            if not reply.media:
                if not vinfo and vname == ("ALIVE" or "AFK"):
                    return await edl(
                        event,
                        "**🪐 Check @DogeTemp for templates.**",
                        45,
                    )

                if len(vinfo) > 70 and vname == ("AFKBIO" or "AFKRBIO"):
                    return await edl(
                        event,
                        "**🚧 Max bio length is 70 characters.**",
                    )

                if not vinfo:
                    return await edl(
                        event,
                        f"Give some values which you want to save for **{vname}**",
                    )

            sgvar(vname, vinfo)
            if BOTLOG_CHATID:
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"#SET_DATAVAR\
                    \n**{vname}** is updated newly in database as below",
                )
                await doge.tgbot.send_message(BOTLOG_CHATID, vinfo, silent=True)
            await edl(
                event, f"🪀 Value of **{vname}** is changed to: `{vinfo}`", time=20
            )
        if cmd == "g":
            var_data = gvar(vname)
            await edl(event, f"🪀 Value of **{vname}** is  `{var_data}`", time=20)
        elif cmd == "d":
            var_data = gvar(vname)
            dgvar(vname)
            if BOTLOG_CHATID:
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"#DEL_DATAVAR\
                    \n**{vname}** is deleted from database\
                    \n\
                    \n🚮 Deleted: `{var_data}`",
                )
            await edl(
                event,
                f"🪀 Value of **{vname}** is now deleted & set to default.",
                time=20,
            )
    elif vname in apilist:
        apiname = vname
        apinfo = vinfo
        if cmd == "s":
            if not apinfo:
                return await edl(
                    event, f"Give some values which you want to save for **{apiname}**"
                )

            sgvar(apiname, apinfo)
            if BOTLOG_CHATID:
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"#SET_APIDATA\
                    \n**{apiname}** is updated newly in database as below",
                )
                await doge.tgbot.send_message(BOTLOG_CHATID, apinfo, silent=True)
            await edl(
                event,
                f"🔮 Value of **{apiname}** is changed.",
            )
        if cmd == "g":
            api_data = gvar(apiname)
            await edl(event, "**I sent API data to BOTLOG.**")
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"🔮 Value of **{apiname}** is  `{api_data}`",
            )
        elif cmd == "d":
            api_data = gvar(apiname)
            dgvar(apiname)
            if BOTLOG_CHATID:
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"#DEL_APIDATA\
                    \n**{apiname}** is deleted from database\
                    \n\
                    \n🚮 Deleted: `{api_data}`",
                )
            await edl(
                event,
                f"🔮 Value of **{apiname}** is now deleted & set to default.",
                time=20,
            )
    else:
        if gvar("PERMISSION_TO_ALL_GLOBAL_DATA_VARIABLES") is True:
            gvarname = vname
            gvarinfo = vinfo
            if cmd == "s":
                if not gvarinfo:
                    return await edl(
                        event,
                        f"⚙️ Give some values which you want to save for **{gvarname}**",
                    )

                sgvar(gvarname, gvarinfo)
                if BOTLOG_CHATID:
                    await doge.tgbot.send_message(
                        BOTLOG_CHATID,
                        f"#SET_GLOBALDATAVAR\
                        \n**⚙️ {gvarname}** is updated newly in database as below",
                    )
                    await doge.tgbot.send_message(BOTLOG_CHATID, gvarinfo, silent=True)
                await edl(
                    event,
                    f"⚙️ Value of **{gvarname}** is changed.",
                )
            if cmd == "g":
                gvardata = gvar(gvarname)
                await edl(event, "**I sent global data var to BOTLOG.**")
                await doge.tgbot.send_message(
                    BOTLOG_CHATID,
                    f"⚙️ Value of **{gvarname}** is  `{gvardata}`",
                )
            elif cmd == "d":
                gvardata = gvar(gvarname)
                dgvar(gvarname)
                if BOTLOG_CHATID:
                    await doge.tgbot.send_message(
                        BOTLOG_CHATID,
                        f"#DEL_GLOBALDATAVAR\
                        \n**{gvarname}** is deleted from database\
                        \n\
                        \n🚮 Deleted: `{gvardata}`",
                    )
                await edl(
                    event,
                    f"⚙️ Value of **{gvarname}** is now deleted & set to default.",
                    time=20,
                )
        else:
            await eor(
                event,
                f"**🪀 Give correct VAR name from the list:\n\n**{vnlist}\n\n\n**🔮 Give correct API name from the list:\n\n**{apilist}",
            )


@doge.bot_cmd(
    pattern="lang (ai|tocr|trt|tts|xg) ([\s\S]*)",
    command=("lang", plugin_category),
    info={
        "header": "Set language for many command.",
        "description": "For langugage codes check [this link](https://telegra.ph/LANGUAGE-CODES-07-01)",
        "options": {
            "ai": "For chatbot(ai)",
            "tocr": "For tocr command",
            "trt": "For trt command",
            "tts": "For tts command",
            "xg": "For Xiaomi plugin",
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
            f"`🚨 Invalid Language code!`\n**🌐 Available language codes:**\n\n`{LANGUAGES}`",
        )

    LANG = LANGUAGES[arg]
    if input_str == "trt":
        sgvar("TRT_LANG", arg)
        await eor(value, f"**🌐 Language for Translator changed to {LANG.title()}.**")
    elif input_str == "tts":
        sgvar("TTS_LANG", arg)
        await eor(
            value, f"**🌐 Language for Text to Speech changed to {LANG.title()}.**"
        )
    elif input_str == "tocr":
        sgvar("TOCR_LANG", arg)
        await eor(
            value, f"**🌐 Language for Translated OCR changed to {LANG.title()}.**"
        )
    elif input_str == "ai":
        sgvar("AI_LANG", arg)
        await eor(value, f"**🌐 Language for AI ChatBot changed to {LANG.title()}.**")
    elif input_str == "xg":
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
            try:
                await fsmessage(value, xl, chat=chat)
            except UnboundLocalError:
                return await edl(
                    value,
                    "🌐 @XiaomiGeekBot Language List:\
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
                        \n🇹🇷 `tr` - Turkish (Türkçe)",
                    time=60,
                )

            await newmsgres(conv, chat)
            await dogevent.edit(
                f"**🌐 Language for @XiaomiGeeksBot changed to {LANG.title()}.**"
            )
            await conv.mark_read()
            await conv.cancel_all()

    if BOTLOG:
        if input_str == "trt":
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"#SET_LANGUAGE\n\n**🌐 Language for Translator changed to {LANG.title()}.**",
            )
        elif input_str == "tts":
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"#SET_LANGUAGE\n\n**🌐 Language for Text to Speech changed to {LANG.title()}.**",
            )
        elif input_str == "tocr":
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"#SET_LANGUAGE\n\n**🌐 Language for Translated OCR changed to {LANG.title()}.**",
            )
        elif input_str == "ai":
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"#SET_LANGUAGE\n\n**🌐 Language for AI ChatBot is changed to {LANG.title()}.**",
            )
        elif input_str == "xg":
            await doge.tgbot.send_message(
                BOTLOG_CHATID,
                f"#SET_LANGUAGE\n\n**🌐 Language for @XiaomiGeekBot is changed to {LANG.title()}.**",
            )
