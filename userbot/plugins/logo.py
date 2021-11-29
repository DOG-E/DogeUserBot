# Credits: @Jisan7509
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from glob import glob
from os import mkdir
from os import path as osp
from os import remove
from random import choice
from re import compile, match
from urllib.request import urlretrieve

from bs4 import BeautifulSoup
from PIL.Image import open as Imopen
from PIL.ImageColor import colormap
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from requests import get
from telethon.tl.types import InputMessagesFilterPhotos

from . import (
    _dogetools,
    clippy,
    convert_toimage,
    dgvar,
    doge,
    edl,
    eor,
    gvar,
    media_type,
    reply_id,
    sgvar,
)

plugin_category = "misc"
vars_list = {
    "lbg": "LOGO_BACKGROUND",
    "lfc": "LOGO_FONT_COLOR",
    "lfs": "LOGO_FONT_SIZE",
    "lfh": "LOGO_FONT_HEIGHT",
    "lfw": "LOGO_FONT_WIDTH",
    "lfsw": "LOGO_FONT_STROKE_WIDTH",
    "lfsc": "LOGO_FONT_STROKE_COLOR",
    "lf": "LOGO_FONT",
}


@doge.bot_cmd(
    pattern="(|s)logo(?: |$)([\s\S]*)",
    command=("logo", plugin_category),
    info={
        "h": "Make a logo in image or sticker",
        "d": "Just a fun purpose plugin to create logo in image or in sticker.",
        "f": {
            "s": "To create a logo in sticker instade of image.",
        },
        "u": [
            "{tr}logo <text>",
            "{tr}slogo <text>",
        ],
        "e": [
            "{tr}logo Doge",
            "{tr}slogo Doge",
        ],
    },
)
async def very(event):
    "To create a logo"
    cmd = event.pattern_match.group(1).lower()
    text = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not text and reply:
        text = reply.text
    if not text:
        return await edl(event, "**ಠ∀ಠ Gimmi text to make logo**")
    reply_to_id = await reply_id(event)
    dogevent = await eor(event, "**⏳ Processing...**")
    LOGO_FONT_SIZE = gvar("LOGO_FONT_SIZE") or 220
    LOGO_FONT_WIDTH = gvar("LOGO_FONT_WIDTH") or 2
    LOGO_FONT_HEIGHT = gvar("LOGO_FONT_HEIGHT") or 2
    LOGO_FONT_COLOR = gvar("LOGO_FONT_COLOR") or "red"
    LOGO_FONT_STROKE_WIDTH = gvar("LOGO_FONT_STROKE_WIDTH") or 0
    LOGO_FONT_STROKE_COLOR = gvar("LOGO_FONT_STROKE_COLOR") or None
    LOGO_BACKGROUND = (
        gvar("LOGO_BACKGROUND")
        or f"https://raw.githubusercontent.com/DOG-E/Source/DOGE/Material/LogoBackgrounds/black.jpg"
    )
    LOGO_FONT = (
        gvar("LOGO_FONT")
        or f"https://github.com/DOG-E/Source/raw/DOGE/Material/Fonts/streamster.ttf"
    )
    if not osp.isdir("./temp"):
        mkdir("./temp")
    if not osp.exists("temp/bg_img.jpg"):
        urlretrieve(LOGO_BACKGROUND, "temp/bg_img.jpg")
    img = Imopen("./temp/bg_img.jpg")
    draw = Draw(img)
    if not osp.exists("temp/logo.ttf"):
        urlretrieve(LOGO_FONT, "temp/logo.ttf")
    font = truetype("temp/logo.ttf", int(LOGO_FONT_SIZE))
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    try:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=int(LOGO_FONT_STROKE_WIDTH),
            stroke_fill=LOGO_FONT_STROKE_COLOR,
        )
    except OSError:
        draw.text(
            (
                (image_widthz - w) / float(LOGO_FONT_WIDTH),
                (image_heightz - h) / float(LOGO_FONT_HEIGHT),
            ),
            text,
            font=font,
            fill=LOGO_FONT_COLOR,
            stroke_width=0,
            stroke_fill=None,
        )
    file_name = "@DogeUserBot.png"
    img.save(file_name, "png")
    if cmd == "":
        await event.client.send_file(
            event.chat_id,
            file_name,
            reply_to=reply_to_id,
            force_document=True,
        )
    elif cmd == "s":
        await clippy(event.client, file_name, event.chat_id, reply_to_id)
    await dogevent.delete()
    if osp.exists(file_name):
        remove(file_name)


