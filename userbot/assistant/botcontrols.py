# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from datetime import datetime

from telethon import Button
from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    Config,
    _format,
    dgvar,
    doge,
    edl,
    eor,
    gvar,
    logging,
    only_botlog,
    reply_id,
    sgvar,
    sudo_owner,
    time_formatter,
)
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)

# denemeler için kısa süreliğine var silenecek
@doge.shiba_cmd(
    pattern=f"^/(aylak|a)$",
    incoming=True,
    func=lambda e: e.is_group,
)
async def grup_start(event):
    obl = only_botlog(event)
    if obl:
        user = await doge.get_me()
        my_mention = f"[{user.first_name}](tg://user?id={user.id})"
        buttons = [
            (Button.inline("✨ Aʏᴀʀʟᴀʀ", data="setmenu"),)(  # noqa
                Button.inline("Help", data="backmainmenu")
            ),  # noqa
        ]
        # if not event.is_private:  # and event.chat_id == BOTLOG_CHATID:
        await event.reply(
            f"**🐶 Hey!\
                \n🐾 Merhaba {my_mention}!\n\
                \n💬 Bu bir test mesajıdır**\n\
                \nBOTLOG_CHATID = {BOTLOG_CHATID}\n\
                \nevent.chat_id = {event.chat_id}",
            buttons=buttons,
        )


@doge.shiba_cmd(
    pattern=f"^/(start|ba[sş]lat)({gvar('BOT_USERNAME')})?([\s]+)?$",
    incoming=True,
    func=lambda e: e.is_group,
)
@sudo_owner
async def grup_start(event):
    user = await doge.get_me()
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    buttons = [
        (Button.inline("🐕‍🦺 ʏᴀʀᴅɪᴍ", data="backmainmenu"),),
    ]
    if not event.is_private:  # and chat.id == BOTLOG_CHATID:
        await event.reply(
            f"**🐶 Hey!\
        \n🐾 Merhaba {my_mention}!\n\
        \n💬 Sana nasıl yardımcı olabilirim?**\n",
            buttons=buttons,
        )


@doge.shiba_cmd(pattern=f"^/(help|yard[ıi]m)({gvar('BOT_USERNAME')})?([\s]+)?$")
async def bot_help(event):
    if not event.is_private and event.chat_id == BOTLOG_CHATID:
        await event.reply(
            f"""🐶 **Botun Komutları:**

🚨 **Nᴏᴛ:** Buradaki komular yalnızca [bu bot](http://t.me/Doge_278943_Bot) için çalışır! 

🕹 **Kᴏᴍᴜᴛ:** `/uinfo` ya da `/kbilgi` <kullanıcının mesajını yanıtlayarak>
📄 **Bɪʟɢɪ:** İletilen çıkartmaların/emojilerin ileti etiketi olmadığından ileti olarak sayılmazlar bu  yüzden komut sadece normal iletilmiş mesajlarda çalışır.
📍 **Nᴏᴛ:** Tüm iletilen mesajlar için çalışır.İletilen mesajlar gizlilik ayarları kapalı olanlar için bile!

🕹 **Kᴏᴍᴜᴛ:** `/ban` ya da `/yasakla` <Kullanıcı ID/Kullanıcı Adı> <Sebep>
📄 **Bɪʟɢɪ:** Komutu kullanıcı mesajını yanıtlayarak sebeple birlikte kullanın. Böylece bottan yasaklandığınız gibi bildirilecek ve mesajları size daha fazla iletilmeyecektir.
📍 **Nᴏᴛ:** Sebep Kullanımı zorunludur. Sebep olmazsa çalışmayacaktır.

🕹 **Kᴏᴍᴜᴛ:** `/unban` ya da `/yasakac` <Kullanıcı ID/Kullanıcı Adı> <Sebep>
📄 **Bɪʟɢɪ:** Kullanıcının bottanyasağını kaldırmak için kullanıcının mesajını yanıtlayrak ya da ID/Kullanıcı Adı yazarak kullanın.
📍 **Nᴏᴛ:** Yasaklananlar listesini görmek için `.botbans` ya da `.yasaklananlar` komutunu kullanın.

🕹 **Kᴏᴍᴜᴛ:** `/broadcast` - `/yayin`
📄 **Bɪʟɢɪ:** Botunu kullananan/başlatan kullanıcıların listesini görmek için `.botusers` ya da `.kullanicilar` komutunu kullanın
📍 **Nᴏᴛ:** Kullanıcı botu durdurdu veya engellediyse, veritabanınızdan kaldırılacaktır. Bot kullanıcıları listesinden silinir."""
        )


