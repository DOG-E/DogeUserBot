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
    BOTLOG,
    BOTLOG_CHATID,
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
            return await doge.bot.send_message(
                BOTLOG_CHATID,
                "**Hata:**\n`Otomatik profil fotoğrafı özelliği için lütfen DEFAULT_PIC değişkenini ayarlayın.`",
            )
        return
    if gvar("autopic") is not None:
        try:
            counter = int(gvar("autopic_counter"))
        except Exception as e:
            LOGS.warning(str(e))
    while AUTOPICSTART:
        if not path.exists(autopic_path):
            downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        file_test = im.rotate(counter, expand=False).save(autophoto_path, "PNG")
        current_time = datetime.now().strftime("  Saat: %H:%M \n  Tarih: %d.%m.%y ")
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
            await sleep(int(gvar("CHANGE_TIME") or 60))
        except BaseException:
            return
        AUTOPICSTART = gvar("autopic") == "true"


async def custompfploop():
    CUSTOMPICSTART = gvar("CUSTOM_PFP") == "true"
    i = 0
    while CUSTOMPICSTART:
        if len(get_collection_list("CUSTOM_PFP_LINKS")) == 0:
            LOGS.error("Ayarlanacak özel profil fotoğrafları yok.")
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
            await sleep(int(gvar("CHANGE_TIME") or 60))
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
            return await doge.bot.send_message(
                BOTLOG_CHATID,
                "**Hata:**\n`Otomatik çiçek profil fotoğrafı özelliği için lütfen DEFAULT_PIC değişkenini ayarlayın.`",
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
        current_time = datetime.now().strftime("\n Saat: %H:%M:%S\n\n Tarih: %d/%m/%y")
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
            await sleep(int(gvar("CHANGE_TIME") or 60))
        except BaseException:
            return
        BLOOMSTART = gvar("bloom") == "true"


async def autoname_loop():
    while AUTONAMESTART := gvar("autoname") == "true":
        DM = strftime("%d-%m-%y")
        HM = strftime("%H:%M")
        DEFAULTUSER = gvar("AUTONAME") or gvar("ALIVE_NAME")
        name = f"⌚️ {HM} ||›  {DEFAULTUSER} ‹|| {DM} 📅"
        LOGS.info(name)
        try:
            await doge(UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await sleep(ex.seconds)
        await sleep(int(gvar("CHANGE_TIME") or 60))


async def autobio_loop():
    while AUTOBIOSTART := gvar("autobio") == "true":
        DMY = strftime("%d.%m.%Y")
        HM = strftime("%H:%M")
        DEFAULTUSERBIO = gvar("DEFAULT_BIO") or "🐶 @DogeUserBot 🐾"
        bio = f"📅 {DMY} | {(DEFAULTUSERBIO)} | ⌚️ {HM}"
        LOGS.info(bio)
        try:
            await doge(UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await sleep(ex.seconds)
        await sleep(int(gvar("CHANGE_TIME") or 60))


async def animeprofilepic(collection_images):
    rnd = randint(0, len(collection_images) - 1)
    pack = collection_images[rnd]
    pc = get(f"http://getwallpapers.com/collection/{pack}").text
    f = compile(r"/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = f"http://getwallpapers.com{choice(f)}"
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
        await sleep(int(gvar("CHANGE_TIME") or 60))
        AUTOPFP_START = gvar("autopfp_strings") is not None


@doge.bot_cmd(
    pattern="bpp$",
    command=("bpp", plugin_category),
    info={
        "h": "Bir dakika aralıklarla profil fotoğafınızı rastgele batman fotoğrafları ile değiştirir.",
        "d": "Fotoğraf değiştirme süresini CHANGE_TIME değişkeninden ayarlayabilirsiniz.",
        "note": "Durdurmak için '{tr}end bpp' yazın.",
        "u": "{tr}bpp",
    },
)
async def _(event):
    "Profil resminizi rastgele batman fotoğrafları ile değiştirir."
    if gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        return await edl(event, f"`{pfp_string} zaten çalışıyor.`")
    sgvar("autopfp_strings", "batmanpfp_strings")
    await event.edit("`İşlem başlatıldı.`")
    await autopfp_start()


@doge.bot_cmd(
    pattern="tpp$",
    command=("tpp", plugin_category),
    info={
        "h": "Bir dakika aralıklarla profil fotoğrafınızı rastgele thor fotoğrafları ile değiştirir.",
        "d": "Fotoğraf değiştirme süresini CHANGE_TIME değişkeninden ayarlayabilirsiniz.",
        "note": "Durdurmak için '{tr}end tpp' yazın.",
        "u": "{tr}tpp",
    },
)
async def _(event):
    "Profil resminizi rastgele batman fotoğrafları ile değistirir."
    if gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        return await edl(event, f"`{pfp_string} zaten çalışıyor.`")
    sgvar("autopfp_strings", "thorpfp_strings")
    await event.edit("`İşlem başlatıldı! ✅`")
    await autopfp_start()


@doge.bot_cmd(
    pattern="autopic ?([\s\S]*)",
    command=("autopic", plugin_category),
    info={
        "h": "Bir dakika aralıklarla profil fotoğrafını yeniler.",
        "d": "Fotoğaf değiştirme süresini CHANGE_TIME değişkeninden ayarlayabilirsiniz.",
        "note": "Bu özelliği kullanmak için, DEFAULT_PIC değişkenini ayarlamalısınız. \
            Durdurmak için '{tr}end autopic' yazın.",
        "u": [
            "{tr}autopic",
            "{tr}autopic <any integer>",
        ],
    },
)
async def _(event):
    "Bir dakika aralıklarla profil fotoğrafını yeniler."
    if gvar("DEFAULT_PIC") is None:
        return await edl(
            event,
            "**Hata:**\n`Bu özelliği kullanmak için, DEFAULT_PIC değişkenini ayarlamalısınız.`",
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
        return await edl(event, "`Autopic, sahibim için başlatıldı!`")
    sgvar("autopic", True)
    if input_str:
        sgvar("autopic_counter", input_str)
    await edl(event, "`Autopic, sahibim için başlatıldı!`")
    await autopicloop()


@doge.bot_cmd(
    pattern="dpp$",
    command=("dpp", plugin_category),
    info={
        "h": "Bir dakika aralıklarla profil fotoğrafını yeniler.",
        "d": "Bir dakika aralıklarla eski profil fotoğrafını kaldırıp, yeni profil fotoğrafı ayarlar.\
             Bu özelliği kullanmak için DIGITAL_PIC değişkenini ayarlamalısınız.",
        "note": "Durdurmak için ',{tr}end dpp' yazın.",
        "u": "{tr}dpp",
    },
)
async def _(event):
    "Bir dakika aralıklarla profil fotoğrafını yeniler."
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvar("digitalpic") is not None and gvar("digitalpic") == "true":
        return await edl(event, "`Digitalpic zaten aktif.`")
    sgvar("digitalpic", True)
    await edl(event, "`Digitalpp sahibim için başlatıldı!`")
    await digitalpicloop()


@doge.bot_cmd(
    pattern="bloom$",
    command=("bloom", plugin_category),
    info={
        "h": "Profil fotoğraflarını bir dakika aralıklarla rastgele renklerle değiştirir.",
        "d": "Fotoğaf değiştirme süresini CHANGE_TIME değişkeninden ayarlayabilirsiniz.",
        "note": "Bu özelliği kullanmak için, DEFAULT_PIC değişkenini ayarlamalısınız. \
            Durdurmak için '{tr}end bloom' yazın.",
        "u": "{tr}bloom",
    },
)
async def _(event):
    "Profil fotoğrafını rastgele renklerle değiştirir."
    if gvar("DEFAULT_PIC") is None:
        return await edl(
            event,
            "**Hata:**\nBu özelliği kullanmak için, DEFAULT_PIC değişkenini ayarlamalısınız.",
        )
    downloader = SmartDL(gvar("DEFAULT_PIC"), autopic_path, progress_bar=True)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvar("bloom") is not None and gvar("bloom") == "true":
        return await edl(event, "`Bloom zaten aktif.`")
    sgvar("bloom", True)
    await edl(event, "`Bloom sahibim için başlatıldı! `")
    await bloom_pfploop()


@doge.bot_cmd(
    pattern="c(ustom)?pp(?: |$)([\s\S]*)",
    command=("custompp", plugin_category),
    info={
        "h": "Özel profil fotoğrafları ayarlar.",
        "d": "Komutu kullanmak için fotoğraf linklerini ayarlamanız lazım.",
        "f": {
            "a": "Custom pp'a fotoğraf eklemek içindir.",
            "r": "Custom pp'dan fotoğrafları kaldırır.",
            "l": "Custom pp için ayarlanmış linkleri verir.",
            "s": "Custom pp'ı durdurur.",
        },
        "u": [
            "{tr}cpp or {tr}custompp <başlatmak için>",
            "{tr}cpp <kategori> <linkler(isteğe bağlı)>",
        ],
        "e": [
            "{tr}cpp",
            "{tr}cpp .l",
            "{tr}cpp .s",
            "{tr}cpp .a link1 link2...",
            "{tr}cpp .r link1 link2...",
        ],
    },
)
async def useless(event):  # sourcery no-metrics
    """Özel profil fotoğrafları ayarlar."""
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
            return await edl(event, "`Custom pp zaten aktif.`")
        if not list_link:
            return await edl(event, "**Özel profil fotoğrafları için linkler ayarlanmamış.**")
        sgvar("CUSTOM_PFP", True)
        await edl(event, "`CustomPP başlatıldı.`")
        await custompfploop()
        return
    if flag == "l":
        if not list_link:
            return await edl(event, "**Özel profil fotoğrafları çin, linkler ayarlanmamış.**")
        links = "**Özel profil fotoğrafları için mevcut linkler:**\n\n"
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
            return await edl(event, "`Özel pp durduruldu!`")
        return await edl(event, "`Özel pp başlatılmadı! `")
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
        await edl(event, f"**{len(plink)} fotoğraf, başarıyla özel profil fotoğraflarına eklendi.**")
    elif flag == "r":
        for i in plink:
            if is_in_list("CUSTOM_PFP_LINKS", i):
                rm_from_list("CUSTOM_PFP_LINKS", i)
        await edl(
            event, f"**{len(plink)} fotoğraf başarıyla özel profil fotoğraflarından kaldırıldı.**"
        )


@doge.bot_cmd(
    pattern="autoname$",
    command=("autoname", plugin_category),
    info={
        "h": "Belirli bir zaman aralığında hesabın adını değiştirir.",
        "d": "AUTONAME değişkeninden hesabın adını ayarlayabilirsiniz.",
        "note": "Durdurmak için '{tr}end autoname' yazın.",
        "u": "{tr}autoname",
    },
)
async def _(event):
    "Belirli bir zaman aralıklarında hesabın adını değiştirir."
    if gvar("autoname") is not None and gvar("autoname") == "true":
        return await edl(event, "`Autoname zaten aktif.")
    sgvar("autoname", True)
    await edl(event, "`Autoname sahibim için başlatıldı!")
    await autoname_loop()


@doge.bot_cmd(
    pattern="autobio$",
    command=("autobio", plugin_category),
    info={
        "h": "Belirli bir zaman aralıklarında bio'yu değiştirir.",
        "d": "DEFAULT_BIO değişkeninden istediğiniz bio'yu ayarlayabilirsiniz.",
        "note": "Durdurmak için '{tr}end autobio' yazın.",
        "u": "{tr}autobio",
    },
)
async def _(event):
    "Belirli bir zaman aralığında bio'yu değiştirir."
    if gvar("autobio") is not None and gvar("autobio") == "true":
        return await edl(event, "`Autobio zaten aktif.`")
    sgvar("autobio", True)
    await edl(event, "`Autobio sahibim için başlatıldı!`")
    await autobio_loop()


@doge.bot_cmd(
    pattern="end ([\s\S]*)",
    command=("end", plugin_category),
    info={
        "h": "Profil fotoğrafı değiştirme işlemini durdurur.",
        "d": "Durdurmak istediğiniz özelliğin komutunu {tr} end <komut> olarak yazın.",
        "o": {
            "autopic": "Autopic özelliğini durdurur.",
            "dpp": "Difitalpp özelliğini durdurur.",
            "bloom": "Bloom özelliğni durdurur.",
            "autoname": "Autoname özelliğini durdurur.",
            "autobio": "Autobio özelliğini durdurur.",
            "tpp": "Thorpp özelliğni durdurur.",
            "bpp": "Batmanpp özelliğini durdurur.",
            "spam": "To stop spam",
        },
        "u": "{tr}end <durdurmak istediğiniz özelliğin komutu>",
        "e": ["{tr}end bpp"],
    },
)
async def _(event):  # sourcery no-metrics
    "Atoprofile eklentisindeki özellikleri durdurur."
    input_str = event.pattern_match.group(1)
    if input_str == "tpp" and gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        if pfp_string != "tpp":
            return await edl(event, "`Thor pp başlatılmadı!`")
        await event.client(
            DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
        )
        dgvar("autopfp_strings")
        return await edl(event, "`Thor pp durduruldu!`")
    if input_str == "bpp" and gvar("autopfp_strings") is not None:
        pfp_string = gvar("autopfp_strings")[:-8]
        if pfp_string != "bpp":
            return await edl(event, "`Batman pp başlatılmadı!`")
        await event.client(
            DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1))
        )
        dgvar("autopfp_strings")
        return await edl(event, "`Batman pp durduruldu!`")
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
            return await edl(event, "`Autopic durduruldu!`")
        return await edl(event, "`Autopic başlatılmadı!`")
    if input_str == "dpp":
        if gvar("digitalpic") is not None and gvar("digitalpic") == "true":
            dgvar("digitalpic")
            await event.client(
                DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edl(event, "`Digitalpp durduruldu!`")
        return await edl(event, "`Digitalpp başlatılmadı!`")
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
            return await edl(event, "`Bloom durduruldu!`")
        return await edl(event, "`Bloom başlatılmadı!`")
    if input_str == "autoname":
        if gvar("autoname") is not None and gvar("autoname") == "true":
            dgvar("autoname")
            DEFAULTUSER = gvar("AUTONAME") or gvar("ALIVE_NAME")
            await event.client(UpdateProfileRequest(first_name=DEFAULTUSER))
            return await edl(event, "`Autoname durduruldu!`")
        return await edl(event, "`Autoname başlatılmadı?`")
    if input_str == "autobio":
        if gvar("autobio") is not None and gvar("autobio") == "true":
            dgvar("autobio")
            DEFAULTUSERBIO = gvar("DEFAULT_BIO") or "  @DogeUserBot 🐾"
            await event.client(UpdateProfileRequest(about=DEFAULTUSERBIO))
            return await edl(event, "`Autobio durduruldu! `")
        return await edl(event, "`Autobio başlatılmadı! `")
    if input_str == "spam":
        if gvar("spamwork") is not None and gvar("spamwork") == "true":
            dgvar("spamwork")
            return await edl(event, "`Spam durduruldu! `")
        return await edl(event, "`Spam başlatılmadı`")
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
            f"{input_str} bu komut geçersizdir. Durdurmam için düzgün bir komut yazın.",
            parse_mode=_format.parse_pre,
        )


doge.loop.create_task(autopfp_start())
doge.loop.create_task(autopicloop())
doge.loop.create_task(digitalpicloop())
doge.loop.create_task(bloom_pfploop())
doge.loop.create_task(autoname_loop())
doge.loop.create_task(autobio_loop())
doge.loop.create_task(custompfploop())
