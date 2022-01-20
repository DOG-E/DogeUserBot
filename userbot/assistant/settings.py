# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio.tasks import sleep
from re import compile

from heroku3 import from_key
from telegraph import Telegraph, upload_file
from telegraph.exceptions import TelegraphException
from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from validators.url import url

from userbot import HEROKU_API_KEY, HEROKU_APP_NAME

from ..core.logger import logging
from ..helpers import resize_image
from ..utils import add_bot_to_logger_group, create_channel, create_supergroup
from . import (
    BOTLOG_CHATID,
    TEMP_DIR,
    check_owner,
    doge,
    get_back_button,
    gvar,
    newmsgres,
    sgvar,
)

plugin_category = "bot"
LOGS = logging.getLogger("DogeUserBot")

telegraph = Telegraph()
r = telegraph.create_account(
    short_name=(gvar("TELEGRAPH_SHORT_NAME") or "@DogeUserBot"),
    author_url="https://t.me/DogeUserBot",
)
auth_url = r["auth_url"]

# ilk ayarlar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"setmenu")))
@check_owner
async def settings(event: CallbackQuery):
    options = [
        [
            Button.inline("🧶 Aᴘɪ'ʟᴇʀ", data="apimenu"),
        ],
        [
            Button.inline(
                "🐾 Sᴇçᴇɴᴇᴋʟᴇʀ", data="ssmenu"
            ),  # ss menu yeniden oluşturalacak
            Button.inline("🧊 Hᴇʀᴏᴋᴜ", data="herokumenu"),
        ],
        [
            Button.inline("🌐 Dɪʟ", data="langmenu"),
        ],
    ]
    if not event.is_private and event.chat_id == BOTLOG_CHATID:
        return await event.answer(
            f"Bu ayarları yapabilmek için bana özelden yazmalısın!", alert=True
        )
    elif not event.is_private:
        return
    else:
        await event.edit(
            f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
            \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
            \n◽ Doɢᴇ oғ {gvar('mention')}\n\
            \n✨ Ayarlamak istediğinizi aşağıdan seçin:**",
            buttons=options,
            link_preview=False,
        )


