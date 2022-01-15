# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from ..sql_helper import antiflood_sql as sql
from ..utils import is_admin
from . import doge, eor

plugin_category = "admin"

CHAT_FLOOD = sql.__load_flood_settings()
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@doge.bot_cmd(incoming=True, groups_only=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    dogadmin = await is_admin(event.client, event.chat_id, event.client.uid)
    if not dogadmin:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"**Otomatik AntiFlooder**\
                \n@admin [Kullanıcı](tg://user?id={event.message.sender_id}) bu sohbette flood yapıyor.\
                \n`{e}`",
            reply_to=event.message.id,
        )
        await sleep(4)
        await no_admin_privilege_message.edit(
            "Bu garip bir Spam dostum. Bunu durdur ve sohbetin tadını çıkar."
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"""**Otomatik AntiFlooder**
[Kullanıcı](tg://user?id={event.message.sender_id}) tanımlanan flood sınırına ulaştığı için otomatik olarak kısıtlandı.""",
            reply_to=event.message.id,
        )


@doge.bot_cmd(
    pattern="setflood(?:\s|$)([\s\S]*)",
    command=("setflood", plugin_category),
    info={
        "h": "Bir grupta antiflood kurun",
        "d": "Kullanıcıyı sohbete spam gönderirse uyarır ve uygun haklara sahip bir yöneticiyseniz, o grupta onu sessize alır.",
        "note": "Flood baskınını durdurmak için 999999 gibi yüksek bir değer girebilirsiniz.",
        "u": "{tr}setflood <sayı>",
        "e": [
            "{tr}setflood 10",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "İstenmeyen postaları önlemek için bir grupta antiflood kurun"
    input_str = event.pattern_match.group(1)
    event = await eor(event, "`Flood ayarları güncelleniyor!`")
    await sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(f"Antiflood mevcut sohbette {input_str} olarak ayarlandı.")
    except Exception as e:
        await event.edit(str(e))