@doge.bot_cmd(
    pattern="(|c)lbg(?:\s|$)([\s\S]*)",
    command=("lbg", plugin_category),
    info={
        "h": "Change the background of logo",
        "d": "To change the background on which logo will created, in **bg** there few built-in backgrounds.",
        "f": {
            "c": "Custom background for logo, can set by giving a telegraph link or reply to media.",
        },
        "u": [
            "{tr}lbg <background color code>",
            "{tr}clbg <telegraph link / reply to media>",
        ],
        "e": [
            "{tr}lbg red",
            "{tr}clbg https://telegra.ph/blablabla.jpg",
        ],
    },
)
async def bad(event):
    "To change background of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    source = get("https://github.com/DOG-E/Source/tree/DOGE/Material/LogoBackgrounds")
    soup = BeautifulSoup(source.text, features="html.parser")
    links = soup.find_all("a", class_="js-navigation-open Link--primary")
    bg_name = []
    lbg_list = "**Available background names are here:**\n\n"
    for i, each in enumerate(links, start=1):
        dog = osp.splitext(each.text)[0]
        bg_name.append(dog)
        lbg_list += f"**{i}.**  `{dog}`\n"
    if osp.exists("./temp/bg_img.jpg"):
        remove("./temp/bg_img.jpg")
    if cmd == "c":
        reply_message = await event.get_reply_message()
        if not input_str and event.reply_to_msg_id and reply_message.media:
            if not osp.isdir("./temp"):
                mkdir("./temp")
            output = await _dogetools.media_to_pic(event, reply_message)
            convert_toimage(output[1], filename="./temp/bg_img.jpg")
            return await edl(event, "This media is successfully set as background.")
        if not input_str.startswith("https://t"):
            return await edl(
                event, "Give a valid Telegraph picture link, Or reply to a media."
            )
        sgvar("LOGO_BACKGROUND", input_str)
        return await edl(event, f"**Background for logo changed to:** `{input_str}`")
    if not input_str:
        return await edl(event, lbg_list, time=60)
    if input_str not in bg_name:
        dogevent = await eor(event, "`Give me a correct background name...`")
        await sleep(1)
        await edl(dogevent, lbg_list, time=60)
    else:
        string = f"https://raw.githubusercontent.com/DOG-E/Source/DOGE/Material/LogoBackgrounds/{input_str}.jpg"
        sgvar("LOGO_BACKGROUND", string)
        await edl(
            event,
            f"**Background for logo changed to:** `{input_str}`",
        )