# HEROKU
@doge.bot.on(CallbackQuery(data=compile(b"herokumenu")))
@check_owner
async def herokumenu(event: CallbackQuery):
    buttons = [
        [
            Button.inline("APP_ID", data="app_id"),
            Button.inline("API_HASH", data="api_hash"),
        ],
        [
            Button.inline("DOGEHUB", data="dogehub"),
            Button.inline("DOGEPLUGIN", data="dogeplugin"),
        ],
        [
            Button.inline("HEROKU_API_KEY", data="heroku_api_key"),
            Button.inline("HEROKU_APP_NAME", data="heroku_app_name"),
        ],
        [
            Button.inline("TZ", data="TZ_HEROKU"),
            Button.inline("TZ_NUMBER", data="TZ_NUMBER_HEROKU"),
        ],
        [
            Button.inline("DATABASE_URL", data="DATABASE_URL"),
            Button.inline("STRING_SESSION", data="STRING_SESSION"),
        ],
        [
            Button.inline("UPSTREAM_REPO_BRANCH", data="UPSTREAM_REPO_BRANCH"),
            Button.inline(
                "PRIVATE_GROUP_BOT_API_ID", data="PRIVATE_GROUP_BOT_API_ID    "
            ),
        ],
    ]
    buttons.append(get_back_button("setmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
            \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
            \n◽ Doɢᴇ oғ {gvar('mention')}\n\
            \n✨ Ayarlamak istediğinizi aşağıdan seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# Ayarlar - Seçenekler
@doge.bot.on(CallbackQuery(data=compile(b"ssmenu")))
@check_owner
async def ssmenu(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Alive", data="ssalive"),
            Button.inline("PmPermit", data="sspmmenu"),
        ],
        [
            Button.inline("PMBot", data="sspmbot"),
            Button.inline("CMDSET", data="sshandler"),
        ],
        [
            Button.inline("Grup & Kanal", data="sscg"),
            Button.inline("Logger", data="sslogger"),
        ],
        [
            Button.inline("SETHELP", data="sshelp"),
            Button.inline("Other", data="ssother"),
        ],
    ]
    buttons.append(get_back_button("setmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz ayarı seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# Alive yapılandırma ayarları
@doge.bot.on(CallbackQuery(data=compile(b"ssalive")))
@check_owner
async def ssalive(event: CallbackQuery):
    buttons = [
        [
            Button.inline("IALIVE_PIC", data="IALIVE_PIC"),
            Button.inline("ALIVE_PIC", data="ALIVE_PIC"),
        ],
        [
            Button.inline("ALIVE_NAME", data="ALIVE_NAME"),
            Button.inline("ALIVE_TEXT", data="ALIVE_TEXT"),
        ],
        [Button.inline("ALIVE", data="ALIVE")],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Alive ile ilgili ayarlamak istediğiniz ayarı seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# TODO çok fazla değiişken var ve çok karışık -_-


@doge.bot.on(CallbackQuery(data=compile(b"sspmmenu")))
@check_owner
async def sspmmenu(event: CallbackQuery):
    buttons = [
        [
            Button.inline("PM_PIC", data="PM_PIC"),
            Button.inline("MAX_FLOOD_IN_PMS", data="MAX_FLOOD_IN_PMS"),
        ],
        [
            Button.inline("pmmenu", data="pmmenu"),
            Button.inline("pmpermit_txt", data="pmpermit_txt"),
        ],
        [Button.inline("pmpermit", data="pmpermit")],
    ]

    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Alive ile ilgili ayarlamak istediğiniz ayarı seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# Asistan Bot için ayarlar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"sspmbot")))
@check_owner
async def sspmbot(event: CallbackQuery):
    buttons = [
        [
            Button.inline("START_PIC", data="START_PIC"),
            Button.inline("START_TEXT", data="START_TEXT"),
        ],
        [Button.inline("START_BUTTON", data="START_BUTTON")],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# varsayılan komutlar ayarlar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"sshandler")))
@check_owner
async def sshandler(event: CallbackQuery):
    buttons = [
        [
            Button.inline("CMDSET", data="CMDSET"),
            Button.inline("SUDO_CMDSET", data="SUDO_CMDSET"),
        ],
        [
            Button.inline("SNIP_CMDSET", data="SNIP_CMDSET"),
        ],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# pm - tag logger ayar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"sslogger")))
@check_owner
async def sslogger(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Pm Logger", data="PM_LOGGER"),
        ],
        [
            Button.inline("Tag Logger", data="TAG_LOGGER"),
        ],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# TAG LOGGER


@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER")))
@check_owner
async def TAG_LOGGER(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Aç", data="TAG_LOGGER_ON"),
            Button.inline("Kapa", data="TAG_LOGGER_OFF"),
        ],
        [Button.inline("Grup ayarları", data="TAG_LOGGER_GROUP")],
    ]
    buttons.append(get_back_button("sslogger"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# TAG LOGGER GROUP
@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER_GROUP")))
@check_owner
async def TAG_LOGGER_GROUP(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Otomatik", data="TAG_LOGGER_GROUP_AUTO"),
            Button.inline("Manuel", data="TAG_LOGGER_GROUP_MANUEL"),
        ]
    ]
    buttons.append(get_back_button("TAG_LOGGER"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# TAG LOGGER KAPAMA
@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER_OFF")))
@check_owner
async def TAG_LOGGER_OFF(event: CallbackQuery):
    if gvar("GRPLOG") != "True":
        hloff = "🐶 Doɢᴇ UsᴇʀBoᴛ\n\nTag Logger özelliğiniz zaten kapalı!"
        return await event.answer(hloff, cache_time=0, alert=True)
    elif gvar("GRPLOG") == "True":
        sgvar("GRPLOG", "False")
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n TAG loggerözelliğiniz başarıyla kapatıldı",
            alert=True,
        )


# TAG LOGGER açma -_-
@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER_ON")))
@check_owner
async def TAG_LOGGER_ON(event: CallbackQuery):
    buttons = [
        [
            Button.inline("🕹 Otomatik", data="TAG_LOGGER_GROUP_AUTO"),
            Button.inline("🥏 Manüel", data="TAG_LOGGER_GROUP_MANUEL"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="TAG_LOGGER_ON"),
        ],
    ]
    if gvar("GRPLOG") == "True":
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n TAG Logger özelliğiniz zaten açık!", alert=True
        )
    elif gvar("PM_LOGGER_GROUP_ID") is None and gvar("TAG_LOGGER_GROUP_ID") is None:
        await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n TAG Logger özelliğini açmak için öncelikle bir grup ayarlamanız gerekir. Sizi grup ayarlama ekranına yönlendiriyorum..."
        )
        await event.edit(
            f"""🔔 **Etiketleri kaydetme grubunuzun Doge UserBot tarafından oluşturulmasını istiyorsanız** "`🕹 Otomatik`", **kendiniz ayarlamak istiyorsanız** "`🥏 Manüel`" **yazan butona tıklayın.**""",
            buttons=buttons,
        )
    elif (
        gvar("PM_LOGGER_GROUP_ID") is not None
        or gvar("TAG_LOGGER_GROUP_ID") is not None
    ):
        sgvar("GRPLOG", True)
        return await event.answer("🐶 TAG LOGGER değeriniz açıldı!", alert=True)


# TAG LOGGER otomatik grup açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER_GROUP_AUTO")))
@check_owner
async def TAG_LOGGER_GROUP_AUTO(event: CallbackQuery):
    if gvar("TAG_LOGGER_GROUP_ID") is None and gvar("PM_LOGGER_GROUP_ID") is None:
        await event.edit(
            f"{gvar('mention')} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
        )
        await tagloggeraurocreate(event)
    elif gvar("HLOGGER_ID") is not None:
        try:
            a = await doge.bot.send_message(
                int(gvar("HLOGGER_ID")), f"Heroku Logger Grubu Test Mesajı!"
            )
            await a.delete()
            return await event.edit(
                f"Heroku Logger için zaten kayıtlı bir grubunuz var! Grup oluşturma işlemini iptal ediyorum",
                buttons=get_back_button("hgloggrpc"),
            )
        except Exception as e:
            LOGS.warning(
                f"Heroku Logger grubuna ulaşılamadı yeni grup açılıyor... Hata Raporu: {e}"
            )
            await event.edit(
                f"{gvar('mention')} Veritabanınızda kayıtlı gruba erişilemedi! Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
            )
            await tagloggeraurocreate(event)


# PM LOGGER için ayarlar
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER")))
@check_owner
async def PM_LOGGER(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Aç", data="PM_LOGGER_ON"),
            Button.inline("Kapa", data="PM_LOGGER_OFF"),
        ],
        [Button.inline("Grup ayarları", data="PM_LOGGER_GROUP")],
    ]
    buttons.append(get_back_button("sslogger"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# PM LOGGER için grup ayarları
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER_GROUP")))
@check_owner
async def PM_LOGGER_GROUP(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Otomatik", data="PM_LOGGER_GROUP_AUTO"),
            Button.inline("Manuel", data="PM_LOGGER_GROUP_MANUEL"),
        ]
    ]
    buttons.append(get_back_button("PM_LOGGER"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# PM LOGGER kapatma
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER_OFF")))
@check_owner
async def PM_LOGGER_OFF(event):
    if gvar("pmpermit") != "True":
        hloff = "🐶 Doɢᴇ UsᴇʀBoᴛ\n\nHeroku Logger özelliğiniz zaten kapalı!"
        return await event.answer(hloff, cache_time=0, alert=True)
    elif gvar("pmpermit") == "True":
        sgvar("HEROKULOGGER", "False")
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\ PM Permit özelliğiniz başarıyla kapatıldı",
            alert=True,
        )


# PM LOGGER açma
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER_ON")))
@check_owner
async def PM_LOGGER_ON(event: CallbackQuery):
    buttons = [
        [
            Button.inline("🕹 Otomatik", data="PM_LOGGER_GROUP_AUTO"),
            Button.inline("🥏 Manüel", data="PM_LOGGER_GROUP_MANUEL"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="PM_LOGGER_ON"),
        ],
    ]
    if gvar("pmpermit") == "True":
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n PM Logger özelliğiniz zaten açık!", alert=True
        )
    elif gvar("PM_LOGGER_GROUP_ID") is not None and gvar("pmpermit") != "True":
        sgvar("pmpermit", True)
        return await event.answer("🐶 PM LOGGER değeriniz açıldı!", alert=True)
    elif gvar("PM_LOGGER_GROUP_ID") is None:
        await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n PM Logger özelliğini açmak için öncelikle bir grup ayarlamanız gerekir. Sizi grup ayarlama ekranına yönlendiriyorum..."
        )
        await event.edit(
            f"""💬 **PM için log grubunuzun Doge UserBot tarafından oluşturulmasını istiyorsanız** "`🕹 Otomatik`", **kendiniz ayarlamak istiyorsanız** "`🥏 Manüel`" **yazan butona tıklayın.**""",
            buttons=buttons,
        )


# PM LOGGER Otomatik grup açma
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER_GROUP_AUTO")))
@check_owner
async def PM_LOGGER_GROUP_AUTO(event: CallbackQuery):
    if gvar("PM_LOGGER_GROUP_ID") is None:
        await event.edit(
            f"{gvar('mention')} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir PM Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
        )
        await pmloggeraurocreate(event)
    elif gvar("PM_LOGGER_GROUP_ID") is not None:
        try:
            a = await doge.bot.send_message(
                int(gvar("PM_LOGGER_GROUP_ID")), f"PM Logger Grubu Test Mesajı!"
            )
            await a.delete()
            return await event.edit(
                f"PM Logger için zaten kayıtlı bir grubunuz var! Grup oluşturma işlemini iptal ediyorum",
                buttons=get_back_button("PM_LOGGER_GROUP"),
            )
        except Exception as e:
            LOGS.warning(
                f"PM Logger grubuna ulaşılamadı yeni grup açılıyor... Hata Raporu: {e}"
            )
            await event.edit(
                f"{gvar('mention')} Veritabanınızda kayıtlı gruba erişilemedi! Sizin için bir PM Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
            )
            await pmloggeraurocreate(event)


# help için ayarlar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"sshelp")))
@check_owner
async def sshelp(event: CallbackQuery):
    buttons = [
        [
            Button.inline("HELP_PIC", data="HELP_PIC"),
        ],
        [
            Button.inline("HELP_TEXT", data="HELP_TEXT"),
            Button.inline("HELP_EMOJI", data="HELP_EMOJI"),
        ],
        [
            Button.inline("Yardımdaki Satır sayısı", data="NO_OF_ROWS_IN_HELP"),
            Button.inline("Yardımdaki Sütun Sayısı", data="NO_OF_COLUMNS_IN_HELP"),
        ],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# geriye kalanlar ayarlar menüsü TODO


@doge.bot.on(CallbackQuery(data=compile(b"ssother")))
@check_owner
async def ssother(event: CallbackQuery):
    buttons = [
        [
            Button.inline("Geri kalan Fotoğraflar", data="otherpics"),
            Button.inline("Geriye Kalan isimler", data="othernames"),
        ],
        [
            Button.inline("Ekstra Pluginler", data="otherplugins"),
            Button.inline("Varsayılan Bio", data="otherbio"),
        ],
        [
            Button.inline("Bio Değişimi", data="otherbioedited"),
            Button.inline("DEV_MOD", data="otherdevmode"),
        ],
        [
            Button.inline("Hava Durumu", data="otherweather"),
        ],
    ]
    buttons.append(get_back_button("ssmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# SSOTHER geriye kalan fotoğraflar


@doge.bot.on(CallbackQuery(data=compile(b"otherpics")))
@check_owner
async def otherpics(event: CallbackQuery):
    buttons = [
        [
            Button.inline("DEFAULT_PIC", data="DEFAULT_PIC"),
            Button.inline("DIGITAL_PIC", data="DIGITAL_PIC"),
        ],
        [Button.inline("THUMB_PIC", data="THUMB_PIC")],
    ]
    buttons.append(get_back_button("ssother"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# SSOTHER geriye kalan isimler
@doge.bot.on(CallbackQuery(data=compile(b"othernames")))
@check_owner
async def othernames(event: CallbackQuery):
    buttons = [
        [
            Button.inline("AUTONAME", data="AUTONAME"),
            Button.inline("CUSTOM_STICKER_PACKNAME", data="CUSTOM_STICKER_PACKNAME"),
        ],
        [Button.inline("TELEGRAPH_SHORT_NAME", data="TELEGRAPH_SHORT_NAME")],
    ]
    buttons.append(get_back_button("ssother"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# SSOTHER hava durumu ayarları
@doge.bot.on(CallbackQuery(data=compile(b"otherweather")))
@check_owner
async def otherweather(event: CallbackQuery):
    buttons = [
        [
            Button.inline("WATCH_COUNTRY", data="WATCH_COUNTRY"),
            Button.inline("WEATHER_CITY", data="WEATHER_CITY"),
        ]
    ]
    buttons.append(get_back_button("ssother"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


# api - grup id'leri menüsü
@doge.bot.on(CallbackQuery(data=compile(b"apimenu")))
@check_owner
async def apisetter(event: CallbackQuery):
    apis = [
        [
            Button.inline("CURRENCY", data="cuapi"),
            Button.inline("Dᴇᴇᴘ", data="deapi"),
        ],
        [
            Button.inline("GENIUS", data="geapi"),
            Button.inline("GITHUB", data="ghapi"),
        ],
        [
            # Button.inline("GOOGLE DRIVE", data="gdapi"),
            Button.inline("IBM WATSON", data="ibmwcapi"),
        ],
        [
            Button.inline("IP DATA", data="ipdapi"),
            Button.inline("LAST FM", data="lfmapi"),
        ],
        [
            Button.inline("OCR SPACE", data="ocrsapi"),
            Button.inline("REMOVE BG", data="rbgapi"),
        ],
        [
            Button.inline("SPAM WATCH", data="swapi"),
            Button.inline("SPOTIFY", data="spapi"),
        ],
        [
            Button.inline("SCREEN SHOT", data="ssapi"),
            Button.inline("WEATHER", data="woapi"),
        ],
    ]
    apis.append(get_back_button("setmenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=apis,
        link_preview=False,
    )


# grup/kanalların ayar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"sscg")))
@check_owner
async def sscg(event: CallbackQuery):
    apis = [
        [
            Button.inline("FBAN GRUBU", data="fgroup"),
            Button.inline("GİZLİ KANAL", data="pccreate"),
        ],
        [
            Button.inline("Heroku Logger", data="hlogger"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="ssmenu"),
        ],
    ]
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=apis,
        link_preview=False,
    )


# heroku logger menüsü
@doge.bot.on(CallbackQuery(data=compile(b"hlogger")))
@check_owner
async def hlogger(event):
    buttons = [
        [
            Button.inline("✅ Aç", data="hgloggeron"),
            Button.inline("❎ Kapat", data="hgloggeroff"),
        ],
        [
            Button.inline("HLog Grubu Ayarla", data="hgloggrpc"),
        ],
    ]
    buttons.append(get_back_button("sscg"))
    await event.edit(f"Heroku Logger özelliği menünüzü özelleştirin.", buttons=buttons)


# heroku logger özelliğini kapatma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hgloggeroff")))
@check_owner
async def hgloggeroff(event):
    if gvar("HEROKULOGGER") == ("False" or None):
        hloff = "🐶 Doɢᴇ UsᴇʀBoᴛ\n\nHeroku Logger özelliğiniz zaten kapalı!"
        return await event.answer(hloff, cache_time=0, alert=True)
    if gvar("HEROKULOOGER") == "True":
        sgvar("HEROKULOGGER", "False")
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\ Heroku Logger özelliğiniz başarıyla kapatıldı",
            alert=True,
        )


# heroku logger özelliğini açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hgloggeron")))
@check_owner
async def hgloggeron(event: CallbackQuery):
    buttons = [
        [
            Button.inline("🕹 Otomatik", data="hgloggerautocreate"),
            Button.inline("🥏 Manuel", data="hloggermanuelcreate"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="hgloggeron"),
        ],
    ]
    # if gvar("DEV_MODE") != True: #Yakında
    #   return await event.answer("Bir geliştirici değilsiniz.", alert=True)
    if gvar("HEROKULOGGER") == "True":
        return await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğiniz zaten açık!", alert=True
        )
    if gvar("HLOGGER_ID") is None and gvar("HEROKULOGGER") == "False":
        await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğini açmak için öncelikle bir grup ayarlamanız gerekir. Sizi grup ayarlama ekranına yönlendiriyorum..."
        )
        await event.edit(
            f'📑 **Heroku log grubunuzun Doge UserBot tarafından oluşturulmasını istiyorsanız** "`🕹 Otomatik`", **kendiniz ayarlamak istiyorsanız** "`🥏 Manüel`" **yazan butona tıklayın.**',
            buttons=buttons,
        )
    if gvar("HEROKULOGGER") == "False" and gvar("HLOOGER_ID") is not None:
        sgvar("HEROKLOGGER", "True")
        await event.answer(
            f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğiniz başarıyla etkinleştirildi! Veritabanına kayıtlı gruba Heroku Log eylemi başlatılacaktır."
        )


# heroku logger grup açma seçenekleri
@doge.bot.on(CallbackQuery(data=compile(b"hgloggrpc")))
@check_owner
async def hgloggrpc(event: CallbackQuery):
    buttons = [
        [
            Button.inline("✅ Evet", data="hgloggerautocreate"),
            Button.inline("🥏 Manuel", data="hloggermanuelcreate"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="hlogger"),
        ],
    ]
    await event.edit(
        f'📑 **Heroku log grubunuzun Doge UserBot tarafından oluşturulmasını istiyorsanız** "`🕹 Otomatik`", **kendiniz ayarlamak istiyorsanız** "`🥏 Manüel`" **yazan butona tıklayın.**',
        buttons=buttons,
    )


# heroku logger için otomatik grup açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hgloggerautocreate")))
@check_owner
async def hgloggerautocreate(event: CallbackQuery):
    # if gvar("DEV_MODE") != True: #Yakında
    #   return await event.answer("Birgeliştirici değilsiniz.", alert=True)
    if gvar("HLOGGER_ID") is None:
        await event.edit(
            f"{gvar('mention')} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
        )
        await herokuloggergroupcreate(event)
    elif gvar("HLOGGER_ID") is not None:
        try:
            a = await doge.bot.send_message(
                int(gvar("HLOGGER_ID")), f"Heroku Logger Grubu Test Mesajı!"
            )
            await a.delete()
            return await event.edit(
                f"Heroku Logger için zaten kayıtlı bir grubunuz var! Grup oluşturma işlemini iptal ediyorum",
                buttons=get_back_button("hgloggrpc"),
            )
        except Exception as e:
            LOGS.warning(
                f"Heroku Logger grubuna ulaşılamadı yeni grup açılıyor... Hata Raporu: {e}"
            )
            await event.edit(
                f"{gvar('mention')} Veritabanınızda kayıtlı gruba erişilemedi! Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin..."
            )
            await herokuloggergroupcreate(event)


# fban grubu açmak için seçenekler menüsü
@doge.bot.on(CallbackQuery(data=compile(b"fgroup")))
@check_owner
async def fggroup(event: CallbackQuery):
    buttons = [
        [
            Button.inline("🕹 Otomatik", data="fgcreate"),
            Button.inline("🥏 Manüel", data="fgapi"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="ssmenu"),
        ],
    ]
    await event.edit(
        f"""✅ **Rose için Fban grup ayarları!**

**Fban grubunuzun Doge UserBot tarafından oluşturulmasını istiyorsanız** "`c`", **kendiniz ayarlamak istiyorsanız** "`🥏 Manüel`" **yazan butona tıklayın.**""",
        buttons=buttons,
        link_preview=False,
    )


# otomatik FBAN grubu açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"fgcreate")))
@check_owner
async def fggrupcreate(event: CallbackQuery):
    if gvar("FBAN_GROUP_ID") is None:
        await event.edit(
            f"{gvar('mention')} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir FBan grubu oluşturuyorum! Lütfen bekleyin..."
        )
        await fgchelper(event)
    else:
        try:
            a = await doge.send_message(
                int(gvar("FBAN_GROUP_ID")), "FBan Grup Deneme mesajı!"
            )
            await a.delete()
            return await event.edit(
                f"FBan için zaten bir grubunuz var! Grup oluşturma işlemini iptal ediyorum...",
                buttons=get_back_button("fgroup"),
            )
        except Exception:
            await event.edit(
                f"{gvar('mention')} Veritabanına kayıtlı grubunuza erişiminiz yok. Sizin için bir FBan grubu oluşturuyorum! Lütfen bekleyin..."
            )
            await fgchelper(event)


# gizli kanal oluşturma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"pccreate")))
@check_owner
async def pccreate(event: CallbackQuery):
    buttons = [
        [
            Button.inline("✅ Evet", data="pcauto"),
            Button.inline("❎ Hayır", data="pcmanuel"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="sscg"),
        ],
    ]
    await event.edit(
        f"__Gizli kanalınız için DogeUserBot tarafından oluştulurulmasını isterseniz__ '✅ Evet' __düğmesine, kendiniz oluşturduğunuz bir grubu ayarlamak için__ '❎ Hayır' __düğmesine basınız.__",
        buttons=buttons,
    )


# gizli kanalın otomatik ayarlanma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"pcauto")))
@check_owner
async def pcmanuel(event: CallbackQuery):
    if gvar("PRIVATE_CHANNEL_ID") is not None:
        try:
            a = await doge.send_message(
                int(gvar("PRIVATE_CHANNEL_ID")), f"Gizli kanal Deneme mesajı!"
            )
            await a.delete()
            return await event.edit(
                f"Gizli Kanal özelliği için zaten hazırda bi kanalınız var! Yeni kanal açma işlemini iptal ediyorum.",
                buttons=get_back_button("pccreate"),
            )
        except Exception as e:
            LOGS.warning(
                f"Gizli kanala erişim sağlanamadı yeni kanal açılıyor... Hata Raporu: {e}"
            )
            await event.edit(
                f"{gvar('mention')} Veritabanınızda kayıtlı gizli kanala erişilemedi! Sizin için bir Gizli Kanal oluşturuyorum! Lütfen bekleyin..."
            )
        try:
            await privatechannel(event)
        except Exception as e:
            await event.edit(
                f"Gizli kanal oluştururken bir hata oluşu! Hata Raporu: {e}"
            )
    if gvar("PRIVATE_CHANNEL_ID") is None:
        await event.edit(
            f"Veritabanında kayıtlı bir Gizli Kanal değeri bulunamadı! Sizin için yeni bir Gizli Kanal oluşturuyoruM! Lütfen bekleyin..."
        )


###### SEÇENEKLER #####

# Heroku Values Callbacks
@doge.bot.on(CallbackQuery(data=compile(b"app_id")))
@check_owner
async def api_id(event: CallbackQuery):
    x = "📃 **DEĞER:** `APP_ID`\n\
    \n📋 **Açıklama:** `APP_ID`\n\
    \n APP_ID"
    y = "APP_ID"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"api_hash")))
@check_owner
async def api_hash(event: CallbackQuery):
    x = "📃 **DEĞER:** `API_HASH`\n\
    \n📋 **Açıklama:** `API_HASH`\n\
    \n API_HASH"
    y = "API_HASH"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"dogehub")))
@check_owner
async def dogehub(event: CallbackQuery):
    x = "📃 **DEĞER:** `DOGEHUB`\n\
    \n📋 **Açıklama:** `DOGEHUB`\n\
    \n DOGEHUB"
    y = "DOGEHUB"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"dogeplugin")))
@check_owner
async def dogeplugin(event: CallbackQuery):
    x = "📃 **DEĞER:** `DOGEPLUGIN`\n\
    \n📋 **Açıklama:** `DOGEPLUGIN`\n\
    \n DOGEPLUGIN"
    y = "DOGEPLUGIN"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"heroku_api_key")))
