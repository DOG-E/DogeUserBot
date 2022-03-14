# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime

from telethon.utils import get_display_name

from ..core.data import blacklist_chats_list
from ..sql_helper.global_collectionjson import (
    add_collection,
    del_collection,
    get_collection,
)
from . import dgvar, doge, edl, eor, gvar, logging, sgvar

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


@doge.bot_cmd(
    pattern="chatblacklist (on|off)$",
    command=("chatblacklist", plugin_category),
    info={
        "h": "Sohbet karalistesini etkinleştirir veya devre dışı bırakır.",
        "d": "Bunu açarsanız, Doge addblackchat komutu ile veritabanında saklanan sohbetler üzerinde çalışmayacaktır. Bunu kapatırsanız, veritabanına sohbet eklemiş olsanız bile Doge o sohbette çalışmayı bırakmaz.",
        "u": "{tr}chatblacklist <on/off>",
    },
)
async def chat_blacklist(event):
    "Sohbet kara listesini etkinleştirin veya devre dışı bırakır."
    input_str = event.pattern_match.group(1)
    blkchats = blacklist_chats_list()
    if input_str == "on":
        if gvar("blacklist_chats") is not None:
            return await edl(event, "__Zaten açık.__")
        sgvar("blacklist_chats", "true")
        text = "__Şu andan itibaren, Doge veritabanında saklanan sohbetlerde çalışmıyor.__"
        if len(blkchats) != 0:
            text += "**Bot, değişiklikleri uygulamak için yeniden başlıyor. Lütfen biraz bekleyin...**"
            msg = await eor(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**Kara listeye herhangi bir sohbet eklemediniz.**"
        return await eor(
            event,
            text,
        )
    if gvar("blacklist_chats") is not None:
        dgvar("blacklist_chats")
        text = "__Doge bir kuş kadar özgür. Her sohbette çalışır.__"
        if len(blkchats) != 0:
            text += "**Bot, değişiklikleri uygulamak için yeniden başlıyor. Lütfen biraz bekleyin...**"
            msg = await eor(
                event,
                text,
            )
            return await event.client.reload(msg)
        text += "**Kara listeye herhangi bir sohbet eklemediniz.**"
        return await eor(
            event,
            text,
        )
    await edl(event, "Sohbet karalistesi zaten kapalıymış.")


@doge.bot_cmd(
    pattern="addblkchat(s)?(?:\s|$)([\s\S]*)",
    command=("addblkchat", plugin_category),
    info={
        "h": "Karalisteye sohbet ekler.",
        "d": "Karalisteye eklediğiniz sohbetlerde Doge çalışmayacaktır. Sohbet ID'lerini girdi olarak verin veya eklemek istediğiniz sohbette bu komutu kullanın.",
        "u": [
            "{tr}addblkchat <sohbet ID>",
            "{tr}addblkchat eklemek istediğin sohbette kullan",
        ],
    },
)
async def add_blacklist_chat(event):
    "Karalisteye sohbet ekler."
    input_str = event.pattern_match.group(2)
    errors = ""
    result = ""
    blkchats = blacklist_chats_list()
    try:
        blacklistchats = get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if input_str:
        input_str = input_str.split(" ")
        for chatid in input_str:
            try:
                chatid = int(chatid.strip())
                if chatid in blkchats:
                    errors += f"{chatid} ID'sine sahip olan grup zaten karalistede."
                    continue
                chat = await event.client.get_entity(chatid)
                date = str(datetime.now().strftime("%B %d, %Y"))
                chatdata = {
                    "chat_id": chat.id,
                    "chat_name": get_display_name(chat),
                    "chat_username": chat.username,
                    "date": date,
                }
                blacklistchats[str(chat.id)] = chatdata
                result += (
                    f"{get_display_name ( chat)} sohbeti karalisteye başarıyla eklendi."
                )
            except Exception as e:
                errors += (
                    f"**{chatid} karalisteye eklenirken hata meydana geldi.** \n__{e}__"
                )
    else:
        chat = await event.get_chat()
        try:
            chatid = chat.id
            if chatid in blkchats:
                errors += f"{chatid} ID'sine sahip olan grup zaten kara listede"
            else:
                date = str(datetime.now().strftime("%B %d, %Y"))
                chatdata = {
                    "chat_id": chat.id,
                    "chat_name": get_display_name(chat),
                    "chat_username": chat.username,
                    "date": date,
                }
                blacklistchats[str(chat.id)] = chatdata
                result += (
                    f"{get_display_name ( chat)} sohbeti karalisteye başarıyla eklendi."
                )
        except Exception as e:
            errors += (
                f"**{chatid} karalisteye eklenirken hata meydana geldi.** \n__{e}__"
            )
    del_collection("blacklist_chats_list")
    add_collection("blacklist_chats_list", blacklistchats, {})
    output = ""
    if result != "":
        output += f"**Başarılı:**\n{result}\n"
    if errors != "":
        output += f"**Hata:**\n{errors}\n"
    if result != "":
        output += "**Bot, değişiklikleri uygulamak için yeniden yükleniyor... Lütfen biraz bekleyin...**"
    msg = await eor(event, output)
    await event.client.reload(msg)


@doge.bot_cmd(
    pattern="rmblkchat(s)?(?:\s|$)([\s\S]*)",
    command=("rmblkchat", plugin_category),
    info={
        "h": "Karalistenizdeki sohbetleri karalisteden kaldırır.",
        "d": "Doge karalistenizden kaldırdığınız sohbetlerde de çalışacaktır. Sohbet ID'lerini girdi olarak verin veya çıkarmak istediğiniz sohbette bu komutu kullanın.",
        "u": [
            "{tr}rmblkchat <sohbet ID>",
            "{tr}rmblkchat çıkarmak istediğiniz sohbet",
        ],
    },
)
async def add_blacklist_chat(event):
    "Karalistenizdeki sohbetleri karalisteden kaldırır."
    input_str = event.pattern_match.group(2)
    errors = ""
    result = ""
    blkchats = blacklist_chats_list()
    try:
        blacklistchats = get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if input_str:
        input_str = input_str.split(" ")
        for chatid in input_str:
            try:
                chatid = int(chatid.strip())
                if chatid in blkchats:
                    chatname = blacklistchats[str(chatid)]["chat_name"]
                    del blacklistchats[str(chatid)]
                    result += f"{chatname} karalisteye alınmış sohbetlerden başarıyla kaldırıldı!"
                else:
                    errors += f"Verilen {chatid} kimliği veritabanınızda mevcut değil. Yani karalisteye alınmamış."
            except Exception as e:
                errors += f"**{chatid} kaldırılırken bir hata oluştu** \nHata: `{e}`\n"
    else:
        chat = await event.get_chat()
        try:
            chatid = chat.id
            if chatid in blkchats:
                chatname = blacklistchats[str(chatid)]["chat_name"]
                del blacklistchats[str(chatid)]
                result += (
                    f"{chatname} karalisteye alınmış sohbetlerden başarıyla kaldırıldı."
                )
            else:
                errors += f"Verilen {chatid} kimliği veritabanınızda mevcut değil. Yani karalisteye alınmamış."
        except Exception as e:
            errors += f"**{chatid} kaldırılırken bir hata oluştu\nHata:** `{e}`\n"
    del_collection("blacklist_chats_list")
    add_collection("blacklist_chats_list", blacklistchats, {})
    output = ""
    if result != "":
        output += f"**Başarılı:**\n{result}\n"
    if errors != "":
        output += f"**Hata:**\n{errors}\n"
    if result != "":
        output += "**Bot, değişiklikleri uygulamak için yeniden yükleniyor... Lütfen biraz bekleyin...**"
    msg = await eor(event, output)
    await event.client.reload(msg)


@doge.bot_cmd(
    pattern="listbl(ac)kchats$",
    command=("listblkchats", plugin_category),
    info={
        "h": "Karalisteye alınan tüm sohbetleri listeler.",
        "d": "Karalisteye alınmış tüm sohbetleri listesini gösterir.",
        "u": [
            "{tr}listblkchat",
        ],
    },
)
async def add_blacklist_chat(event):
    "Karalisteye alınan tüm sohbetleri listeler."
    blkchats = blacklist_chats_list()
    try:
        blacklistchats = get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if len(blkchats) == 0:
        return await edl(event, "__Botunuzda karalisteye alınmış sohbet yok.__")
    result = "**Karalisteye alınan sohbetlerin listesi:**\n\n"
    for chat in blkchats:
        result += f"☞ {blacklistchats[str(chat)]['chat_name']}\n"
        result += f"**Sohbet ID:** `{chat}`\n"
        username = blacklistchats[str(chat)]["chat_username"] or "__Gizli grup__"
        result += f"**Kullanıcı Adı:** {username}\n"
        result += f"**Eklendiği Zaman:** {blacklistchats[str(chat)]['date']}\n\n"
    await eor(event, result)
