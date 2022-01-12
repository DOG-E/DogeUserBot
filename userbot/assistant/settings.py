# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import logging
from re import compile
from time import sleep

from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.channels import ToggleSignaturesRequest

from userbot import BOT_USERNAME, FBAN_GROUP_ID
from userbot.sql_helper.globals import gvar
from ..utils.tools import create_channel, create_supergroup
from . import check_owner, doge, get_back_button, mention, newmsgres, sgvar

plugin_category = "bot"
LOGS = logging.getLogger("DogeUserBot")

# ilk ayarlar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"setmenu")))
@check_owner
async def settings(event):
    options = [
        [
            Button.inline("🌐 Dɪʟ", data="langmenu"),
        ],
        [
            Button.inline("🧶 Aᴘɪ'ʟᴇʀ", data="apimenu"),
        ],
        [
            Button.inline("🐾 Mᴇɴᴜ", data="mainmenu"),
        ],
    ]
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {mention}\n\
        \n✨ Ayarlamak istediğinizi aşağıdan seçin:**",
        buttons=options,
        link_preview=False,
    )

# api - grup id'leri menüsü
@doge.bot.on(CallbackQuery(data=compile(b"apimenu")))
@check_owner
async def apisetter(event: CallbackQuery):
    apis = [
        [
            Button.inline("GRUP & KANAL", data="cgapi"),
            Button.inline("CURRENCY", data="cuapi"),
        ],
        [Button.inline("Dᴇᴇᴘ", data="deapi"), Button.inline("GENIUS", data="geapi")],
        [
            Button.inline("GITHUB", data="ghapi"),
            Button.inline("GOOGLE DRIVE", data="gdapi"),
        ],
        [
            Button.inline("IBM WATSON", data="ibmwcapi"),
            Button.inline("IP DATA", data="ipdapi"),
        ],
        [
            Button.inline("LAST FM", data="lfmapi"),
            Button.inline("OCR SPACE", data="ocrsapi"),
        ],
        [
            Button.inline("RANDOM STUFF", data="rsapi"),
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
        \n◽ Doɢᴇ oғ {mention}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=apis,
        link_preview=False,
    )

# alınan değer ile verisini databseye yazırma işlemi
async def setdv(e, vname, vinfo):
    try:
        sgvar(vname, vinfo)
    except BaseException:
        return await e.edit("`🚨 Bir şeyler ters gitti!`")

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
                    \n◽ Doɢᴇ oғ {mention}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button(z),
                    link_preview=False,
                )
            else:
                return await conv.send_message(
                    f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                    \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                    \n◽ Doɢᴇ oғ {mention}\n\
                    \n⛔ İptal edildi!**",
                    buttons=get_back_button("apimenu"),
                    link_preview=False,
                )
        await setdv(event, y, vinfo)
        if z:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {mention}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button(z),
                link_preview=False,
            )
        else:
            await conv.send_message(
                f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n◽ Doɢᴇ oғ {mention}\n\
                \n✅ {y} değişkenini başarıyla değiştirdim.**",
                buttons=get_back_button("apimenu"),
                link_preview=False,
            )


# grup/kanalların ayar menüsü
@doge.bot.on(CallbackQuery(data=compile(b"cgapi")))
@check_owner
async def cgapi(event: CallbackQuery):
    apis = [
        [
            Button.inline("FBAN GRUBU", data="fgroup"),
            Button.inline("GİZLİ KANAL", data="pccreate"),
        ],
        [
            Button.inline("Heroku Logger", data="hlogger")
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data="apimenu")
        ]
    ]
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {mention}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=apis,
        link_preview=False,
    )


# heroku logger menüsü
@doge.bot.on(CallbackQuery(data=compile(b"hlogger")))
@check_owner
async def hlogger(event: CallbackQuery):
    buttons= [
        [
            Button.inline("✅ Aç", data="hgloggeron"),
            Button.inline("❎ Kapat", data="hgloggeroff")
        ],
        [
            Button.inline("HLog Grubu Ayarla", data="hgloggrpc")
        ]
    ]
    await event.edit(f"Heroku Logger özelliği menünüzü özelleştirin.", buttons=buttons)