@check_owner
async def heroku_api_key(event: CallbackQuery):
    x = "📃 **DEĞER:** `HEROKU_API_KEY`\n\
    \n📋 **Açıklama:** `HEROKU_API_KEY`\n\
    \n HEROKU_API_KEY"
    y = "HEROKU_API_KEY"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"heroku_app_name")))
@check_owner
async def heroku_app_name(event: CallbackQuery):
    x = "📃 **DEĞER:** `HEROKU_APP_NAME`\n\
    \n📋 **Açıklama:** `HEROKU_APP_NAME`\n\
    \n HEROKU_APP_NAME"
    y = "HEROKU_APP_NAME"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"TZ_HEROKU")))
@check_owner
async def TZ_HEROKU(event: CallbackQuery):
    x = "📃 **DEĞER:** `TZ`\n\
    \n📋 **Açıklama:** `TZ`\n\
    \n TZ"
    y = "TZ"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"TZ_NUMBER_HEROKU")))
@check_owner
async def TZ_NUMBER_HEROKU(event: CallbackQuery):
    x = "📃 **DEĞER:** `TZ_NUMBER`\n\
    \n📋 **Açıklama:** `TZ_NUMBER`\n\
    \n TZ_NUMBER"
    y = "TZ_NUMBER"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"DATABASE_URL")))
