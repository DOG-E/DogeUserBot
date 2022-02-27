# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import dump, load
from math import ceil
from os.path import join as ospjoin
from random import choice
from re import compile, findall
from time import time
from uuid import uuid4

from telethon import Button
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.types import (
    InputBotInlineMessageMediaAuto,
    InputBotInlineResult,
    InputWebDocument,
)
from youtubesearchpython import VideosSearch

from userbot import doge, tr

from ..Config import Config
from ..helpers.functions import rand_key
from ..helpers.functions.utube import (
    download_button,
    get_yt_video_id,
    get_ytthumb,
    result_formatter,
    ytsearch_data,
)
from ..sql_helper.globals import gvar
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner
from .logger import logging

LOGS = logging.getLogger(__name__)

BTN_URL_REGEX = compile(r"(\[([^\[]+?)\]\<(?:/{0,2})(.+?)(:same)?\>)")


def back_menu(back):
    text = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
    \n🐾 Yᴀʀᴅıᴍᴄı\n\
    \n◽ Doɢᴇ oғ {gvar('mention')}**"
    buttons = [(Button.inline("ℹ️️ Bɪʟɢɪ", data="check"), ), (
            Button.inline(
                f"👮‍♂️ Aᴅᴍɪɴ ({len(GRP_INFO['admin'])})",
                data="admin_menu",
            ),
            Button.inline(
                f"🐶 Doɢᴇ ({len(GRP_INFO['bot'])})",
                data="bot_menu",
            ),
        ), (
            Button.inline(
                f"🎈 Eɢ̆ʟᴇɴᴄᴇ ({len(GRP_INFO['fun'])})",
                data="fun_menu",
            ),
            Button.inline(
                f"🪀 Çᴇşɪᴛʟɪ ({len(GRP_INFO['misc'])})",
                data="misc_menu",
            ),
        ), (
            Button.inline(
                f"🧰 Aʀᴀç ({len(GRP_INFO['tool'])})",
                data="tool_menu",
            ),
            Button.inline(
                f"🍑 Hᴜʙ ({len(GRP_INFO['hub'])})",
                data="hub_menu",
            ),
        )]
    buttons.append(get_back_button(back))
    return text, buttons


def main_menu():
    text = f"**🐶 Doɢᴇ UsᴇʀBoᴛ\
    \n🐾 Yᴀʀᴅıᴍᴄı\n\
    \n◽ Doɢᴇ oғ {gvar('mention')}**"
    buttons = [(Button.inline("ℹ️️ Bɪʟɢɪ", data="check"), ), (
            Button.inline(
                f"👮‍♂️ Aᴅᴍɪɴ ({len(GRP_INFO['admin'])})",
                data="admin_menu",
            ),
            Button.inline(
                f"🐶 Doɢᴇ ({len(GRP_INFO['bot'])})",
                data="bot_menu",
            ),
        ), (
            Button.inline(
                f"🎈 Eɢ̆ʟᴇɴᴄᴇ ({len(GRP_INFO['fun'])})",
                data="fun_menu",
            ),
            Button.inline(
                f"🪀 Çᴇşɪᴛʟɪ ({len(GRP_INFO['misc'])})",
                data="misc_menu",
            ),
        ), (
            Button.inline(
                f"🧰 Aʀᴀç ({len(GRP_INFO['tool'])})",
                data="tool_menu",
            ),
            Button.inline(
                f"🍑 Hᴜʙ ({len(GRP_INFO['hub'])})",
                data="hub_menu",
            ),
        ), (Button.inline("⛔ KAPAT ⛔", data="close"), )]
    return text, buttons


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


def get_back_button(name):
    return [Button.inline("⬅️️ Gᴇʀɪ", data=f"{name}")]


def command_in_category(cname):
    cmds = 0
    for i in GRP_INFO[cname]:
        for _ in PLG_INFO[i]:
            cmds += 1
    return cmds


