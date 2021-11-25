# batmanpp and thorpp: @Nihinivi
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
from base64 import b64decode
from datetime import datetime
from os import getcwd, path, remove
from random import choice, randint
from re import compile, findall
from shutil import copy
from time import strftime
from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from requests import get
from telethon.errors import FloodWaitError
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from urlextract import URLExtract

from ..sql_helper.global_list import (
    add_to_list,
    get_collection_list,
    is_in_list,
    rm_from_list,
)
from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    CHANGE_TIME,
    DEFAULT_BIO,
    _dogeutils,
    _format,
    dgvar,
    doge,
    edl,
    gvar,
    logging,
    sgvar,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

DEFAULTUSERBIO = DEFAULT_BIO or "🐶 @DogeUserBot 🐾"
DEFAULTUSER = AUTONAME or ALIVE_NAME
FONT_FILE_TO_USE = "userbot/helpers/resources/fonts/spacemono_regular.ttf"
autopic_path = path.join(getcwd(), "userbot", "original_pic.png")
digitalpic_path = path.join(getcwd(), "userbot", "digital_pic.png")
autophoto_path = path.join(getcwd(), "userbot", "photo_pfp.png")
digitalpfp = gvar("DIGITAL_PIC") or "https://telegra.ph/file/aeaebe33b1f3988a0b690.jpg"
COLLECTION_STRINGS = {
    "batmanpfp_strings": [
        "awesome-batman-wallpapers",
        "batman-arkham-knight-4k-wallpaper",
        "batman-hd-wallpapers-1080p",
        "the-joker-hd-wallpaper",
        "dark-knight-joker-wallpaper",
    ],
    "thorpfp_strings": [
        "thor-wallpapers",
        "thor-wallpaper",
        "thor-iphone-wallpaper",
        "thor-wallpaper-hd",
    ],
}


async def autopicloop():
    AUTOPICSTART = gvar("autopic") == "true"
    if AUTOPICSTART and gvar("DEFAULT_PIC") is None:
        if BOTLOG:
            return await doge.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of autopic you need to set DEFAULT_PIC var`",
            )
        return
    if gvar("autopic") is not None:
        try:
            counter = int(gvar("autopic_counter"))
        except Exception as e:
            LOGS.warn(str(e))
    while AUTOPICSTART:
        if not path.exists(autopic_path):
            downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        file_test = im.rotate(counter, expand=False).save(autophoto_path, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await doge.upload_file(autophoto_path)
        try:
            await doge(UploadProfilePhotoRequest(file))
            remove(autophoto_path)
            counter += counter
            await sleep(CHANGE_TIME)
        except BaseException:
            return
        AUTOPICSTART = gvar("autopic") == "true"


async def custompfploop():
    CUSTOMPICSTART = gvar("CUSTOM_PFP") == "true"
    i = 0
    while CUSTOMPICSTART:
        if len(get_collection_list("CUSTOM_PFP_LINKS")) == 0:
            LOGS.error("No custom pfp images to set.")
            return
        pic = choice(list(get_collection_list("CUSTOM_PFP_LINKS")))
        urlretrieve(pic, "donottouch.jpg")
        file = await doge.upload_file("donottouch.jpg")
        try:
            if i > 0:
                await doge(
                    DeletePhotosRequest(await doge.get_profile_photos("me", limit=1))
                )
            i += 1
            await doge(UploadProfilePhotoRequest(file))
            remove("donottouch.jpg")
            await sleep(CHANGE_TIME)
        except BaseException:
            return
        CUSTOMPICSTART = gvar("CUSTOM_PFP") == "true"


async def digitalpicloop():
    DIGITALPICSTART = gvar("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        dog = str(
            b64decode(
                "dXNlcmJvdC9oZWxwZXJzL3Jlc291cmNlcy9vdGhlcmZvbnRzL2RpZ2l0YWwudHRm"
            )
        )[2:36]
        fnt = ImageFont.truetype(dog, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await doge.upload_file(autophoto_path)
        try:
            if i > 0:
                await doge(
                    DeletePhotosRequest(await doge.get_profile_photos("me", limit=1))
                )
            i += 1
            await doge(UploadProfilePhotoRequest(file))
            remove(autophoto_path)
            await sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvar("digitalpic") == "true"


async def bloom_pfploop():
    BLOOMSTART = gvar("bloom") == "true"
    if BLOOMSTART and gvar("DEFAULT_PIC") is None:
        if BOTLOG:
            return await doge.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of bloom you need to set DEFAULT_PIC var`",
            )
        return
    while BLOOMSTART:
        if not path.exists(autopic_path):
            downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        # RIP Danger zone Here no editing here plox
        R = randint(0, 256)
        B = randint(0, 256)
        G = randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        copy(autopic_path, autophoto_path)
        image = Image.open(autophoto_path)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(autophoto_path)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(autophoto_path)
        file = await doge.upload_file(autophoto_path)
        try:
            await doge(UploadProfilePhotoRequest(file))
            remove(autophoto_path)
            await sleep(CHANGE_TIME)
        except BaseException:
            return
        BLOOMSTART = gvar("bloom") == "true"