@check_owner
async def DATABASE_URL(event: CallbackQuery):
    x = "📃 **DEĞER:** `DATABASE_URL`\n\
    \n📋 **Açıklama:** `DATABASE_URL`\n\
    \n DATABASE_URL"
    y = "DATABASE_URL"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"STRING_SESSION")))
@check_owner
async def STRING_SESSION(event: CallbackQuery):
    x = "📃 **DEĞER:** `STRING_SESSION`\n\
    \n📋 **Açıklama:** `STRING_SESSION`\n\
    \n STRING_SESSION"
    y = "STRING_SESSION"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"UPSTREAM_REPO_BRANCH")))
@check_owner
async def UPSTREAM_REPO_BRANCH(event: CallbackQuery):
    x = "📃 **DEĞER:** `UPSTREAM_REPO_BRANCH`\n\
    \n📋 **Açıklama:** `UPSTREAM_REPO_BRANCH`\n\
    \n UPSTREAM_REPO_BRANCH"
    y = "UPSTREAM_REPO_BRANCH"
    z = "herokumenu"
    await sh(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"PRIVATE_GROUP_BOT_API_ID")))
@check_owner
async def PRIVATE_GROUP_BOT_API_ID(event: CallbackQuery):
    x = "📃 **DEĞER:** `PRIVATE_GROUP_BOT_API_ID`\n\
    \n📋 **Açıklama:** `PRIVATE_GROUP_BOT_API_ID`\n\
    \n PRIVATE_GROUP_BOT_API_ID"
    y = "PRIVATE_GROUP_BOT_API_ID"
    z = "herokumenu"
    await sh(event, x, y, z)