# heroku logger özelliğini kapatma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hgloggeroff")))
@check_owner
async def hgloggeroff(event: CallbackQuery):
    if gvar("HEROKULOGGER") == False or None:
        return await event.answer(f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\nHeroku Logger özelliğiniz zaten kapalı!", alert=True)
    if gvar("HEROKULOOGER") == True:
        await sgvar("HEROKULOGGER", False)
        return await event.answer(f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\ Heroku Logger özelliğiniz başarıyla kapatıldı", alert=True)


# heroku logger özelliğini açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hgloggeron")))
@check_owner
async def hgloggeron(event: CallbackQuery):
    buttons = [
        [
            Button.inline("✅ Evet", data="hgloggerautocreate"),
            Button.inline("❎ Hayır", data="hloggermanuelcreate"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data = "hgloggeron")
        ]
    ]
    if gvar("HEROKULOGGER") == True:
        return await event.answer(f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğiniz zaten açık!", alert=True)
    if gvar("HLOGGER_ID") is None and gvar("HEROKULOGGER") == False:
        await event.answer(f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğini açmak için öncelikle bir grup ayarlamanız gerekir. Sizi grup ayarlama ekranına yönlendiriyorum...")
        await event.edit(f"Heroku Logger özelliği için grubunuzun bot tarafından oluştulurulmasını isterseniz__ '✅ Evet' __düğmesine, kendiniz oluşturduğunuz bir grubu ayarlamak için__ '❎ Hayır' __düğmesine basınız.__", buttons=buttons)
    if gvar("HEROKULOGGER") == False and gvar("HLOOGER_ID") is not None:
        await sgvar("HEROKLOGGER", True)
        await event.answer(f"🐶 Doɢᴇ UsᴇʀBoᴛ\n\n Heroku Logger özelliğiniz başarıyla etkinleştirildi! Veritabanına kayıtlı gruba Heroku Log eylemi başlatılacaktır.")



# heroku logger grup açma seçenekleri
@doge.bot.on(CallbackQuery(data=compile(b"hgloggrpc")))
@check_owner
async def hgloggrpc(event: CallbackQuery):
    buttons = [
        [
            Button.inline("✅ Evet", data="hgloggerautocreate"),
            Button.inline("❎ Hayır", data="hloggermanuelcreate"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data = "cgapi")
        ]
    ]
    await event.edit(f"Heroku Logger özelliği için grubunuzun bot tarafından oluştulurulmasını isterseniz__ '✅ Evet' __düğmesine, kendiniz oluşturduğunuz bir grubu ayarlamak için__ '❎ Hayır' __düğmesine basınız.__", buttons=buttons)


# heroku logger için otomatik grup açma işlemi 
@doge.bot.on(CallbackQuery(data=compile(b"hgloggerautocreate")))
@check_owner
async def hgloggerautocreate(event: CallbackQuery):
    if gvar("HLOGGER_ID") is None:
        await event.edit(f"{mention} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin...")
        await herokuloggergroupcreate(event)
    elif gvar("HLOGGER_ID") is not None:
        try:
            a = await doge.bot.send_message(gvar("HLOGGER_ID"), f"Heroku Logger Grubu Test Mesajı!")
            await a.delete()
            return await event.edit(f"Heroku Logger için zaten kayıtlı bir grubunuz var! Grup oluşturma işlemini iptal ediyorum", buttons=get_back_button("hgloggrpc"))
        except Exception as e:
            LOGS.warning(f"Heroku Logger grubuna ulaşılamadı yeni grup açılıyor... Hata Raporu: {e}")
            await event.edit(f"{mention} Veritabanınızda kayıtlı gruba erişilemedi! Sizin için bir Heroku Logger Kayıt grubu oluşturuyorum! Lütfen bekleyin...")
            await herokuloggergroupcreate(event)


# heroku logger manuel grup açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"hloggermanuelcreate")))
@check_owner
async def hloggermanuelcreate(event: CallbackQuery):
    x = "📃 **DEĞER:** `Heroku Logger Grup ID`\
\
📋 **Açıklama:** `Heroku Logger Grubu `\
\
🕹 **Değeri elde etmek için;**\
`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "HLOGGER_ID"
    z = "hgloggrpc"
    await setapi(event, x, y, z)


# fban grubu açmak için seçenekler menüsü
@doge.bot.on(CallbackQuery(data=compile(b"fgroup")))
@check_owner
async def fggroup(event: CallbackQuery):
    buttons = [
        [
            Button.inline("✅ Evet", data="fgcreate"),
            Button.inline("❎ Hayır", data="fgapi"),
        ],
        [
            Button.inline("⬅️️ Gᴇʀɪ", data = "apimenu")
        ]
    ]
    await event.edit(f"**{mention} [Rose](https://t.me/MissRose_Bot) için FBAN Grup ayarları!**\n\
        \n__FBAN grubunuzun için bot tarafından oluştulurulmasını isterseniz__ '✅ Evet' __düğmesine, kendiniz oluşturduğunuz bir grubu ayarlamak için__ '❎ Hayır' __düğmesine basınız.__", buttons=buttons, link_preview=False) 


# manuel FBAN grubu açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"fgapi")))
@check_owner
async def fgapi(event: CallbackQuery):
    x = "📃 **DEĞER:** `FBan Grup ID`\
\
📋 **Açıklama:** `FBan Grubu `\
\
🕹 **Değeri elde etmek için;**\
`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz grubunuzun kimliğini bana gönderin.`"
    y = "FBAN_GROUP_ID"
    z = "fgroup"
    await setapi(event, x, y, z)


# otomatik FBAN grubu açma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"fgcreate")))
@check_owner
async def fggrupcreate(event: CallbackQuery):
    if gvar("FBAN_GROUP_ID") is None:
        await event.edit(f"{mention} Veritabanına kayıtlı bir grubunuz yok. Sizin için bir FBan grubu oluşturuyorum! Lütfen bekleyin...")
        await fgchelper(event)
    else:
        try:
            a = await doge.send_message(FBAN_GROUP_ID, "FBan Grup Deneme mesajı!")
            await a.delete()
            return await event.edit(f"FBan için zaten bir grubunuz var! Grup oluşturma işlemini iptal ediyorum...", buttons=get_back_button("fgroup"))
        except Exception:
            await event.edit(f"{mention} Veritabanına kayıtlı grubunuza erişiminiz yok. Sizin için bir FBan grubu oluşturuyorum! Lütfen bekleyin...")
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
            Button.inline("⬅️️ Gᴇʀɪ", data = "cgapi")
        ]
    ]
    await event.edit(f"__Gizli kanalınız için DogeUserBot tarafından oluştulurulmasını isterseniz__ '✅ Evet' __düğmesine, kendiniz oluşturduğunuz bir grubu ayarlamak için__ '❎ Hayır' __düğmesine basınız.__", buttons=buttons)


# gizli kanalın otomatik ayarlanma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"pcauto")))
@check_owner
async def pcmanuel(event: CallbackQuery):
    if gvar("PRIVATE_CHANNEL_ID") is not None:
        try:
            a = await doge.send_message(gvar("PRIVATE_CHANNEL_ID"), f"Gizli kanal Deneme mesajı!")
            await a.delete()
            return await event.edit(f"Gizli Kanal özelliği için zaten hazırda bi kanalınız var! Yeni kanal açma işlemini iptal ediyorum.", buttons=get_back_button("pccreate"))
        except Exception as e:
            LOGS.warning(f"Gizli kanala erişim sağlanamadı yeni kanal açılıyor... Hata Raporu: {e}")
            await event.edit(f"{mention} Veritabanınızda kayıtlı gizli kanala erişilemedi! Sizin için bir Gizli Kanal oluşturuyorum! Lütfen bekleyin...")
            await privatechannel(event)
    if gvar("PRIVATE_CHANNEL_ID") is None:
        await event.edit(f"Veritabanında kayıtlı bir Gizli Kanal değeri bulunamadı! Sizin için yeni bir Gizli Kamal oluşturuyoruM! Lütfen bekleyin...")


# gizli kanalın manuel ayarlanma işlemi
@doge.bot.on(CallbackQuery(data=compile(b"pcmanuel")))
@check_owner
async def pcmanuel(event: CallbackQuery):
    x = "📃 **DEĞER:** `Secret Channel ID`\
\
📋 **Açıklama:** `Gizli Kanal özelliği için ayarlanan kanal. `\
\
🕹 **Değeri elde etmek için;**\
`Yeni bir oluşturduğunuz veya önceden oluşturmuş olduğunuz kanalın kimliğini bana gönderin.`"
    y = "PRIVATE_CHANNEL_ID"
    z = "cgapi"
    await setapi(event, x, y, z)


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
    x = "📃 **API:** `DEEP API Key`\
\
📋 **Açıklama:** `Fotoğraf ve videolardaki çıplaklık oranını ölçebilir ya da gruba atılan medyaların çıplaklık içermesine engel olabilirsiniz.`\
\
🕹 **API Key'i elde etmek için;**\
[Buraya](https://us11.list-manage.com/subscribe?u=ce17e59f5b68a2fd3542801fd&id=252aee70a1) `gidin ve hesap oluşturun. Ardından API key'i alıp bana gönderin.`"
    y = "DEEPAI_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"geapi")))
@check_owner
async def geapi(event: CallbackQuery):
    x = "📃 **API:** `GENIUS API Key`\
\
📋 **Açıklama:** `Aradığınız şarkının sözlerini almanızı sağlar.`\
\
🕹 **API Key'i elde etmek için;**\
`Öncelikle` [Genius (https://genius.com/signup_or_login#)](https://genius.com/signup_or_login#) `sitesine kayıt olun. Sonrasında ise` [buradaki](https://genius.com/api-clients#] `ekrana gelip yeni 'client' oluşturun Size verdiği Token'i bana gönderin.`"
    y = "GENIUS_API"
    z = "apimenu"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"ghapi")))
