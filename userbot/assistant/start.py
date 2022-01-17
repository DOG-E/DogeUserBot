from telethon import Button
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from userbot.assistant.botpm import check_bot_started_users

from ..sql_helper.bot_blacklists import check_is_black_list
from . import BOTLOG, BOTLOG_CHATID, Config, doge, gvar, reply_id


@doge.shiba_cmd(
    pattern=f"/start ?(.*))",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start(event):
    args = event.pattern_match.group(1)
    chat = await event.get_chat()
    user = await doge.get_me()
    if check_is_black_list(chat.id):
        return
    reply_to = await reply_id(event)
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{user.first_name}](tg://user?id={user.id})"
    first = chat.first_name
    last = chat.last_name if chat.last_name else ""
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = user.first_name
    my_last = user.last_name if user.last_name else ""
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{user.username}" if user.username else my_mention
    customstrmsg = gvar("START_TEXT") or None
    help_text = f"""🐶 **Botun Komutları:**

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
    # TODO await check_bot_started_users(chat, event)
    if (
        event.sender_id != int(gvar("OWNER_ID"))
        or event.sender_id not in Config.SUDO_USERS
    ):
        if customstrmsg is not None:
            start_msg = customstrmsg.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            )
        else:
            start_msg = str(
                "**🐶 Hey!**\
            \n🐾 Selam {}!\n\
            \n**🐶 Ben {}'in sadık köpeğiyim.**\
            \n💭 Ustamla buradan iletişime geçebilirsiniz.".format(
                    mention, my_mention
                )
            )
            if gvar("START_BUTTON"):
                sbutton = gvar("START_BUTTON")
                SBNAME = sbutton.split(";")[0]
                SBLINK = sbutton.split(";")[1]
                buttons = [(Button.url(SBNAME, url=SBLINK))]
            else:
                buttons = [
                    (Button.url("📣 Kᴀɴᴀʟ", "https://t.me/DogeUserBot"),),
                    (
                        Button.url("💬 Sᴜᴘᴘᴏʀᴛ", "https://t.me/DogeSup"),
                        Button.url("🧩 Pʟᴜɢɪɴ", "https://t.me/DogePlugin"),
                    ),
                ]
                if gvar("START_PIC") != "False":
                    START_PIC = (
                        gvar("START_PIC")
                        or "https://telegra.ph/file/e854a644808aeb1112462.png"
                    )
                elif gvar("START_PIC") == "False":
                    START_PIC = 1
                    try:
                        if START_PIC == 1:
                            await event.client.send_message(
                                chat.id,
                                start_msg,
                                link_preview=False,
                                buttons=buttons,
                                reply_to=reply_to,
                            )
                        else:
                            await event.client.send_file(
                                chat.id,
                                START_PIC,
                                caption=start_msg,
                                link_preview=False,
                                buttons=buttons,
                                reply_to=reply_to,
                            )
                    except (
                        WebpageMediaEmptyError,
                        MediaEmptyError,
                        WebpageCurlFailedError,
                    ) as e:
                        await event.client.send_file(
                            chat.id,
                            "https://telegra.ph/file/e854a644808aeb1112462.png",
                            caption=start_msg,
                            link_preview=False,
                            buttons=buttons,
                            reply_to=reply_to,
                        )
                        if BOTLOG:
                            await event.client.send_message(
                                BOTLOG,
                                f"**🚨 Hᴀᴛᴀ:** Kullanıcı botunuzu başlatırken ayarladığınız görsel gönderilemediği için varsayılan [görsel](https://telegra.ph/file/e854a644808aeb1112462.png) gönderildi! Lütfen en kısa sürede kontrol edip düzeltiniz.\
                                \n\n➡️ Hata Geri Bildirimi: `{e}`",
                            )
                    except Exception as e:
                        if BOTLOG:
                            await doge.bot.send_message(
                                BOTLOG_CHATID,
                                f"**🚨 Hᴀᴛᴀ:**\n`ℹ️ Kullanıcı botunuzu başlatırken bir hata oluştu.`\
                                \n➡️ `{e}`",
                            )
    elif (
        event.sender_id == int(gvar("OWNER_ID")) or event.sender_id in Config.SUDO_USERS
    ):
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
        ownerb = [
            (Button.inline("✨ Aʏᴀʀʟᴀʀ", data="setmenu"),),
            (Button.inline("🐕‍🦺 ʏᴀʀᴅɪᴍ", data="mainmenu"),),
        ]
        owner = "**🐶 Hey!\
    \n🐾 Merhaba {}!\n\
    \n💬 Sana nasıl yardımcı olabilirim?**".format(
            my_mention
        )
        if args == "settings":
            await event.client.send_file(
                chat.id,
                "https://telegra.ph/file/e854a644808aeb1112462.png",
                caption=f"**🐶 [Doɢᴇ UsᴇʀBoᴛ](https://t.me/DogeUserBot)\
                \n🐾 Yᴀʀᴅɪᴍᴄɪ\n\
                \n✨ Ayarlamak istediğinizi aşağıdan seçin:**",
                buttons=options,
                link_preview=False,
                reply_to=reply_to,
            )
        elif args == "help":
            await event.reply(help_text)
        else:
            await event.client.send_message(
                chat.id,
                owner,
                link_preview=False,
                buttons=ownerb,
                reply_to=reply_to,
            )
    else:
        await check_bot_started_users(chat, event)
