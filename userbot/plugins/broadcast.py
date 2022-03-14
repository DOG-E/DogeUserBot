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

from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from ..sql_helper.broadcast_sql import (
    add_to_broadcastlist,
    del_keyword_broadcastlist,
    get_broadcastlist_chats,
    get_chat_broadcastlist,
    is_in_broadcastlist,
    num_broadcastlist_chat,
    num_broadcastlist_chats,
    rm_from_broadcastlist,
)
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    _format,
    doge,
    edl,
    eor,
    get_user_from_event,
    logging,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


@doge.bot_cmd(
    pattern="msgto(?:\s|$)([\s\S]*)",
    command=("msgto", plugin_category),
    info={
        "h": "Kişiye veya sohbete mesaj göndermek için.",
        "d": "Belirli bir sohbetten, istediğiniz kişiye/gruba mesaj göndermek istiyorsanız, bu komut ile birlikte kullanıcı adı/kullanıcı kimliği(id)/sohbet kimliği(id) kullanın.",
        "u": [
            "{tr}msgto Metni yanıtla ve bir <kullanıcı adı / İD> ver ",
            "{tr}msgto <kullanıcı adı / İD> <metin>",
        ],
        "e": "{tr}msgto @SohbetDoge Naber?",
    },
)
async def dogebroadcast_add(event):
    "Kişiye veya sohbete mesaj atmak için."
    user, reason = await get_user_from_event(event)
    reply = await event.get_reply_message()
    if not user:
        return
    if not reason and not reply:
        return await edl(
            event, "__Kişiye ne göndermeliyim? Metne cevap ver veya bir metin ver__"
        )
    if reply and reason and user.id != reply.sender_id:
        if BOTLOG:
            msg = await doge.bot.send_message(BOTLOG_CHATID, reason)
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "Yanıtlanan ileti kullanıcıya gönderilemedi.",
                reply_to=msg.id,
            )
        msglink = await event.client.get_msg_link(msg)
        return await eor(
            event,
            f"__Sorry! Confusion between users to whom should I send the person mentioned in message or to the person replied. text message was logged in [log group]({msglink}). you can resend message from there__",
        )
    if reason:
        msg = await event.client.send_message(user.id, reason)
    else:
        msg = await event.client.send_message(user.id, reply)
    await edl(event, "__Mesaj başarıyla gönderildi.__")


@doge.bot_cmd(
    pattern="addto(?:\s|$)([\s\S]*)",
    command=("addto", plugin_category),
    info={
        "h": "Belirli sohbeti belirtilen kategoriye ekleyecektir.",
        "u": "{tr}addto <Kategori adı>",
        "e": "{tr}addto test.",
    },
)
async def dogebroadcast_add(event):
    "Herhangi sohbeti bir kategoriye ekleyin"
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Bu sohbeti hangi kategoriye eklemeliyim?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    check = is_in_broadcastlist(keyword, event.chat_id)
    if check:
        return await edl(
            event,
            f"Bu sohbet zaten {keyword} kategorisinde var.",
            parse_mode=_format.parse_pre,
        )
    add_to_broadcastlist(keyword, event.chat_id)
    await edl(
        event,
        f"Sohbet başarıyla {keyword} kategorisine eklendi.",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"Sohbet {chat.title}, {keyword} kategorisine eklendi.",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"{chat.first_name} kullanıcısı {keyword} kategorisine eklendi",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="list(?:\s|$)([\s\S]*)",
    command=("list", plugin_category),
    info={
        "h": "Verilen kategorideki tüm sohbetler gösterilecek.",
        "u": "{tr}list <kategori adı>",
        "e": "{tr}list test",
    },
)
async def dogebroadcast_list(event):
    "Belirtilen kategorideki tüm sohbetleri listeler."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Hangi kategorideki Sohbetleri listelemeliyim?\n.listall yazarak kontrol edin",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await edl(
            event,
            f"{keyword} adında bir kategori yok. .listall yazarak kontrol edin",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event,
        f"{keyword} kategorisinin bilgileri getiriliyor",
        parse_mode=_format.parse_pre,
    )
    resultlist = f"**'{keyword}' kategorisi '{no_of_chats}' sohbetlerine sahiptir ve bunlar aşağıda listelenmiştir:**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **Kanal** \n  •  **Ad:** {chatinfo.title} \n  •  **İD:** `{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **Grup** \n  •  **Ad:** {chatinfo.title} \n  •  **İD:** `{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **Kullanıcı** \n  •  **Ad:** {chatinfo.first_name} \n  •  **İD:** `{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 __Veritabanındaki bu İD {int(chat)} muhtemelen sohbetten/kanaldan çıkmış olabilir veya geçersiz id olabilir.\
                            \n__ `.frmfrom {keyword} {int(chat)}` komutunu kullanarak bu İD'i veritabanından kaldırın \n\n"
    finaloutput = resultlist + errorlist
    await eor(dogevent, finaloutput)