async def autoname_loop():
    AUTONAMESTART = gvar("autoname") == "true"
    while AUTONAMESTART:
        DM = strftime("%d-%m-%y")
        HM = strftime("%H:%M")
        name = f"⌚️ {HM} ||›  {DEFAULTUSER} ‹|| {DM} 📅"
        LOGS.info(name)
        try:
            await doge(UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await sleep(ex.seconds)
        await sleep(CHANGE_TIME)
        AUTONAMESTART = gvar("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvar("autobio") == "true"
    while AUTOBIOSTART:
        DMY = strftime("%d.%m.%Y")
        HM = strftime("%H:%M")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        LOGS.info(bio)
        try:
            await doge(UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await sleep(ex.seconds)
        await sleep(CHANGE_TIME)
        AUTOBIOSTART = gvar("autobio") == "true"


async def animeprofilepic(collection_images):
    rnd = randint(0, len(collection_images) - 1)
    pack = collection_images[rnd]
    pc = get("http://getwallpapers.com/collection/" + pack).text
    f = compile(r"/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + choice(f)
    if not path.exists("userbot/helpers/resources/fonts/roboto_regular.ttf"):
        urlretrieve(
            "https://github.com/DOG-E/Source/raw/DOGE/Material/Fonts/roboto_regular.ttf",
            "roboto_regular.ttf",
        )
    img = get(fy)
    with open("donottouch.jpg", "wb") as outfile:
        outfile.write(img.content)
    return "donottouch.jpg"


async def autopfp_start():
    if gvar("autopfp_strings") is not None:
        AUTOPFP_START = True
        string_list = COLLECTION_STRINGS[gvar("autopfp_strings")]
    else:
        AUTOPFP_START = False
    i = 0
    while AUTOPFP_START:
        await animeprofilepic(string_list)
        file = await doge.upload_file("donottouch.jpg")
        if i > 0:
            await doge(
                DeletePhotosRequest(await doge.get_profile_photos("me", limit=1))
            )
        i += 1
        await doge(UploadProfilePhotoRequest(file))
        await _dogeutils.runcmd("rm -rf donottouch.jpg")
        await sleep(CHANGE_TIME)
        AUTOPFP_START = gvar("autopfp_strings") is not None


@doge.bot_cmd(
    pattern="bpp$",
    command=("bpp", plugin_category),
    info={
        "header": "Changes profile pic with random batman pics every 1 minute",
        "description": "Changes your profile pic every 1 minute with random batman pics.\
        If you like to change the time then set CHANGE_TIME var with time (in seconds) between each change of profilepic.",
        "note": "To stop this do '{tr}end bpp'",
        "usage": "{tr}bpp",
    },
)
async def _(event):
    "To set random batman profile pics"
    if gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        return await edl(event, f"`{pfp_string} is already running.`")
    sgvar("autopfp_strings", "batmanpfp_strings")
    await event.edit("`Starting batman Profile Pic.`")
    await autopfp_start()


@doge.bot_cmd(
    pattern="tpp$",
    command=("tpp", plugin_category),
    info={
        "header": "Changes profile pic with random thor pics every 1 minute",
        "description": "Changes your profile pic every 1 minute with random thor pics.\
        If you like to change the time then set CHANGE_TIME var with time(in seconds) between each change of profilepic.",
        "note": "To stop this do '{tr}end tpp'",
        "usage": "{tr}tpp",
    },
)
async def _(event):
    "To set random thor profile pics"
    if gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        return await edl(event, f"`{pfp_string} is already running.`")
    sgvar("autopfp_strings", "thorpfp_strings")
    await event.edit("`Starting thor Profile Pic.`")
    await autopfp_start()


@doge.bot_cmd(
    pattern="autopic ?([\s\S]*)",
    command=("autopic", plugin_category),
    info={
        "header": "Changes profile pic every 1 minute with the custom pic with time",
        "description": "If you like to change the time interval for every new pic change \
            then set CHANGE_TIME var with time(in seconds) between each change of profilepic.",
        "options": "you can give integer input with cmd like 40,55,75 ..etc.\
             So that your profile pic will rotate with that specific angle",
        "note": "For functioning of this cmd you need to set DEFAULT_PIC var. \
            To stop this do '{tr}end autopic'",
        "usage": [
            "{tr}autopic",
            "{tr}autopic <any integer>",
        ],
    },
)
async def _(event):
    "To set time on your profile pic"
    if gvar("DEFAULT_PIC") is None:
        return await edl(
            event,
            "**Error**\n`For functing of autopic you need to set DEFAULT_PIC var`",
        )
    downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = int(input_str)
        except ValueError:
            input_str = 60
    elif gvar("autopic_counter") is None:
        sgvar("autopic_counter", 30)
    if gvar("autopic") is not None and gvar("autopic") == "true":
        return await edl(event, "`Autopic is already enabled`")
    sgvar("autopic", True)
    if input_str:
        sgvar("autopic_counter", input_str)
    await edl(event, "`Autopic has been started by my Master`")
    await autopicloop()


@doge.bot_cmd(
    pattern="dpp$",
    command=("dpp", plugin_category),
    info={
        "header": "Updates your profile pic every 1 minute with time on it",
        "description": "Deletes old profile pic and Update profile pic with new image with time on it.\
             You can change this image by setting DIGITAL_PIC var with telegraph image link",
        "note": "To stop this do '{tr}end dpp'",
        "usage": "{tr}dpp",
    },
)
async def _(event):
    "To set random colour pic with time to profile pic"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvar("digitalpic") is not None and gvar("digitalpic") == "true":
        return await edl(event, "`Digitalpic is already enabled`")
    sgvar("digitalpic", True)
    await edl(event, "`Digitalpp has been started by my Master`")
    await digitalpicloop()


@doge.bot_cmd(
    pattern="bloom$",
    command=("bloom", plugin_category),
    info={
        "header": "Changes profile pic every 1 minute with the random colour pic with time on it",
        "description": "If you like to change the time interval for every new pic chnage \
            then set CHANGE_TIME var with time(in seconds) between each change of profilepic.",
        "note": "For functioning of this cmd you need to set DEFAULT_PIC var. \
            To stop this do '{tr}end bloom'",
        "usage": "{tr}bloom",
    },
)
async def _(event):
    "To set random colour pic with time to profile pic"
    if gvar("DEFAULT_PIC") is None:
        return await edl(
            event,
            "**Error**\nFor functing of bloom you need to set DEFAULT_PIC var",
        )
    downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=True)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvar("bloom") is not None and gvar("bloom") == "true":
        return await edl(event, "`Bloom is already enabled`")
    sgvar("bloom", True)
    await edl(event, "`Bloom has been started by my Master`")
    await bloom_pfploop()


@doge.bot_cmd(
    pattern="c(ustom)?pp(?: |$)([\s\S]*)",
    command=("custompp", plugin_category),
    info={
        "header": "Set Your Custom pps",
        "description": "Set links of pic to use them as auto profile. You can use {tr}cpp or {tr}custompp as command",
        "flags": {
            "a": "To add links for custom pp",
            "r": "To remove links for custom pp",
            "l": "To get links of custom pp",
            "s": "To stop custom pp",
        },
        "usage": [
            "{tr}cpp or {tr}custompp <to start>",
            "{tr}cpp <flags> <links(optional)>",
        ],
        "examples": [
            "{tr}cpp",
            "{tr}cpp .l",
            "{tr}cpp .s",
            "{tr}cpp .a link1 link2...",
            "{tr}cpp .r link1 link2...",
        ],
    },
)
async def useless(event):  # sourcery no-metrics
    """Custom profile pics"""
    input_str = event.pattern_match.group(2)
    ext = findall(r".\w+", input_str)
    try:
        flag = ext[0].replace(".", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        flag = None
    list_link = get_collection_list("CUSTOM_PFP_LINKS")
    if flag is None:
        if gvar("CUSTOM_PFP") is not None and gvar("CUSTOM_PFP") == "true":
            return await edl(event, "`Custom pp is already enabled`")
        if not list_link:
            return await edl(event, "**ಠ∀ಠ  There no links for custom pp...**")
        sgvar("CUSTOM_PFP", True)
        await edl(event, "`Starting custom pp....`")
        await custompfploop()
        return
    if flag == "l":
        if not list_link:
            return await edl(event, "**ಠ∀ಠ  There no links set for custom pp...**")
        links = "**Available links for custom pp are here:**\n\n"
        for i, each in enumerate(list_link, start=1):
            links += f"**{i}.**  {each}\n"
        await edl(event, links, 60)
        return
    if flag == "s":
        if gvar("CUSTOM_PFP") is not None and gvar("CUSTOM_PFP") == "true":
            dgvar("CUSTOM_PFP")
            await event.client(
                DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edl(event, "`Custom pp has been stopped now`")
        return await edl(event, "`Custom pp haven't enabled`")
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid link or give valid link url as input...**"
        )
    extractor = URLExtract()
    plink = extractor.find_urls(input_str)
    if len(plink) == 0:
        return await edl(
            event, "**ಠ∀ಠ  Reply to valid link or give valid link url as input...**"
        )
    if flag == "a":
        for i in plink:
            if not is_in_list("CUSTOM_PFP_LINKS", i):
                add_to_list("CUSTOM_PFP_LINKS", i)
        await edl(event, f"**{len(plink)} pictures sucessfully added to custom pps**")
    elif flag == "r":
        for i in plink:
            if is_in_list("CUSTOM_PFP_LINKS", i):
                rm_from_list("CUSTOM_PFP_LINKS", i)
        await edl(
            event, f"**{len(plink)} pictures sucessfully removed from custom pps**"
        )


@doge.bot_cmd(
    pattern="autoname$",
    command=("autoname", plugin_category),
    info={
        "header": "Changes your name with time",
        "description": "Updates your profile name along with time. Set AUTONAME var with your profile name,",
        "note": "To stop this do '{tr}end autoname'",
        "usage": "{tr}autoname",
    },
)
async def _(event):
    "To set your display name along with time"
    if gvar("autoname") is not None and gvar("autoname") == "true":
        return await edl(event, "`Autoname is already enabled`")
    sgvar("autoname", True)
    await edl(event, "`Autoname has been started by my Master `")
    await autoname_loop()


@doge.bot_cmd(
    pattern="autobio$",
    command=("autobio", plugin_category),
    info={
        "header": "Changes your bio with time",
        "description": "Updates your profile bio along with time. Set DEFAULT_BIO var with your fav bio,",
        "note": "To stop this do '{tr}end autobio'",
        "usage": "{tr}autobio",
    },
)
async def _(event):
    "To update your bio along with time"
    if gvar("autobio") is not None and gvar("autobio") == "true":
        return await edl(event, "`Autobio is already enabled`")
    sgvar("autobio", True)
    await edl(event, "`Autobio has been started by my Master `")
    await autobio_loop()


@doge.bot_cmd(
    pattern="end ([\s\S]*)",
    command=("end", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "autopic": "To stop autopic",
            "dpp": "To stop difitalpp",
            "bloom": "To stop bloom",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
            "tpp": "To stop thorpp",
            "bpp": "To stop batmanpp",
            "spam": "To stop spam",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "tpp" and gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        if pfp_string != "tpp":
            return await edl(event, "`Thor pp isn't started`")
        await event.client(
            DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
        )
        dgvar("autopfp_strings")
        return await edl(event, "`Thor pp has been stopped now`")
    if input_str == "bpp" and gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        if pfp_string != "bpp":
            return await edl(event, "`Batman pp isn't started`")
        await event.client(
            DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
        )
        dgvar("autopfp_strings")
        return await edl(event, "`Batman pp has been stopped now`")
    if input_str == "autopic":
        if gvar("autopic") is not None and gvar("autopic") == "true":
            dgvar("autopic")
            if path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(UploadProfilePhotoRequest(file))
                    remove(autopic_path)
                except BaseException:
                    return
            return await edl(event, "`Autopic has been stopped now`")
        return await edl(event, "`Autopic haven't enabled`")
    if input_str == "dpp":
        if gvar("digitalpic") is not None and gvar("digitalpic") == "true":
            dgvar("digitalpic")
            await event.client(
                DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edl(event, "`Digitalpp has been stopped now`")
        return await edl(event, "`Digitalpp haven't enabled`")
    if input_str == "bloom":
        if gvar("bloom") is not None and gvar("bloom") == "true":
            dgvar("bloom")
            if path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(UploadProfilePhotoRequest(file))
                    remove(autopic_path)
                except BaseException:
                    return
            return await edl(event, "`Bloom has been stopped now`")
        return await edl(event, "`Bloom haven't enabled`")
    if input_str == "autoname":
        if gvar("autoname") is not None and gvar("autoname") == "true":
            dgvar("autoname")
            await event.client(UpdateProfileRequest(first_name=DEFAULTUSER))
            return await edl(event, "`Autoname has been stopped now`")
        return await edl(event, "`Autoname haven't enabled`")
    if input_str == "autobio":
        if gvar("autobio") is not None and gvar("autobio") == "true":
            dgvar("autobio")
            await event.client(UpdateProfileRequest(about=DEFAULTUSERBIO))
            return await edl(event, "`Autobio has been stopped now`")
        return await edl(event, "`Autobio haven't enabled`")
    if input_str == "spam":
        if gvar("spamwork") is not None and gvar("spamwork") == "true":
            dgvar("spamwork")
            return await edl(event, "`Spam cmd has been stopped now`")
        return await edl(event, "`You haven't started spam`")
    END_CMDS = [
        "autopic",
        "dpp",
        "bloom",
        "autoname",
        "autobio",
        "tpp",
        "bpp",
        "spam",
    ]
    if input_str not in END_CMDS:
        await edl(
            event,
            f"{input_str} is invalid end command. Mention clearly what should I end.",
            parse_mode=_format.parse_pre,
        )


doge.loop.create_task(autopfp_start())
doge.loop.create_task(autopicloop())
doge.loop.create_task(digitalpicloop())
doge.loop.create_task(bloom_pfploop())
doge.loop.create_task(autoname_loop())
doge.loop.create_task(autobio_loop())
doge.loop.create_task(custompfploop())