# Alive values callbacks
@doge.bot.on(CallbackQuery(data=compile(b"IALIVE_PIC")))
@check_owner
async def IALIVE_PIC(event: CallbackQuery):
    x = "📃 **DEĞER:** `IALIVE_PIC`\n\
    \n📋 **Açıklama:** `IALIVE_PIC `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "IALIVE_PIC"
    z = "ssalive"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ALIVE_PIC")))
@check_owner
async def ALIVE_PIC(event: CallbackQuery):
    x = "📃 **DEĞER:** `ALIVE_PIC`\n\
    \n📋 **Açıklama:** `ALIVE_PIC `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "ALIVE_PIC"
    z = "ssalive"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ALIVE_NAME")))
@check_owner
async def ALIVE_NAME(event: CallbackQuery):
    x = "📃 **DEĞER:** `ALIVE_NAME`\n\
    \n📋 **Açıklama:** `ALIVE_NAME `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "ALIVE_NAME"
    z = "ssalive"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ALIVE_TEXT")))
@check_owner
async def ALIVE_TEXT(event: CallbackQuery):
    x = "📃 **DEĞER:** `ALIVE_TEXT`\n\
    \n📋 **Açıklama:** `ALIVE_TEXT `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "ALIVE_TEXT"
    z = "ssalive"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ALIVE")))
@check_owner
async def ALIVE(event: CallbackQuery):
    x = "📃 **DEĞER:** `ALIVE`\n\
    \n📋 **Açıklama:** `ALIVE `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "ALIVE"
    z = "ssalive"
    await ss(event, x, y, z)


# PM Permit values callbacks
@doge.bot.on(CallbackQuery(data=compile(b"PM_PIC")))
@check_owner
async def PM_PIC(event: CallbackQuery):
    x = "📃 **DEĞER:** `PM_PIC`\n\
    \n📋 **Açıklama:** `PM_PIC `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "PM_PIC"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"MAX_FLOOD_IN_PMS")))
@check_owner
async def MAX_FLOOD_IN_PMS(event: CallbackQuery):
    x = "📃 **DEĞER:** `MAX_FLOOD_IN_PMS`\n\
    \n📋 **Açıklama:** `MAX_FLOOD_IN_PMS `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "MAX_FLOOD_IN_PMS"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"pmmenu")))
@check_owner
async def pmmenu(event: CallbackQuery):
    x = "📃 **DEĞER:** `pmmenu`\n\
    \n📋 **Açıklama:** `pmmenu `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "pmmenu"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"pmpermit_txt")))
@check_owner
async def pmpermit_txt(event: CallbackQuery):
    x = "📃 **DEĞER:** `pmpermit_txt`\n\
    \n📋 **Açıklama:** `pmpermit_txt `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "pmpermit_txt"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"pmpermit")))
@check_owner
async def pmpermit(event: CallbackQuery):
    x = "📃 **DEĞER:** `pmpermit`\n\
    \n📋 **Açıklama:** `pmpermit `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "pmpermit"
    z = "sspmmenu"
    await ss(event, x, y, z)


# Assıstant bot values callbacks
@doge.bot.on(CallbackQuery(data=compile(b"START_PIC")))
@check_owner
async def START_PIC(event: CallbackQuery):
    x = "📃 **DEĞER:** `START_PIC`\n\
    \n📋 **Açıklama:** `START_PIC `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "START_PIC"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"START_TEXT")))
@check_owner
async def START_TEXT(event: CallbackQuery):
    x = "📃 **DEĞER:** `START_TEXT`\n\
    \n📋 **Açıklama:** `START_TEXT `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "START_TEXT"
    z = "sspmmenu"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"START_BUTTON")))
@check_owner
async def START_BUTTON(event: CallbackQuery):
    x = "📃 **DEĞER:** `START_BUTTON`\n\
    \n📋 **Açıklama:** `START_BUTTON `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "START_BUTTON"
    z = "sspmmenu"
    await ss(event, x, y, z)


# CMD set values callback
@doge.bot.on(CallbackQuery(data=compile(b"CMDSET")))
@check_owner
async def CMDSET(event: CallbackQuery):
    x = "📃 **DEĞER:** `CMDSET`\n\
    \n📋 **Açıklama:** `CMDSET `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "CMDSET"
    z = "sshandler"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"SUDO_CMDSET")))
@check_owner
async def SUDO_CMDSET(event: CallbackQuery):
    x = "📃 **DEĞER:** `SUDO_CMDSET`\n\
    \n📋 **Açıklama:** `SUDO_CMDSET `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "SUDO_CMDSET"
    z = "sshandler"
    await ss(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"SNIP_CMDSET")))