@check_owner
async def ghapi(event: CallbackQuery):
    x = "📃 **API:** `GITHUB ACCESS TOKEN`"
    y = "GITHUB_ACCESS_TOKEN"
    z = "apimenu"
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"gdapi")))
@check_owner
async def gdapi(event: CallbackQuery):
    x = "f"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"ibmwcapi")))
@check_owner
async def ibmwcapi(event: CallbackQuery):
    x = "g"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"ipdapi")))
@check_owner
async def ipdapi(event: CallbackQuery):
    x = "h"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"lfmapi")))
@check_owner
async def lfmapi(event: CallbackQuery):
    x = "i"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"ocrsapi")))
@check_owner
async def ocrsapi(event: CallbackQuery):
    x = "j"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"rsapi")))
@check_owner
async def rsapi(event: CallbackQuery):
    x = "k"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"rbgapi")))
@check_owner
async def rbgapi(event: CallbackQuery):
    x = "l"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"swapi")))
@check_owner
async def swapi(event: CallbackQuery):
    x = "m"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"spapi")))
@check_owner
async def spapi(event: CallbackQuery):
    x = "n"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"ssapi")))
@check_owner
async def ssapi(event: CallbackQuery):
    x = "o"
    y = ""
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"woapi")))
@check_owner
async def woapi(event: CallbackQuery):
    x = "p"
    y = ""
    await setapi(event, x, y)