def paginate_help(
    page_number,
    loaded_plugins,
    prefix,
    plugins=True,
    category_plugins=None,
    category_pgno=0,
):  # sourcery no-metrics
    try:
        number_of_rows = int(gvar("NO_OF_ROWS_IN_HELP") or 6)
    except (ValueError, TypeError):
        number_of_rows = 6
    try:
        number_of_cols = int(gvar("NO_OF_COLUMNS_IN_HELP") or 2)
    except (ValueError, TypeError):
        number_of_cols = 2

    HELP_EMOJI = gvar("HELP_EMOJI") or " "
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    if len(HELP_EMOJI) == 2:
        if plugins:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_prev(1)_command_{prefix}_{page_number}",
                )
                for x in helpable_plugins
            ]

        else:
            modules = [
                Button.inline(
                    f"{HELP_EMOJI[0]} {x} {HELP_EMOJI[1]}",
                    data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
                )
                for x in helpable_plugins
            ]

    elif plugins:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_prev(1)_command_{prefix}_{page_number}",
            )
            for x in helpable_plugins
        ]

    else:
        modules = [
            Button.inline(
                f"{HELP_EMOJI} {x} {HELP_EMOJI}",
                data=f"{x}_cmdhelp_{prefix}_{page_number}_{category_plugins}_{category_pgno}",
            )
            for x in helpable_plugins
        ]

    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))

    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))

    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )

    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))

    elif len(modules) % number_of_cols == 2:
        pairs.append((modules[-2], modules[-1]))

    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if plugins:
        if len(pairs) > number_of_rows:
            pairs = (pairs[
                modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
            ] + [(Button.inline(
                        "⏪",
                        data=f"{prefix}_prev({modulo_page})_plugin",
                    ), Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"), Button.inline(
                        "⏩",
                        data=f"{prefix}_next({modulo_page})_plugin",
                    )), (Button.inline("⛔ Kᴀᴘᴀᴛ", data="close"), )])

        else:
            pairs = pairs + [
                (
                    Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"),
                    Button.inline("⛔ Kᴀᴘᴀᴛ", data="close"),
                )
            ]


    elif len(pairs) > number_of_rows:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                Button.inline(
                    "⏪",
                    data=f"{prefix}_prev({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
                Button.inline(
                    "⏩",
                    data=f"{prefix}_next({modulo_page})_command_{category_plugins}_{category_pgno}",
                ),
            ),
            (
                Button.inline(
                    "⬅️️ Gᴇʀɪ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"),
                Button.inline("⛔ Kᴀᴘᴀᴛ", data="close"),
            ),
        ]


    else:
        if category_pgno < 0:
            category_pgno = len(pairs) + category_pgno
        pairs = pairs + [
            (
                Button.inline(
                    "⬅️️ Gᴇʀɪ",
                    data=f"back_plugin_{category_plugins}_{category_pgno}",
                ),
                Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"),
                Button.inline("⛔ Kᴀᴘᴀᴛ", data="close"),
            )
        ]

    return pairs