@check_owner
async def SNIP_CMDSET(event: CallbackQuery):
    x = "📃 **DEĞER:** `SNIP_CMDSET`\n\
    \n📋 **Açıklama:** `SNIP_CMDSET `\n\
    \n🕹 **Değeri elde etmek için;**"
    y = "SNIP_CMDSET"
    z = "sshandler"
    await ss(event, x, y, z)


# TAG LOGGER MANUEL
@doge.bot.on(CallbackQuery(data=compile(b"TAG_LOGGER_GROUP_MANUEL")))
@check_owner
async def TAG_LOGGER_GROUP_MANUEL(event: CallbackQuery):
    x = "📃 **DEĞER:** `TAG_LOGGER_GROUP_ID`\n\
    \n📋 **Açıklama:** `Tag Logger Grubu `\n\
    \n🕹 **Değeri elde etmek için;**\
    \n`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "TAG_LOGGER_GROUP_ID"
    z = "TAG_LOGGER_GROUP"
    await ss(event, x, y, z)


# PM LOGGER için manuel grup açma
@doge.bot.on(CallbackQuery(data=compile(b"PM_LOGGER_GROUP_MANUEL")))
@check_owner
async def PM_LOGGER_GROUP_MANUEL(event: CallbackQuery):
    x = "📃 **DEĞER:** `PM Logger Grup ID`\n\
    \n📋 **Açıklama:** `Heroku Logger Grubu `\n\
    \n🕹 **Değeri elde etmek için;**\
    \n`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "PM_LOGGER_GROUP_ID"
    z = "PM_LOGGER_GROUP"
    await ss(event, x, y, z)


# heroku logger manuel grup açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hloggermanuelcreate")))
@check_owner
async def hloggermanuelcreate(event: CallbackQuery):
    x = "📃 **DEĞER:** `Heroku Logger Grup ID`\n\
    \n📋 **Açıklama:** `Heroku Logger Grubu `\n\
    \n🕹 **Değeri elde etmek için;**\
    \n`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "HLOGGER_ID"
    z = "hgloggrpc"
    # if gvar("DEV_MODE") != True: #Yakında
    #   return await event.answer("Birgeliştirici değilsiniz.", alert=True)
    await setapi(event, x, y, z)


# manuel FBAN grubu açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"fgapi")))
@check_owner
async def fgapi(event: CallbackQuery):
    x = "📃 **DEĞER:** `FBan Grup ID`\n\
    \n📋 **Açıklama:** `FBan Grubu `\n\
    \n🕹 **Değeri elde etmek için;**\
    \n`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "FBAN_GROUP_ID"
    z = "fgroup"
    await setapi(event, x, y, z)


# gizli kanalın manuel ayarlanma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"pcmanuel")))
@check_owner
async def pcmanuel(event: CallbackQuery):
    x = "📃 **DEĞER:** `Secret Channel ID`\n\
    \n📋 **Açıklama:** `Gizli kanal özelliği için ayarlanan kanal.`\n\
    \n🕹 **Değeri elde etmek için;**\
    \n`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz kanalın kimliğini bana gönderin.`"
    y = "PRIVATE_CHANNEL_ID"
    z = "sscg"
    await setapi(event, x, y, z)


##### APILER #####
@doge.bot.on(CallbackQuery(data=compile(b"cuapi")))
@check_owner
async def cuapi(event: CallbackQuery):
    x = "b"
    y = "CURRENCY_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"deapi")))
@check_owner
async def deapi(event: CallbackQuery):
    x = "📃 **API:** `DEEP API Key`\n\
    \n📋 **Açıklama:** `Fotoğraf ve videolardaki çıplaklık oranını ölçebilir ya da gruba atılan medyaların çıplaklık içermesine engel olabilirsiniz.`\n\
    \n🕹 **API Key'i elde etmek için;**\
    \n[Buraya](https://us11.list-manage.com/subscribe?u=ce17e59f5b68a2fd3542801fd&id=252aee70a1) `gidin ve hesap oluşturun. Ardından API key'i alıp bana gönderin.`"
    y = "DEEPAI_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"geapi")))
@check_owner
async def geapi(event: CallbackQuery):
    x = "📃 **API:** `GENIUS API Key`\n\
    \n📋 **Açıklama:** `Aradığınız şarkının sözlerini almanızı sağlar.`\n\
    \n🕹 **API Key'i elde etmek için;**\
    \n`Öncelikle` [Genius](https://genius.com/signup_or_login#) `sitesine kayıt olun. Sonrasında ise` [buradaki](https://genius.com/api-clients#] `ekrana gelip yeni 'client' oluşturun Size verdiği Token'i bana gönderin.`"
    y = "GENIUS_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ghapi")))
@check_owner
async def ghapi(event: CallbackQuery):
    x = "📃 **API:** `GITHUB ACCESS TOKEN`"
    y = "GITHUB_ACCESS_TOKEN"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"gdapi")))
@check_owner
async def gdapi(event: CallbackQuery):
    x = "f"
    y = ""
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"IBM_WATSON_CRED_URL")))
@check_owner
async def IBM_WATSON_CRED_URL(event: CallbackQuery):
    x = "g"
    y = "IBM_WATSON_CRED_URL"
    z = "ibmwcapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"IBM_WATSON_CRED_PASSWORD")))
@check_owner
async def IBM_WATSON_CRED_PASSWORD(event: CallbackQuery):
    x = "g"
    y = "IBM_WATSON_CRED_PASSWORD"
    z = "ibmwcapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ibmwcapi")))