@doge.bot_cmd(
    pattern="lf(|c|s|h|w|sc|sw)(?:\s|$)([\s\S]*)",
    command=("lf", plugin_category),
    info={
        "h": "Change text style for logo.",
        "d": "Customise logo font, font size, font position like text hight or width.",
        "f": {
            "c": "To change color of logo font.",
            "s": "To change size of logo font.",
            "h": "To change hight of logo font.",
            "w": "To change width of logo font.",
            "sw": "To change stroke width of logo font.",
            "sc": "To change stroke color of logo font.",
        },
        "u": [
            "{tr}lf <font name>",
            "{tr}lfc <logo font color>",
            "{tr}lfs <1-1000>",
            "{tr}lfh <10-100>",
            "{tr}lfw <10-100>",
            "{tr}lfsw <10-100>",
            "{tr}lfsc <logo font stroke color>",
        ],
        "e": [
            "{tr}lf genau-font.ttf",
            "{tr}lfc white",
            "{tr}lfs 120",
            "{tr}lfh 1",
            "{tr}lfw 8",
            "{tr}lfsw 5",
            "{tr}lfsc white",
        ],
    },
)
async def custom_font(event):
    "To customise logo font"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if cmd == "":
        source = get("https://github.com/DOG-E/Source/tree/DOGE/Material/Fonts")
        soup = BeautifulSoup(source.text, features="html.parser")
        links = soup.find_all("a", class_="js-navigation-open Link--primary")
        logo_font = []
        font_name = "**Available font names are here:**\n\n"
        for i, each in enumerate(links, start=1):
            dog = osp.splitext(each.text)[0]
            logo_font.append(dog)
            font_name += f"**{i}.**  `{dog}`\n"
        if not input_str:
            return await edl(event, font_name, time=80)
        if input_str not in logo_font:
            dogevent = await eor(event, "`Give me a correct font name...`")
            await sleep(1)
            await edl(dogevent, font_name, time=80)
        else:
            if " " in input_str:
                input_str = str(input_str).replace(" ", "%20")
            string = f"https://github.com/DOG-E/Source/raw/DOGE/Material/Fonts/{input_str}.ttf"
            if osp.exists("temp/logo.ttf"):
                remove("temp/logo.ttf")
                urlretrieve(
                    string,
                    "temp/logo.ttf",
                )
            sgvar("LOGO_FONT", string)
            await edl(
                event,
                f"**Font for logo changed to:** `{input_str}`",
            )
    elif cmd in ["c", "sc"]:
        fg_name = []
        for name, code in colormap.items():
            fg_name.append(name)
            fg_list = str(fg_name).replace("'", "`")
        if not input_str:
            return await edl(
                event,
                f"**Available color names are here:**\n\n{fg_list}",
                time=80,
            )
        if input_str not in fg_name:
            dogevent = await eor(event, "`Give me a correct color name...`")
            await sleep(1)
            await edl(
                dogevent,
                f"**Available color names are here:**\n\n{fg_list}",
                time=80,
            )
        elif cmd == "c":
            sgvar("LOGO_FONT_COLOR", input_str)
            await edl(
                event,
                f"**Foreground color for logo changed to:** `{input_str}`",
            )
        else:
            sgvar("LOGO_FONT_STROKE_COLOR", input_str)
            await edl(event, f"**Stroke color for logo changed to:** `{input_str}`")
    else:
        dog = compile(r"^\-?[1-9][0-9]*\.?[0-9]*")
        isint = match(dog, input_str)
        if not input_str or not isint:
            return await edl(
                event,
                f"**Give an integer value to set**",
            )
        if cmd == "s":
            input_str = int(input_str)
            if input_str > 0 and input_str <= 1000:
                sgvar("LOGO_FONT_SIZE", input_str)
                await edl(event, f"**Font size is changed to:** `{input_str}`")
            else:
                await edl(
                    event,
                    f"**Font size is between 0 - 1000, You can't set limit to:** `{input_str}`",
                )
        elif cmd == "w":
            input_str = float(input_str)
            if input_str > 0 and input_str <= 100:
                sgvar("LOGO_FONT_WIDTH", input_str)
                await edl(event, f"**Font width is changed to:** `{input_str}`")
            else:
                await edl(
                    event,
                    f"**Font width is between 0 - 100, You can't set limit to {input_str}",
                )
        elif cmd == "h":
            input_str = float(input_str)
            if input_str > 0 and input_str <= 100:
                sgvar("LOGO_FONT_HEIGHT", input_str)
                await edl(event, f"**Font hight is changed to:** `{input_str}`")
            else:
                await edl(
                    event,
                    f"**Font hight is between 0 - 100, You can't set limit to {input_str}",
                )
        elif cmd == "sw":
            input_str = int(input_str)
            if input_str > 0 and input_str <= 100:
                sgvar("LOGO_FONT_STROKE_WIDTH", input_str)
                await edl(event, f"**Font stroke width is changed to:** `{input_str}`")
            else:
                await edl(
                    event,
                    f"**Font stroke width size is between 0 - 100, You can't set limit to:** `{input_str}`",
                )


