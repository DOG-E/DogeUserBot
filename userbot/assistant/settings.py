# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from re import compile

from telethon import Button
from telethon.events import CallbackQuery

from . import check_owner, doge, get_back_button, mention, newmsgres, sgvar

plugin_category = "bot"


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


async def setdv(e, vname, vinfo):
    try:
        sgvar(vname, vinfo)
    except BaseException:
        return await e.edit("`🚨 Bir şeyler ters gitti!`")


async def setapi(event: CallbackQuery, x, y, z=None):
    await event.delete()
    chat = event.sender_id
    async with event.client.conversation(chat) as conv:
        await conv.send_message(x)
        response = await newmsgres(conv, chat)
        vinfo = response.message.message
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


@doge.bot.on(CallbackQuery(data=compile(b"cgapi")))
@check_owner
async def cgapi(event: CallbackQuery):
    apis = [
        [
            Button.inline("FBAN GRUBU", data="fgapi"),
            Button.inline("GİZLİ KANAL", data="pcapi"),
        ],
    ]
    apis.append(get_back_button("apimenu"))
    await event.edit(
        f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
        \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
        \n◽ Doɢᴇ oғ {mention}\n\
        \n🧶 Ayarlamak istediğiniz değişkeni seçin:**",
        buttons=apis,
        link_preview=False,
    )


@doge.bot.on(CallbackQuery(data=compile(b"fgapi")))
@check_owner
async def fgapi(event: CallbackQuery):
    x = "a"
    y = "FBAN_GROUP_ID"
    z = "cgapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"fgapi")))
@check_owner
async def fgapi(event: CallbackQuery):
    x = "a"
    y = "FBAN_GROUP_ID"
    z = "cgapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"pcapi")))
@check_owner
async def pcapi(event: CallbackQuery):
    x = "aa"
    y = "PRIVATE_CHANNEL_ID"
    z = "cgapi"
    await setapi(event, x, y, z)


@doge.bot.on(CallbackQuery(data=compile(b"cuapi")))
@check_owner
async def cuapi(event: CallbackQuery):
    x = "b"
    y = "CURRENCY_API"
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"deapi")))
@check_owner
async def deapi(event: CallbackQuery):
    x = "c"
    y = "DEEPAI_API"
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"geapi")))
@check_owner
async def geapi(event: CallbackQuery):
    x = "d"
    y = "GENIUS_API"
    await setapi(event, x, y)


@doge.bot.on(CallbackQuery(data=compile(b"ghapi")))
@check_owner
async def ghapi(event: CallbackQuery):
    x = "e"
    y = ""
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
