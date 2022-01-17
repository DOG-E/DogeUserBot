# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from re import IGNORECASE, escape, search

from telethon.utils import get_display_name

from ..sql_helper import blacklist_sql as sql
from ..utils import is_admin
from . import BOTLOG_CHATID, doge, eor

plugin_category = "admin"


@doge.bot_cmd(incoming=True, groups_only=True)
async def on_new_message(event):
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    dogadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not dogadmin:
        return
    for snip in snips:
        pattern = r"( |^|[^\w])" + escape(snip) + r"( |$|[^\w])"
        if search(pattern, name, flags=IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    f"{get_display_name(await event.get_chat())} sohbetinde silme iznim yok.\
                    \nYani bu sohbette karalistedeki kelimeleri içeren mesajları silemem.",
                )
                for word in snips:
                    sql.rm_from_blacklist(event.chat_id, word.lower())
            break


@doge.bot_cmd(
    pattern="addblacklist ((.|\n)*)",
    command=("addblacklist", plugin_category),
    info={
        "h": "Karalisteye kelime ekler.",
        "d": "Verilen kelime veya kelimeler, komutu kullandığınız sohbette karalisteye eklenecek, herhangi bir kullanıcı karalistedeki kelimeyle mesaj gönderirse mesaj silinecek.",
        "note": "Aynı anda birden fazla kelime eklemek istiyorsanız, Bu şekilde [merhaba merhaba] değil, yeni bir satırda verilmelidir. [merhaba\nmerhaba] gibi olmalıdır.",
        "u": "{tr}addblacklist <kelime(ler)>",
        "e": ["{tr}addblacklist aq", "{tr}addblacklist aq (enter) amk"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "Karalisteye kelime ekler."
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await eor(
        event,
        "Bu sohbetteki karalisteye {} eklendi.".format(len(to_blacklist)),
    )


@doge.bot_cmd(
    pattern="rmblacklist ((.|\n)*)",
    command=("rmblacklist", plugin_category),
    info={
        "h": "Karalistedeki kelimeleri kaldırır.",
        "d": "Verilen kelime veya kelimeler, komutu kullandığınız sohbette karalisteden kaldırılacaktır.",
        "note": "Aynı anda birden fazla kelime eklemek istiyorsanız, Bu şekildee [merhaba merhaba] değil, yeni bir satırda verilmelidir. [merhaba\nmerhaba] gibi olmalıdır.",
        "u": "{tr}rmblacklist <kelime(ler)>",
        "e": ["{tr}rmblacklist aq", "{tr}rmblacklist aq (enter) amk"],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "Karalistedeki kelimeleri kaldırır."
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(sql.rm_from_blacklist(event.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    await eor(
        event,
        f"Karalistedeki {len(to_unblacklist)} kelimelerinden {successful} kaldırıldı.",
    )


@doge.bot_cmd(
    pattern="listblacklist$",
    command=("listblacklist", plugin_category),
    info={
        "h": "Karalistedeki kelimeleri listeler.",
        "d": "Sohbette karalistedeki kelimelerin listesini gösterir.",
        "u": "{tr}listblacklist",
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "Karalistedeki kelimeleri listeler."
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "Mevcut Sohbetteki Kara Listeler:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "KaraListe bulunamadı. `.addblacklist` komutu ile  karalisteye kelime eklemeye başlayın."
    await eor(event, OUT_STR)