@doge.bot.on(InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id

    if query_user_id == int(gvar("OWNER_ID")) or query_user_id in Config.SUDO_USERS:
        hmm = compile("troll (.*) (.*)")
        match = findall(hmm, query)
        inf = compile("s (.*) (.*)")
        match2 = findall(inf, query)
        hid = compile("hide (.*)")
        match3 = findall(hid, query)

        if query.startswith("ㅤ"):
            buttons = [
                (
                    Button.url("🐶 Doɢᴇ UsᴇʀBoᴛ", "https://t.me/DogeUserBot"),
                    Button.inline(f"🐾 Bɪʟɢɪ", data="infos"),
                )
            ]
            ALIVE_PIC = gvar("ALIVE_PIC")
            IALIVE_PIC = gvar("IALIVE_PIC")
            if IALIVE_PIC:
                DOG = [x for x in IALIVE_PIC.split()]
                PIC = list(DOG)
                I_IMG = choice(PIC)
            if not IALIVE_PIC and ALIVE_PIC:
                DOG = [x for x in ALIVE_PIC.split()]
                PIC = list(DOG)
                I_IMG = choice(PIC)
            elif not IALIVE_PIC:
                I_IMG = None or "https://telegra.ph/file/4d498bf8dfc83a93f418b.png"
            if I_IMG and I_IMG.endswith((".jpg", "jpeg", ".png")):
                result = builder.photo(
                    I_IMG,
                    # title="🐶 Doge UserBot Alive",
                    text=query,
                    buttons=buttons,
                )
            elif I_IMG:
                result = builder.document(
                    I_IMG,
                    title="🐶 Doge UserBot Çalışıyor ⚡",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="🐶 Doge UserBot Çalışıyor ⚡",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)

        elif query.startswith("Inline buttons"):
            markdown_note = query[14:]
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
                if n_escapes % 2 == 0:
                    buttons.append(
                        (match.group(2), match.group(3), bool(match.group(4)))
                    )
                    note_data += markdown_note[prev : match.start(1)]
                    prev = match.end(1)
                elif n_escapes % 2 == 1:
                    note_data += markdown_note[prev:to_check]
                    prev = match.start(1) - 1
                else:
                    break
            else:
                note_data += markdown_note[prev:]
            message_text = note_data.strip()
            tl_ib_buttons = ibuild_keyboard(buttons)
            result = builder.article(
                title=f"🐶 Doge UserBot Buton Özelleştirme",
                text=message_text,
                buttons=tl_ib_buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

        elif match:
            query = query[7:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            troll = ospjoin("./userbot", "troll.txt")
            try:
                jsondata = load(open(troll))
            except Exception:
                jsondata = False
            try:
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        teledoge = f"@{u.username}"
                    else:
                        teledoge = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    teledoge = f"[user](tg://user?id={u})"
            except ValueError:
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    teledoge = f"@{u.username}"
                else:
                    teledoge = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time() * 2)
            newtroll = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline(f"🔐 Mᴇsᴀᴊı Gösᴛᴇʀ", data=f"troll_{timestamp}")]
            result = builder.article(
                title=f"🐶 Doge UserBot Trol Mesajı",
                text=f"🤡 Bu mesaja sadece {teledoge} erişemez!",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newtroll)
                dump(jsondata, open(troll, "w"))
            else:
                dump(newtroll, open(troll, "w"))

        elif match2:
            query = query[2:]
            user, txct = query.split(" ", 1)
            builder = event.builder
            secret = ospjoin("./userbot", "secrets.txt")
            try:
                jsondata = load(open(secret))
            except Exception:
                jsondata = False
            try:
                u = int(user)
                try:
                    u = await event.client.get_entity(u)
                    if u.username:
                        teledoge = f"@{u.username}"
                    else:
                        teledoge = f"[{u.first_name}](tg://user?id={u.id})"
                    u = int(u.id)
                except ValueError:
                    teledoge = f"[user](tg://user?id={u})"
            except ValueError:
                try:
                    u = await event.client.get_entity(user)
                except ValueError:
                    return
                if u.username:
                    teledoge = f"@{u.username}"
                else:
                    teledoge = f"[{u.first_name}](tg://user?id={u.id})"
                u = int(u.id)
            except Exception:
                return
            timestamp = int(time() * 2)
            newsecret = {str(timestamp): {"userid": u, "text": txct}}

            buttons = [Button.inline(f"🔐 Mᴇsᴀᴊı Gösᴛᴇʀ", data=f"s_{timestamp}")]
            result = builder.article(
                title=f"🐶 Doge UserBot Gizli Mesaj",
                text=f"🔒 Bu {teledoge} için gizli bir nesajdır, sadece {teledoge} görebilir.",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newsecret)
                dump(jsondata, open(secret, "w"))
            else:
                dump(newsecret, open(secret, "w"))

        elif match3:
            query = query[5:]
            builder = event.builder
            hide = ospjoin("./userbot", "hide.txt")
            try:
                jsondata = load(open(hide))
            except Exception:
                jsondata = False
            timestamp = int(time() * 2)
            newhide = {str(timestamp): {"text": query}}

            buttons = [Button.inline(f"🔏 Mᴇsᴀᴊı Gösᴛᴇʀ", data=f"hide_{timestamp}")]
            result = builder.article(
                title=f"🐶 Doge UserBot Gizlenmiş Mesaj",
                text="ㅤ",
                buttons=buttons,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(newhide)
                dump(jsondata, open(hide, "w"))
            else:
                dump(newhide, open(hide, "w"))

        elif string == "help":
            HELP_PIC = gvar("HELP_PIC")
            if HELP_PIC:
                DOG = [x for x in HELP_PIC.split()]
                PIC = list(DOG)
                HP_IMG = choice(PIC)
            else:
                HP_IMG = None or "https://telegra.ph/file/d578c86d2bc21a1790c77.png"
            _result = main_menu()
            if HP_IMG is not None and HP_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    file=HP_IMG,
                    # title="🐶 Doɢᴇ UsᴇʀBoᴛ",
                    # description="Yᴀʀᴅıᴍ Mᴇɴüsü",
                    text=_result[0],
                    buttons=_result[1],
                )
            elif HP_IMG:
                result = builder.document(
                    HP_IMG,
                    title=f"🐶 Doɢᴇ UsᴇʀBoᴛ",
                    description=f"Yᴀʀᴅıᴍ Mᴇɴüsü",
                    text=query,
                    buttons=_result[1],
                )
            else:
                result = builder.article(
                    title="🐶 Doɢᴇ UsᴇʀBoᴛ",
                    description=f"Yᴀʀᴅıᴍ Mᴇɴüsü",
                    text=query,
                    buttons=_result[1],
                )
            await event.answer([result] if result else None)

        elif str_y[0].lower() == "yt" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                search = VideosSearch(str_y[1].strip(), limit=15)
                resp = (search.result()).get("result")
                if len(resp) == 0:
                    found_ = False
                else:
                    outdata = await result_formatter(resp)
                    key_ = rand_key()
                    ytsearch_data.store_(key_, outdata)
                    buttons = [
                        Button.inline(
                            f"1 - {len(outdata)}",
                            data=f"ytdl_next_{key_}_1",
                        ),
                        Button.inline(
                            f"📜 Hᴇᴘsɪɴɪ Lɪsᴛᴇʟᴇ",
                            data=f"ytdl_listall_{key_}_1",
                        ),
                        Button.inline(
                            f"📥 İɴᴅɪʀ",
                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',
                        ),
                    ]
                    caption = outdata[1]["message"]
                    photo = await get_ytthumb(outdata[1]["video_id"])
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo = InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link,
                    description=f"📥 İɴᴅɪʀ",
                    thumb=photo,
                    content=photo,
                    send_message=InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="🙁 Bunu bulamadım.",
                    text=f"🚨 `{str_y[1]}` için sonuç bulunamadı.",
                    description="INVALID",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="🙁 Bunu bulamadım.",
                            text=f"🚨 `{str_y[1]}` için sonuç bulunamadı.",
                            description="INVALID",
                        )
                    ]
                )

        elif string == "pmpermit":
            buttons = [
                Button.inline(
                    text=f"🪐 Sᴇçᴇɴᴇᴋʟᴇʀɪ Gösᴛᴇʀ", data="show_pmpermit_options"
                ),
            ]
            PM_PIC = gvar("PM_PIC")
            if PM_PIC:
                DOG = [x for x in PM_PIC.split()]
                PIC = list(DOG)
                DOG_IMG = choice(PIC)
            else:
                DOG_IMG = None or "https://telegra.ph/file/559cc3291fe1fc3521998.png"
            query = gvar("pmpermit_text")
            if DOG_IMG and DOG_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    DOG_IMG,
                    # title="🐶 Doge UserBot PMPermit Modülü",
                    text=query,
                    buttons=buttons,
                )
            elif DOG_IMG:
                result = builder.document(
                    DOG_IMG,
                    title="🐶 Doge UserBot PMPermit Modülü",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="🐶 Doge UserBot PMPermit Modülü",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)

    else:
        DOGLOGO = "https://telegra.ph/file/3fe8dd882e2c6bfca0fc4.png"
        buttons = [
            (
                Button.url("🐶 Doɢᴇ UsᴇʀBoᴛ", "https://t.me/DogeUserBot"),
                Button.url(
                    f"🐕‍🦺 Dᴇsᴛᴇᴋ Gʀᴜʙᴜ",
                    "https://t.me/DogeSup",
                ),
            )
        ]
        markup = event.client.build_reply_markup(buttons)
        photo = InputWebDocument(
            url=DOGLOGO, size=0, mime_type="image/jpeg", attributes=[]
        )
        suplink = "https://t.me/DogeSup"
        text, msg_entities = await event.client._parse_message_text(
            f"**[🐶 Doɢᴇ UsᴇʀBoᴛ 🐾](https://t.me/DogeUserBot)**\
            \n\
            \n❤ Doge, Telegram'ı eğlenceli hale getirmek ve kullanımını kolaylaştırmak içindir.\n\
            \n**🐕‍🦺 Siz de bir Doge sahibi olmak istiyorsanız,\
            \n🐾 [Destek grubumuza]({suplink}) gelebilirsiniz!**",
            "md",
        )
        result = InputBotInlineResult(
            id=str(uuid4()),
            type="photo",
            title="🐶 Doge UserBot",
            description="🐕‍🦺 Sen de bir @DogeUserBot sahiplen!",
            url="https://t.me/DogeUserBot",
            thumb=photo,
            content=photo,
            send_message=InputBotInlineMessageMediaAuto(
                reply_markup=markup, message=text, entities=msg_entities
            ),
        )
        await event.answer([result] if result else None)