@check_owner
async def ibmwcapi(event: CallbackQuery):
    buttons = [
        [
            Button.inline("IBM_WATSON_CRED_URL", data="IBM_WATSON_CRED_URL"),
            Button.inline("IBM_WATSON_CRED_PASSWORD", data="IBM_WATSON_CRED_PASSWORD"),
        ]
    ]
    buttons.append(get_back_button("apimenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"ipdapi")))
@check_owner
async def ipdapi(event: CallbackQuery):
    x = "h"
    y = "IPDATA_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"LASTFM_API")))
@check_owner
async def LASTFM_API(event: CallbackQuery):
    x = "i"
    y = "LASTFM_API"
    z = "lfmapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"LASTFM_USERNAME")))
@check_owner
async def LASTFM_USERNAME(event: CallbackQuery):
    x = "i"
    y = "LASTFM_USERNAME"
    z = "lfmapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"LASTFM_PASSWORD_PLAIN")))
@check_owner
async def LASTFM_PASSWORD_PLAIN(event: CallbackQuery):
    x = "i"
    y = "LASTFM_PASSWORD_PLAIN"
    z = "lfmapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"LASTFM_SECRET")))
@check_owner
async def LASTFM_SECRET(event: CallbackQuery):
    x = "i"
    y = "LASTFM_SECRET"
    z = "lfmapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"lfmapi")))
@check_owner
async def ibmwcapi(event: CallbackQuery):
    buttons = [
        [
            Button.inline("LASTFM_API", data="LASTFM_API"),
            Button.inline("LASTFM_USERNAME", data="LASTFM_USERNAME"),
        ],
        [
            Button.inline("LASTFM_PASSWORD_PLAIN", data="LASTFM_PASSWORD_PLAIN"),
            Button.inline("LASTFM_SECRET", data="LASTFM_SECRET"),
        ],
    ]
    buttons.append(get_back_button("apimenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"ocrsapi")))
@check_owner
async def ocrsapi(event: CallbackQuery):
    x = "j"
    y = "OCRSPACE_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"rbgapi")))
@check_owner
async def rbgapi(event: CallbackQuery):
    x = "l"
    y = "REMOVEBG_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"swapi")))
@check_owner
async def swapi(event: CallbackQuery):
    x = "m"
    y = "SPAMWATCH_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"SPOTIFY_DC")))
@check_owner
async def SPOTIFY_DC(event: CallbackQuery):
    x = "n"
    y = "SPOTIFY_DC"
    z = "spapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"SPOTIFY_KEY")))
@check_owner
async def SPOTIFY_KEY(event: CallbackQuery):
    x = "n"
    y = "SPOTIFY_KEY"
    z = "spapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"spapi")))
@check_owner
async def spapi(event: CallbackQuery):
    buttons = [
        [
            Button.inline("SPOTIFY_DC", data="SPOTIFY_DC"),
            Button.inline("SPOTIFY_KEY", data="SPOTIFY_KEY"),
        ],
    ]
    buttons.append(get_back_button("apimenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {gvar('mention')}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=buttons,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"ssapi")))
@check_owner
async def ssapi(event: CallbackQuery):
    x = "o"
    y = "SS_API"
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"woapi")))
@check_owner
async def woapi(event: CallbackQuery):
    x = "p"
    y = "WEATHER_API"
    await setapi(event, x, y)


# FBAN GRUBU İÇİN OTOMATİK GRUP AÇMA / DEĞERLERİ YAZMA
async def fgchelper(event: CallbackQuery):
    descript = "🚧 BU GRUBU SİLMEYİN!\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 FBAN özelliği çalışmayacaktır.\n\
    \n🧡 @DogeUserBot"
    gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeFBan.jpg")
    await sleep(0.75)
    rose = "@MissRose_Bot"
    _, groupid = await create_supergroup(
        "🐾 Dᴏɢᴇ FBᴀɴ Gʀᴜᴘ", doge, rose, descript, gphoto
    )
    await sleep(0.75)
    await add_bot_to_logger_group(doge, groupid, rose, "Rose")
    await sleep(0.75)
    descmsg = "**🚧 BU GRUBU SİLMEYİN!\
    \n🚧 BU GRUPTAN AYRILMAYIN!\
    \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 FBAN özelliği çalışmayacaktır!\n\
    \n**🧡 @DogeUserBot**"
    msg = await doge.send_message(groupid, descmsg)
    await sleep(0.25)
    await msg.pin()
    sgvar("FBAN_GROUP_ID", groupid)
    await event.edit(
        f"{gvar('mention')} Sizin için bir FBan grubu oluşturdum ve verileri veritabanına yazdım!",
        buttons=get_back_button("fgroup"),
    )
    LOGS.info("✅ FBAN_GROUP_ID için özel bir grup başarıyla oluşturdum!")


# HEROKU İÇİN OTOMATİK GRUP AÇMA İŞLEMİ
async def herokuloggergroupcreate(event: CallbackQuery):
    descript = "🚧 BU GRUBU SİLMEYİN!\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 Heroku Logger özelliği çalışmayacaktır.\n\
    \n🧡 @DogeUserBot"
    gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeHerokuLog.jpg")
    await sleep(0.75)
    _, groupid = await create_supergroup(
        "🐾 Doɢᴇ Hᴇʀoᴋᴜ Loɢɢᴇʀ Gʀᴜᴘ", doge, gvar("BOT_USERNAME"), descript, gphoto
    )
    await sleep(0.75)
    await add_bot_to_logger_group(doge, groupid, gvar("BOT_USERNAME"), "Doge")
    await sleep(0.75)
    descmsg = "**🚧 BU GRUBU SİLMEYİN!\
    \n🚧 BU GRUPTAN AYRILMAYIN!\
    \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 Heroku Logger özelliği çalışmayacaktır!\n\
    \n**🧡 @DogeUserBot**"
    msg = await doge.bot.send_message(groupid, descmsg)
    await sleep(0.25)
    await msg.pin()
    sgvar("HLOGGER_ID", groupid)
    await event.edit(
        f"{gvar('mention')} Sizin için bir Heroku Logger grubu oluşturdum ve verileri veritabanına yazdım!",
        buttons=get_back_button("hlogger"),
    )
    LOGS.info("✅ HLOGGER_ID için özel bir grup başarıyla oluşturdum!")


# GİZLİ KANAL İÇİN OTOMATİK KANAL AÇMA İŞLEMİ
async def privatechannel(event: CallbackQuery):
    descript = f"🚧 BU KANALI SİLMEYİN!\n\
    \n🗑 Eğer bu kanalı silerseniz,\
    \n🐾 Kaydederek iletme özelliği çalışmayacaktır.\n\
    \n🧡 @DogeUserBot"
    gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
    await sleep(0.75)
    _, channelid = await create_channel("🐾 Doɢᴇ Gɪzʟɪ Kᴀɴᴀʟ", doge, descript, gphoto)
    await sleep(0.75)
    descmsg = f"**🚧 BU KANALI SİLMEYİN!\
    \n🚧 BU KANALDAN AYRILMAYIN!\
    \n🚧 BU KANALI DEĞİŞTİRMEYİN!**\n\
    \n🗑 Eğer bu kanalı silerseniz,\
    \n🐾 Kaydederek iletme özelliği çalışmayacaktır!\n\
    \n**🧡 @DogeUserBot**"
    msg = await doge.send_message(channelid, descmsg)
    await sleep(0.25)
    await msg.pin()
    sgvar("PRIVATE_CHANNEL_ID", channelid)
    await event.edit(
        f"{gvar('mention')} Sizin için bir Gizli Kanal oluşturdum ve verileri veritabanına yazdım!",
        buttons=get_back_button("sscg"),
    )
    LOGS.info("✅ PRIVATE_CHANNEL_ID için özel bir grup başarıyla oluşturdum!")


# PM LOGGER İÇİN OTOMATİK GRUP AÇMA İŞLEMİ
async def pmloggeraurocreate(event: CallbackQuery):
    descript = "🚨 BU GRUBU SİLMEYİN!\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 PM özelliği çalışmayacaktır.\n\
    \n🧡 @DogeUserBot"
    gphoto = await doge.upload_file(file="userbot/helpers/resources/DogePmLog.jpg")
    await sleep(0.75)
    _, groupid = await create_supergroup(
        "🐾 Doɢᴇ Hᴇʀoᴋᴜ Pᴍ Gʀᴜᴘ", doge, gvar("BOT_USERNAME"), descript, gphoto
    )
    await sleep(1)
    await add_bot_to_logger_group(doge, groupid, gvar("BOT_USERNAME"), "Doge")
    await sleep(1)
    descmsg = """🚨 **Bu grubu silmeyin!        
🚨 Bu gruptan ayrılmayın!        
🚨 Bu grubu değiştirmeyin!**
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖      
🗑 **Eğer bu grubu silecek olursanız,        
🐾 [Doge](http://t.me/DogeUserBot) çalışmayacaktır!**
        
🧡 @DogeUserBot"""
    msg = await doge.bot.send_message(groupid, descmsg)
    await sleep(0.25)
    await msg.pin()
    sgvar("PM_LOGGER_GROUP_ID", groupid)
    await event.edit(
        f"{gvar('mention')} Sizin için bir PM Logger grubu oluşturdum ve verileri veritabanına yazdım!",
        buttons=get_back_button("hlogger"),
    )
    LOGS.info("✅ PM_LOGGER_GROUP_ID için özel bir grup başarıyla oluşturdum!")


# TAG LOGGER İÇİN otomatik grup açma
async def tagloggeraurocreate(event: CallbackQuery):
    descript = "🚨 BU GRUBU SİLMEYİN!\n\
    \n🗑 Eğer bu grubu silerseniz,\
    \n🐾 Tag Logger özelliği çalışmayacaktır.\n\
    \n🧡 @DogeUserBot"
    gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeTagLog.jpg")
    await sleep(0.75)
    _, groupid = await create_supergroup(
        "🐾 Doɢᴇ Tᴀɢ Loɢɢᴇʀ", doge, gvar("BOT_USERNAME"), descript, gphoto
    )
    await sleep(1)
    await add_bot_to_logger_group(doge, groupid, gvar("BOT_USERNAME"), "Doge")
    await sleep(1)
    descmsg = """🚨 **Bu grubu silmeyin!        
🚨 Bu gruptan ayrılmayın!        
🚨 Bu grubu değiştirmeyin!**
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖      
🗑 **Eğer bu grubu silecek olursanız,        
🐾 Tag Logger çalışmayacaktır!**
        
🧡 @DogeUserBot"""
    msg = await doge.bot.send_message(groupid, descmsg)
    await sleep(0.25)
    await msg.pin()
    sgvar("TAG_LOGGER_GROUP_ID", groupid)
    await event.edit(
        f"{gvar('mention')} Sizin için bir Tag Logger grubu oluşturdum ve verileri veritabanına yazdım!",
        buttons=get_back_button("hlogger"),
    )
    LOGS.info("✅ TAG_LOGGER_GROUP_ID için özel bir grup başarıyla oluşturdum!")


# herokudan api key ile veri çekme
if HEROKU_API_KEY:
    heroku = from_key(HEROKU_API_KEY)
    app = heroku.app(HEROKU_APP_NAME)

# alınan değer ile config var yazdırma işlemi
async def hheroku(e, vname, vinfo, z=None):
    try:
        app.config()[vname] = vinfo
    except Exception:
        if z:
            return await e.edit(
                f"`🚨 Bir şeyler ters gitti!`\n\
                \n**Hata:** `{e}`",
                buttons=get_back_button(z),
            )
        else:
            return await e.edit(
                f"`🚨 Bir şeyler ters gitti!`\n\
                \n**Hata:** `{e}`",
                buttons=get_back_button("setmenu"),
            )


# alınan değer ile verisini databseye yazdırma işlemi
async def setdv(e, vname, vinfo, z=None):
    try:
        sgvar(vname, vinfo)
    except Exception:
        if z:
            return await e.edit(
                f"`🚨 Bir şeyler ters gitti!`\n\
                \n**Hata:** `{e}`",
                buttons=get_back_button(z),
            )
        else:
            return await e.edit(
                f"`🚨 Bir şeyler ters gitti!`\n\
                \n**Hata:** `{e}`",
                buttons=get_back_button("setmenu"),
            )


# heroku configleri değiştirilme işlemi
async def sh(event: CallbackQuery, x, y, z=None):
    await event.delete()
    chat = event.sender_id
    async with event.client.conversation(chat) as conv:
        await conv.send_message(x)
        response = await newmsgres(conv, chat)
        vinfo = response.message.message
        if vinfo.startswith(("/")):
            return
        if vinfo == "/cancel":
            if z:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button(z),
                    link_preview=False,
                )
            else:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button("herokumenu"),
                    link_preview=False,
                )
        await hheroku(event, y, vinfo, z)
        if z:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button(z),
                link_preview=False,
            )
        else:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button("herokumenu"),
                link_preview=False,
            )