# FBAN GRUBU İÇİN OTOMATİK GRUP AÇMA / DEĞERLERİ YAZMA
async def fgchelper(event:CallbackQuery):
        descript = f"🚧 BU GRUBU SİLMEYİN!\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 FBAN özelliği çalışmayacaktır.\n\
        \n🧡 @DogeUserBot"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        sleep(0.75)
        _, groupid = await create_supergroup(
            "🐾 Dᴏɢᴇ FBᴀɴ Gʀᴜᴘ", doge, "@MissRose_Bot", descript, gphoto
        )
        sleep(0.75)
        descmsg = f"**🚧 BU GRUBU SİLMEYİN!\
        \n🚧 BU GRUPTAN AYRILMAYIN!\
        \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 FBAN özelliği çalışmayacaktır!\n\
        \n**🧡 @DogeUserBot**"
        msg = await doge.send_message(groupid, descmsg)
        sleep(0.25)
        await msg.pin()
        sgvar("FBAN_GROUP_ID", groupid)
        await event.edit(f"{mention} Sizin için bir FBan grubu oluşturdum ve verileri veritabanına yazdım!", buttons=get_back_button("fgroup"))
        LOGS.info("✅ FBAN_GROUP_ID için özel bir grup başarıyla oluşturdum!")

# HEROKU İÇİN OTOMATİK GRUP AÇMA İŞLEMİ
async def herokuloggergroupcreate(event:CallbackQuery):
        descript = f"🚧 BU GRUBU SİLMEYİN!\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Heroku Logger özelliği çalışmayacaktır.\n\
        \n🧡 @DogeUserBot"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        sleep(0.75)
        _, groupid = await create_supergroup(
            "🐾 Doɢᴇ Hᴇʀoᴋᴜ Loɢɢᴇʀ Gʀᴜᴘ", doge, BOT_USERNAME, descript, gphoto
        )
        sleep(0.75)
        descmsg = f"**🚧 BU GRUBU SİLMEYİN!\
        \n🚧 BU GRUPTAN AYRILMAYIN!\
        \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Heroku Logger özelliği çalışmayacaktır!\n\
        \n**🧡 @DogeUserBot**"
        msg = await doge.send_message(groupid, descmsg)
        sleep(0.25)
        await msg.pin()
        sgvar("HLOGGER_ID", groupid)
        await event.edit(f"{mention} Sizin için bir Heroku Logger grubu oluşturdum ve verileri veritabanına yazdım!", buttons=get_back_button("hlogger"))
        LOGS.info("✅ HLOGGER_ID için özel bir grup başarıyla oluşturdum!")