@doge.bot_cmd(
    pattern="listall$",
    command=("listall", plugin_category),
    info={
        "h": "Tüm kategori adlarının listesini gösterecektir.",
        "u": "{tr}listall",
    },
)
async def dogebroadcast_list(event):
    "Tüm kategori adlarını listelemek için."
    if num_broadcastlist_chats() == 0:
        return await edl(
            event,
            "daha fazla yardım için en az bir kategori kontrol bilgisi oluşturmalısınız.",
            parse_mode=_format.parse_pre,
        )
    chats = get_broadcastlist_chats()
    resultext = "**İşte kategorinizin listesi:**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __{num_broadcastlist_chat(i)} sohbet içeriyor.__\n"
    await eor(event, resultext)


@doge.bot_cmd(
    pattern="sendto(?:\s|$)([\s\S]*)",
    command=("sendto", plugin_category),
    info={
        "h": "Yanıtlanan mesajı verilen kategorideki tüm sohbetlere gönderecek.",
        "u": "{tr}sendto <kategori adı>",
        "e": "{tr}sendto test",
    },
)
async def dogebroadcast_send(event):
    "Mesajı belirtilen kategorideki tüm sohbetlere göndermek için."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Bu mesajı hangi kategoriye göndereyim?",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    dog = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    if not reply:
        return await edl(
            event,
            "Bu kategoriye ne göndermeliyim?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    group_ = Get(dog)
    if no_of_chats == 0:
        return await edl(
            event,
            f"{keyword} adında bir kategori yok. .listall yazarak kontrol edin.",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event,
        "Bu mesajı kategorideki tüm Gruplara gönderiyorum",
        parse_mode=_format.parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.send_message(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
        await sleep(0.5)
    resultext = f"`Mesaj, {keyword} kategorisindeki {no_of_chats} sohbetten {i} sohbete gönderildi.`"
    await edl(dogevent, resultext)
    if BOTLOG:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"{keyword} kategorisindeki {no_of_chats} sohbetten {i} sohbete bir mesaj gönderildi",
            parse_mode=_format.parse_pre,
        )


@doge.bot_cmd(
    pattern="fwdto(?:\s|$)([\s\S]*)",
    command=("fwdto", plugin_category),
    info={
        "h": "Cevaplanan mesajı verilen kategorideki tüm sohbetlere iletecek",
        "u": "{tr}fwdto <kategori adı>",
        "e": "{tr}fwdto test",
    },
)
async def dogebroadcast_send(event):
    "Mesajı belirtilen kategorideki tüm sohbetlere iletmek için."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Bu mesajı hangi kategoriye göndereyim?",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    dog = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    if not reply:
        return await edl(
            event,
            "Bu kategoriye ne göndermeliyim?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    group_ = Get(dog)
    if no_of_chats == 0:
        return await edl(
            event,
            f"{keyword} adında bir kategori yok. .listall yazarak kontrol edin.",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event,
        "Bu mesajı kategorideki tüm Gruplara gönderiyorum",
        parse_mode=_format.parse_pre,
    )
    try:
        await event.client(group_)
    except BaseException:
        pass
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.forward_messages(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
        await sleep(0.5)
    resultext = f"`Mesaj, {keyword} kategorisindeki {no_of_chats} sohbetten {i} sohbete gönderildi.`"
    await edl(dogevent, resultext)
    if BOTLOG:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"{keyword} kategorisindeki {no_of_chats} sohbetten {i} sohbete bir mesaj iletildi",
            parse_mode=_format.parse_pre,
        )


@doge.bot_cmd(
    pattern="rmfrom(?:\s|$)([\s\S]*)",
    command=("rmfrom", plugin_category),
    info={
        "h": "Belirli sohbeti belirtilen kategoriden kaldıracak",
        "u": "{tr}rmfrom <kategori adı>",
        "e": "{tr}rmfrom test",
    },
)
async def dogebroadcast_remove(event):
    "Sohbeti belirtilen kategoriden kaldırmak için"
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Bu sohbeti hangi kategoriden kaldırmalıyım?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    check = is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await edl(
            event,
            f"Bu sohbet {keyword} kategorisinde değil.",
            parse_mode=_format.parse_pre,
        )
    rm_from_broadcastlist(keyword, event.chat_id)
    await edl(
        event,
        f"Bu sohbet artık {keyword} kategorisinde değil",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"Sohbet {chat.title}, {keyword} kategorisinden kaldırıldı",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"{chat.first_name} kullanıcısı {keyword} kategorisinden kaldırıldı",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="frmfrom(?:\s|$)([\s\S]*)",
    command=("frmfrom", plugin_category),
    info={
        "h": " Verilen sohbeti bir kategoriden kaldırmaya zorlamak için.",
        "d": "Suppose if you're muted or group/channel is deleted you can't send message there so you can use this cmd to the chat from that category",
        "u": "{tr}frmfrom <kategori adı> <İD>",
        "e": "{tr}frmfrom test -100123456",
    },
)
async def dogebroadcast_remove(event):
    "Verilen sohbeti bir kategoriden kaldırmaya zorlamak için."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Bu sohbeti hangi kategoriden kaldırmalıyım?",
            parse_mode=_format.parse_pre,
        )
    args = doginput_str.split(" ")
    if len(args) != 2:
        return await edl(
            event,
            ".frmfrom kategori_adı GrupİD'de gösterildiği gibi uygun sözdizimini kullanın",
            parse_mode=_format.parse_pre,
        )
    try:
        groupid = int(args[0])
        keyword = args[1].lower()
    except ValueError:
        try:
            groupid = int(args[1])
            keyword = args[0].lower()
        except ValueError:
            return await edl(
                event,
                ".frmfrom kategori_adı GrupİD'de gösterildiği gibi uygun sözdizimini kullanın",
                parse_mode=_format.parse_pre,
            )
    keyword = keyword.lower()
    check = is_in_broadcastlist(keyword, int(groupid))
    if not check:
        return await edl(
            event,
            f"Bu sohbet {keyword} kategorisinde değil",
            parse_mode=_format.parse_pre,
        )
    rm_from_broadcastlist(keyword, groupid)
    await edl(
        event,
        f"Bu sohbet artık {keyword} kategorisinde değil",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"{chat.title} {keyword} kategorisinden kaldırıldı",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"{chat.first_name} kullanıcısı {keyword} kategorisinden kaldırıldı",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="delc(?:\s|$)([\s\S]*)",
    command=("delc", plugin_category),
    info={
        "h": "Kategoriyi veritabanından tamamen silmek için",
        "u": "{tr}delc <kategori adı>",
        "e": "{tr}delc test",
    },
)
async def dogebroadcast_delete(event):
    "To delete a category completely."
    doginput_str = event.pattern_match.group(1)
    check1 = num_broadcastlist_chat(doginput_str)
    if check1 < 1:
        return await edl(
            event,
            f"{doginput_str} kategorisi olduğundan emin misiniz?",
            parse_mode=_format.parse_pre,
        )
    try:
        del_keyword_broadcastlist(doginput_str)
        await eor(
            event,
            f"{doginput_str} kategorisi başarıyla silindi",
            parse_mode=_format.parse_pre,
        )
    except Exception as e:
        await edl(
            event,
            str(e),
            parse_mode=_format.parse_pre,
        )