@doge.bot_cmd(
    pattern="(g|d|r)lvar(?:\s|$)([\s\S]*)",
    command=("lvar", plugin_category),
    info={
        "h": "Manage values which set for logo",
        "d": "To see which value have been set, or to delete a value or to reset all values.",
        "f": {
            "g": "Gets the value of the var which you set manually for logo.",
            "d": "Delete the value of the var which you set manually for logo.",
            "r": "Delete all the values of the vars which you set manually for logo & reset all changes.",
        },
        "u": [
            "{tr}glvar <var code>",
            "{tr}dlvar <var code>",
            "{tr}rlvar",
        ],
        "e": [
            "{tr}glvar lbg",
            "{tr}dlvar lfc",
        ],
    },
)
async def dog(event):
    "Manage all values of logo"
    cmd = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(2)
    if input_str in vars_list.keys():
        var = vars_list[input_str]
        if cmd == "g":
            var_data = gvar(var)
            await edl(event, f"📑 Value of **{var}** is  `{var_data}`", time=60)
        elif cmd == "d":
            if input_str == "lbg" and osp.exists("./temp/bg_img.jpg"):
                remove("./temp/bg_img.jpg")
            if input_str == "lf" and osp.exists("./temp/logo.ttf"):
                remove("./temp/logo.ttf")
            dgvar(var)
            await edl(
                event, f"📑 Value of **{var}** is now deleted & set to default.", time=60
            )
    elif not input_str and cmd == "r":
        dgvar("LOGO_BACKGROUND")
        dgvar("LOGO_FONT_COLOR")
        dgvar("LOGO_FONT")
        dgvar("LOGO_FONT_SIZE")
        dgvar("LOGO_FONT_HEIGHT")
        dgvar("LOGO_FONT_WIDTH")
        dgvar("LOGO_FONT_STROKE_COLOR")
        dgvar("LOGO_FONT_STROKE_WIDTH")
        if osp.exists("./temp/bg_img.jpg"):
            remove("./temp/bg_img.jpg")
        if osp.exists("./temp/logo.ttf"):
            remove("./temp/logo.ttf")
        await edl(
            event,
            "📑 Values for all vars deleted successfully & all settings reset.",
            time=20,
        )
    else:
        await edl(
            event,
            f"**📑 Give correct vars name:**\n__Correct Vars code list is:__\n\n1. `lbg`:** LOGO_BACKGROUND**\n2. `lfc`:** LOGO_FONT_COLOR**\n3. `lf`:** LOGO_FONT**\n4. `lfs`:** LOGO_FONT_SIZE**\n5. `lfh`:** LOGO_FONT_HEIGHT**\n6. `lfw`:** LOGO_FONT_WIDTH**",
            time=60,
        )


# Credits: TeamUltroid - github.com/teamultroid
@doge.bot_cmd(
    pattern="logoo([\s\S]*)",
    command=("logoo", plugin_category),
    info={
        "h": "Make a random logo",
        "d": "Generate a logo of the given text or reply to image, to write your text on it. Or reply to font file, to write with that font.",
        "u": "{tr}logoo <text>",
        "e": "{tr}logoo Doge",
    },
)
async def logo_generate(event):
    dogevent = await eor(event, "`Proccessing...`")
    name = event.pattern_match.group(1)
    if not name:
        await eor(dogevent, "`Give a name too!`")
    bg_, font_ = "", ""
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            if hasattr(temp.media, "document"):
                if "font" in temp.file.mime_type:
                    font_ = await temp.download_media()
                elif (".ttf" in temp.file.name) or (".otf" in temp.file.name):
                    font_ = await temp.download_media()
            elif "Photo" in media_type(temp.media):
                bg_ = await temp.download_media()
    else:
        pics = []
        async for i in event.client.iter_messages(
            "@Doge_File", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = choice(pics)
        bg_ = await id_.download_media()
        fpath_ = glob("userbot/helpers/resources/otherfonts/*")
        font_ = choice(fpath_)
    if not bg_:
        pics = []
        async for i in event.client.iter_messages(
            "@Doge_File", filter=InputMessagesFilterPhotos
        ):
            pics.append(i)
        id_ = choice(pics)
        bg_ = await id_.download_media()
    if not font_:
        fpath_ = glob("userbot/helpers/resources/otherfonts/*")
        font_ = choice(fpath_)
    if len(name) <= 8:
        fnt_size = 150
        strke = 10
    elif len(name) >= 9:
        fnt_size = 50
        strke = 5
    else:
        fnt_size = 130
        strke = 20
    img = Imopen(bg_)
    draw = Draw(img)
    font = truetype(font_, fnt_size)
    w, h = draw.textsize(name, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        name,
        font=font,
        fill=(255, 255, 255),
    )
    x = (image_width - w) / 2
    y = (image_height - h) / 2
    draw.text(
        (x, y), name, font=font, fill="white", stroke_width=strke, stroke_fill="black"
    )
    flnme = f"@DogeUserBot.png"
    img.save(flnme, "png")
    await dogevent.edit("`Done!`")
    if osp.exists(flnme):
        await event.client.send_file(
            event.chat_id,
            file=flnme,
            force_document=True,
        )
        remove(flnme)
        await dogevent.delete()
    if osp.exists(bg_):
        remove(bg_)
    if osp.exists(font_):
        if not font_.startswith("userbot/helpers/resources/otherfonts"):
            remove(font_)