# GİZLİ KANAL İÇİN OTOMATİK KANAL AÇMA İŞLEMİ
async def privatechannel(event:CallbackQuery):
        descript = f"🚧 BU KANALI SİLMEYİN!\n\
        \n🗑 Eğer bu kanalı silerseniz,\
        \n🐾 Kaydederek iletme özelliği çalışmayacaktır.\n\
        \n🧡 @DogeUserBot"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        sleep(0.75)
        _, channelid = await create_channel(
            "🐾 Doɢᴇ Gɪzʟɪ Kᴀɴᴀʟ", doge, descript, gphoto
        )
        sleep(0.75)
        descmsg = f"**🚧 BU KANALI SİLMEYİN!\
        \n🚧 BU KANALDAN AYRILMAYIN!\
        \n🚧 BU KANALI DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu kanalı silerseniz,\
        \n🐾 Kaydederek iletme özelliği çalışmayacaktır!\n\
        \n**🧡 @DogeUserBot**"
        msg = await doge.send_message(channelid, descmsg)
        sleep(0.25)
        await msg.pin()
        sgvar("PRIVATE_CHANNEL_ID", channelid)
        await event.edit(f"{mention} Sizin için bir Gizli Kanal oluşturdum ve verileri veritabanına yazdım!", buttons=get_back_button("cgapi"))
        LOGS.info("✅ PRIVATE_CHANNEL_ID için özel bir grup başarıyla oluşturdum!")