@doge.shiba_cmd(pattern=f"^/(settings|ayarlar)({gvar('BOT_USERNAME')})?([\s]+)?$")
@sudo_owner
async def settings(event):
    user = await event.get_sender()
    options = [
        [
            Button.inline("🧶 Aᴘɪ'ʟᴇʀ", data="apimenu"),
        ],
        [
            Button.inline("🐾 Sᴇçᴇɴᴇᴋʟᴇʀ", data="ssmenu"),
            Button.inline("🧊 Hᴇʀᴏᴋᴜ", data="herokumenu"),
        ],
        [
            Button.inline("🌐 Dɪʟ", data="langmenu"),
        ],
    ]
    bot_username = gvar("BOT_USERNAME")
    if bot_username.startswith("@"):
        new_bot_username = bot_username[-1:]
    buttons = [
        [
            Button.url(
                f"Buraya Tıklayın",
                url=f"https://t.me/{new_bot_username}?start=settings",
            ),
        ],
    ]
    ment = f"[{user.first_name}](tg://user?id={user.id})"
    if not event.is_private and event.chat_id == BOTLOG_CHATID:
        return await event.reply(
            f"🐾 Selam {ment}! Lütfen ayarlarınızı yapmak için aşağıdaki düğmeye tıklayın.",
            buttons=buttons,
        )
    elif event.is_private:
        await event.reply(
            f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
            \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
            \n✨ Ayarlamak istediğinizi aşağıdan seçin:**",
            buttons=options,
            link_preview=False,
        )


@doge.shiba_cmd(pattern=f"^/(broadcast|yay[ıi]n)({gvar('BOT_USERNAME')})?([\s]+)?$")
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**ℹ️ Yayın yapmak istediğiniz mesajı yanıtlayın!**")

    start_ = datetime.now()
    br_cast = await replied.reply("**🔊 Yayın Yapılıyor...**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply(
            f"**ℹ️ Henüz kimse {gvar('BOT_USERNAME')} botunu başlatmamış!**"
        )

    users = get_all_starters()
    if users is None:
        return await event.reply(
            f"**ℹ️ Henüz kimse {gvar('BOT_USERNAME')} botunu başlatmamış!**"
        )

    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "**🔊 Yeni bir yayın aldın.**"
            )
            await event.client.send_message(int(user.user_id), replied)
            await sleep(0.8)
        except FloodWaitError as e:
            await sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**🚨 Hᴀᴛᴀ:**\n__ℹ️ Yayın Yaparken bir hata oluştu.__\n➡️ `{e}`",
                )
        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        f"**🔊 Yayın Yapılıyor...**\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• **✅ Başarılı:** `{count}`\n"
                        + f"• **❌ Hatalı** `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await sleep(e.seconds)
    end_ = datetime.now()
    b_info = "🔊 ➡️ <b> {} tane kullanıcı </b> için mesajı başarıyla yayınladı.".format(
        count
    )
    if len(blocked_users) != 0:
        b_info += f"\n🚫 <b>{len(blocked_users)} tane kullanıcı</b> {gvar('BOT_USERNAME')} botunu engellemiş ya da botla olan mesajları silmiş. Bu yüzden bot kullanıcıları listesinden silindi."
    b_info += "⏱ Tamamlanma Süresi:<code> {}</code>.".format(
        time_formatter((end_ - start_).seconds)
    )
    await br_cast.edit(b_info, parse_mode="html")