@doge.bot.on(CallbackQuery(data=compile(rb"mainmenu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    _result = main_menu()
    await event.edit(_result[0], buttons=_result[1], link_preview=False)


@doge.bot.on(CallbackQuery(data=compile(rb"backmainmenu")))
@check_owner
async def back_main_menu(event):
    _result = back_menu("start")
    await event.edit(_result[0], buttons=_result[1], link_preview=False)


@doge.bot.on(CallbackQuery(data=compile(b"start")))
@check_owner
async def back_to_start(event):
    buttons = [
        (Button.inline("🐕‍🦺 ʏᴀʀᴅɪᴍ", data="backmainmenu"),),
    ]
    # if not event.is_private and chat.id == BOTLOG_CHATID:
    await event.edit(
        f"**🐶 Hey!\
    \n🐾 Merhaba {gvar('mention')}!\n\
    \n💬 Sana nasıl yardımcı olabilirim?**\n",
        buttons=buttons,
    )


@doge.bot.on(CallbackQuery(data=compile(b"close")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    buttons = [
        (Button.inline(f"🐾 Mᴇɴᴜ", data="mainmenu"),),
    ]
    await event.edit(
        f"**[🐶 Doɢᴇ UsᴇʀBoᴛ 🐾](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅıᴍᴄı\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}**",
        buttons=buttons,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"check")))
async def on_plugin_callback_query_handler(event):
    text = f"🐶 𝗗𝗢𝗚𝗘 𝗨𝗦𝗘𝗥𝗕𝗢𝗧 🐾\
    \n🧩 Pʟᴜɢɪɴʟᴇʀ: {len(PLG_INFO)}\
    \n⌨️ Koᴍᴜᴛʟᴀʀ: {len(CMD_INFO)}\n\
    \n{tr}doge .c <komut>: Herhangi bir komut hakkında bilgi alır.\
    \n{tr}s <komut>: Herhangi bir komutu arar."
    await event.answer(text, cache_time=0, alert=True)


@doge.bot.on(CallbackQuery(data=compile(b"(.*)_menu")))
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    buttons = paginate_help(0, GRP_INFO[category], category)
    text = f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
    \n🐾 Yᴀʀᴅıᴍcı\n\
    \n◽ Doɢᴇ oғ {gvar('mention')}**\n\
    \n**🗃 Kᴀᴛᴇɢoʀɪ:** {category}\
    \n**🧩 Pʟᴜɢɪɴʟᴇʀ:** {len(GRP_INFO[category])}\
    \n**⌨️ Koᴍᴜᴛʟᴀʀ:** {command_in_category(category)}"
    await event.edit(text, buttons=buttons, link_preview=False)


@doge.bot.on(
    CallbackQuery(
        data=compile(b"back_([a-z]+)_([a-z_1-9]+)_([0-9]+)_?([a-z1-9]+)?_?([0-9]+)?")
    )
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    mtype = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    if mtype == "plugin":
        buttons = paginate_help(pgno, GRP_INFO[category], category)
        text = f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅıᴍcı\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}**\n\
        \n**🗃 Kᴀᴛᴇɢoʀɪ:** {category}\
        \n**🧩 Pʟᴜɢɪɴʟᴇʀ:** {len(GRP_INFO[category])}\
        \n**⌨️ Koᴍᴜᴛʟᴀʀ:** {command_in_category(category)}"

    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            pgno,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅıᴍcı\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}**\n\
        \n**🧩 Pʟᴜɢɪɴ:** {category}\
        \n**🗃 Kᴀᴛᴇɢoʀɪ:** {getkey(category)}\
        \n**⌨️ Koᴍᴜᴛʟᴀʀ:** {len(PLG_INFO[category])}"
    await event.edit(text, buttons=buttons, link_preview=False)


@doge.bot.on(
    CallbackQuery(data=compile(rb"(.*)_prev\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number - 1, GRP_INFO[category], category)
    else:
        category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
        category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
        buttons = paginate_help(
            current_page_number - 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
        text = f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅıᴍcı\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}**\n\
        \n**🧩 Pʟᴜɢɪɴ:** {category}\
        \n**🗃 Kᴀᴛᴇɢoʀɪ:** {getkey(category)}\
        \n**⌨️ Koᴍᴜᴛʟᴀʀ:** {len(PLG_INFO[category])}"
        try:
            return await event.edit(text, buttons=buttons, link_preview=False)
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
    await event.edit(buttons=buttons, link_preview=False)


@doge.bot.on(
    CallbackQuery(data=compile(rb"(.*)_next\((.+?)\)_([a-z]+)_?([a-z]+)?_?(.*)?"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    category = str(event.pattern_match.group(1).decode("UTF-8"))
    current_page_number = int(event.data_match.group(2).decode("UTF-8"))
    htype = str(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = event.pattern_match.group(4)
    if category_plugins:
        category_plugins = str(category_plugins.decode("UTF-8"))
    category_pgno = event.pattern_match.group(5)
    if category_pgno:
        category_pgno = int(category_pgno.decode("UTF-8"))
    if htype == "plugin":
        buttons = paginate_help(current_page_number + 1, GRP_INFO[category], category)
    else:
        buttons = paginate_help(
            current_page_number + 1,
            PLG_INFO[category],
            category,
            plugins=False,
            category_plugins=category_plugins,
            category_pgno=category_pgno,
        )
    await event.edit(buttons=buttons, link_preview=False)


@doge.bot.on(
    CallbackQuery(data=compile(b"(.*)_cmdhelp_([a-z_1-9]+)_([0-9]+)_([a-z]+)_([0-9]+)"))
)
@check_owner
async def on_plug_in_callback_query_handler(event):
    cmd = str(event.pattern_match.group(1).decode("UTF-8"))
    category = str(event.pattern_match.group(2).decode("UTF-8"))
    pgno = int(event.pattern_match.group(3).decode("UTF-8"))
    category_plugins = str(event.pattern_match.group(4).decode("UTF-8"))
    category_pgno = int(event.pattern_match.group(5).decode("UTF-8"))
    buttons = [
        (
            Button.inline(
                f"⬅️️ Gᴇʀɪ",
                data=f"back_command_{category}_{pgno}_{category_plugins}_{category_pgno}",
            ),
            Button.inline(
                f"🐾 Mᴇɴᴜ",
                data="mainmenu",
            ),
            Button.inline(
                f"⛔ Kᴀᴘᴀᴛ",
                data="close",
            ),
        ),
    ]
    text = f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
    \n🐾 Yᴀʀᴅıᴍcı\n\
    \n◽ Doɢᴇ oғ {gvar('mention')}**\n\
    \n**⌨️ Koᴍᴜᴛʟᴀʀ:** `{tr}{cmd}`\
    \n**🧩 Pʟᴜɢɪɴ:** {category}\
    \n**🗃 Kᴀᴛᴇɢoʀɪ:** {category_plugins}\n\
    \n**ℹ️ Bɪʟɢɪ:**\
    \n{CMD_INFO[cmd][0]}"
    await event.edit(text, buttons=buttons, link_preview=False)