# API harici ayarların değiştirilme işlemi
async def ss(event: CallbackQuery, x, y, z=None):
    await event.delete()
    chat = event.sender_id
    async with event.client.conversation(chat) as conv:
        xmsg = await conv.send_message(x)
        response = await newmsgres(conv, chat)
        if "PIC" in y:
            rpic = response.message
            try:
                if (type(rpic.media) == MessageMediaDocument) or (
                    type(rpic.media) == MessageMediaPhoto
                ):
                    downloaded_file_name = await event.client.download_media(
                        rpic, TEMP_DIR
                    )
                    try:
                        if downloaded_file_name.endswith((".webp")):
                            resize_image(downloaded_file_name)
                        media_urls = upload_file(downloaded_file_name)
                        vinfo = f"https://telegra.ph{media_urls[0]}"

                    except AttributeError:
                        await xmsg.edit(
                            "🚨 `Telegraph bağlantısı oluşturulurken hata oluştu!`"
                        )
                        await sleep(10)
                        return await xmsg.delete()

                    except TelegraphException as exc:
                        return await xmsg.edit(f"**🚨 Hata:**\n➡️ `{str(exc)}`")

            except Exception as e:
                LOGS.error(e)

        elif y == "START_BUTTON":
            blink = response.message.message
            SBLINK = blink.split(";")[1]
            for i in SBLINK:
                if url(i):
                    vinfo = blink
                elif not url(i):
                    if z:
                        return await xmsg.edit(
                            "🚨 `Lütfen bağlantıyı kontrol edin ve tekrar deneyin!`",
                            buttons=get_back_button(z),
                        )
                    else:
                        return await xmsg.edit(
                            "🚨 `Lütfen bağlantıyı kontrol edin ve tekrar deneyin!`",
                            buttons=get_back_button("ssmenu"),
                        )

        else:
            vinfo = response.message.message
        if vinfo.startswith(("/", "!")):
            return
        if vinfo == "/cancel":
            if z:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button(z),
                    link_preview=False,
                )
            else:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button("ssmenu"),
                    link_preview=False,
                )
        await setdv(event, y, vinfo, z)
        if z:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button(z),
                link_preview=False,
            )
        else:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button("ssmenu"),
                link_preview=False,
            )


# gelen API keylerde değiştirme işlemi
async def setapi(event: CallbackQuery, x, y, z=None):
    await event.delete()
    chat = event.sender_id
    async with event.client.conversation(chat) as conv:
        await conv.send_message(x)
        response = await newmsgres(conv, chat)
        vinfo = response.message.message
        if vinfo.startswith(("/", "!")):
            return
        if vinfo == "/cancel":
            if z:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button(z),
                    link_preview=False,
                )
            else:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button("apimenu"),
                    link_preview=False,
                )
        await setdv(event, y, vinfo, z)
        if z:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button(z),
                link_preview=False,
            )
        else:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {gvar('mention')}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button("apimenu"),
                link_preview=False,
            )