@doge.bot_cmd(
    pattern=f"^/(botusers|kullan[ıi]c[ıi]lar)({gvar('BOT_USERNAME')})?([\s]+)?$",
    command=("botusers", plugin_category),
    info={
        "h": "Botu başlatan kullanıcıların listesini almak için.",
        "d": "Botunu başlatan kullanıcıların tam listesini almak için kullanılır.",
        "u": ["{tr}botusers", "{tr}kullanıcılar"],
    },
)
async def ban_starters(event):
    "Botu başlatan kullanıcıların listesini almak için."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edl(
            event, "**ℹ️ {} botunu henüz kimse başlattı.**".format(gvar("BOT_USERNAME"))
        )

    msg = f"**🐾 {gvar('BOT_USERNAME')} botunu başlatan kullanıcıların listesi:\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.user_id)}\
                \n   **🆔 Kullanıcı ID'si:** `{user.user_id}`\
                \n   **ℹ️ Kullanıcı Adı:** @{user.username}\
                \n   **📅 Tarih:** __{user.date}__\n\n"
    await eor(event, msg)


@doge.shiba_cmd(
    pattern="^/(ban|yasakla)({gvar('BOT_USERNAME')})?([\s]+)?\\s+([\\s\\S]*)"
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id,
            "Üzgünüm! Bu kullanıcıyı veritabanımda bulamadım",
            reply_to=reply_to,
        )

    if not reason:
        return await event.client.send_message(
            event.chat_id,
            "**🚨 Kullanıcıyı yasaklamak için önce sebep verin!**",
            reply_to=reply_to,
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**🚨 Hᴀᴛᴀ:**\n➡️ `{e}`")

    if user_id == int(gvar("OWNER_ID")):
        return await event.reply("**🚨 Seni yasaklayamam.**")

    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #ZATEN_BANLI\
            \n➡️ Kullanıcı zaten yasaklı kullanıcılar listemde var.\
            \n**📅 Tarih:** `{check.date}`\
            \n**⛓ Sebep** `{check.reason}`",
        )

    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.shiba_cmd(
    pattern="^/(unban|yasakac)({gvar('BOT_USERNAME')})?([\s]+)?(?:\\s|$)([\\s\\S]*)"
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**🚨 Kullanıcıyı bulamadım.", reply_to=reply_to
        )

    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**🚨 Hᴀᴛᴀ:**\n➡️ `{e}`")

    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"🛑 #KULLANICI_YASAKLI_DEGİL\
            \n👤 {_format.mentionuser(user.first_name, user.id)} yasaklanan kullanıcılar listemde yok.",
        )

    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@doge.bot_cmd(
    pattern="(botbans|yasakl[iı]lar)$",
    command=("botbans", plugin_category),
    info={
        "h": "Bottan yasaklanan kullanıcılar listesini almak için.",
        "d": "Bottan yasaklanan kullanıcıların listesini almak için.",
        "u": "{tr}botbans",
    },
)
async def ban_starters(event):
    "Bottan yasaklanan kullanıcılar listesini almak için."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edl(
            event, f"**ℹ️ {gvar('BOT_USERNAME') } botunda henüz kimse yasaklanmadı.**"
        )

    msg = (
        f"**🐾 {gvar('BOT_USERNAME') } botunda yasaklanan kullanıcıların listesi:\n\n**"
    )
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name, user.chat_id)}\
                \n   **🆔 Kullanıcı ID'si:** `{user.chat_id}`\
                \n   **ℹ️ UKullnıcı Adı:** @{user.username}\
                \n   **📅 Tarih:** __{user.date}__\
                \n   **⛓ Sebep:** __{user.reason}__\n\n"
    await eor(event, msg)


@doge.bot_cmd(
    pattern="botantif (on|off)$",
    command=("botantif", plugin_category),
    info={
        "h": "Bot antiflood özelliğini etkinleştirmek veya devre dışı bırakmak için.",
        "d": "Açıksa, üst üste gönderilen ya da üst üst düzenlenen 10 mesajdan sonra otomatk olarak yasaklar.",
        "u": [
            "{tr}botantif on",
            "{tr}botantif off",
        ],
    },
)
async def ban_antiflood(event):
    "Bot antiflood özelliğini etkinleştirmek veya devre dışı bırakmak için."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvar("bot_antif") is not None:
            return await edl(event, "**ℹ️ Bot Antiflood zaten etkindi.**")

        sgvar("bot_antif", True)
        await edl(event, "**ℹ️ Bot Antiflood Etkin.**")
    elif input_str == "off":
        if gvar("bot_antif") is None:
            return await edl(event, "**ℹ️ Bot Antiflood zaten devre dışı.**")

        dgvar("bot_antif")
        await edl(event, "**ℹ️ Bot antiflolood devre dışı.**")
