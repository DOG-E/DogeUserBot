# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name
from userbot.helpers.utils.utils import run_async

from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    _format,
    doge,
    edl,
    eor,
    get_user_from_event,
    logging,
    media_type,
    tr,
    wowmydev,
)

# =================== STRINGS ============
plugin_category = "admin"
LOGS = logging.getLogger(__name__)

PP_TOO_SMOL = "`Bu görüntü işlemek için çok küçük`"
PP_ERROR = "`Görüntüyü işlerken bir hata meydana geldi.`"
NO_PERM = "`Bunu yapabilmek için yeterli iznim yok! Bu çok üzücü (ಥ﹏ಥ)`"
CHAT_PP_CHANGED = "`Sohbet resmi değiştirildi.`"
INVALID_MEDIA = "`Geçersiz uzantı`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@doge.bot_cmd(
    pattern="(d|)gpic$",
    command=("gpic", plugin_category),
    info={
        "h": "Grup profil fotoğrafını değiştirir veya siler.",
        "d": "Bir resmi yanıtlarak kullanırsanız o resmi grup fotoğrafı yapar.",
        "f": {
            "d": "Grup fotoğrafını siler.",
        },
        "u": [
            "{tr}gpic <bir fotoğraf yanıtlayarak>",
            "{tr}dgpic",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "DP grubunu değiştirmek için"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "d":
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edl(event, f"**Hata:** `{e}`")
        process = "silindi."
        await edl(event, "```Grup profil resmi başarıyla silindi.```")
    else:
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edl(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edl(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edl(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edl(event, PP_ERROR)
            except Exception as e:
                return await edl(event, f"**Hata:** `{str(e)}`")
            process = "değiştirildi."
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GRUP_RESIM_DEGISIKLIGI\n"
            f"Grup profili resmi başarıyla {process}"
            f"**Grup**: {get_display_name(await event.get_chat())}\
            \n**Grup ID'si:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", plugin_category),
    info={
        "h": "Bir kişi için yönetici hakları verir.",
        "d": "Sohbetteki bir üyeye yönetici hakları sağlar.",
        "u": [
            "{tr}promote <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}promote <ID/kullanıcı adı/yanıtlayarak> <isteğe bağlı başlık>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır"
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "Sohbette bir kişiyi tanıtmak"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Yönetici"
    if not user:
        return
    dogevent = await eor(event, "`Promoting...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    await dogevent.edit("**Kullanıcı başarıyla yetkilendirildi!**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#YETKILENDIRME\
            \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
            \n**Grup:** {get_display_name(await event.get_chat())}\
            \n**Grup ID'si:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", plugin_category),
    info={
        "h": "Bir kişiyi yönetici listesinden çıkarır.",
        "d": "Bu kişinin bu sohbet içindeki tüm yönetici haklarını kaldırır.",
        "u": [
            "{tr}demote <ID/kullanıcı adı/yanıtlayarak>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız var ve ayrıca o üyenin yönetici yetkilerini düzenleyebiliyor olmanız gerekmektedir."
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "Gruptaki bir kişiyi engellemek için"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "`Yetki düşürülüyor...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    await dogevent.edit("**Yetkisi başarıyla düşürüldü!**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#YETKİSİZLENDİRME\
            \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
            \n**Grup:** {get_display_name(await event.get_chat())}\
            \n**Grup ID'si:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", plugin_category),
    info={
        "h": "Kullanılan gruptan seçilen üyeyi yasaklar.",
        "d": "Seçilen üye gruptan kalıcı olarak atılır ve yasağı kaldırılana kadaar geri dönemez.",
        "u": [
            "{tr}ban <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}ban <ID/kullanıcı adı/yanıtlayarak> <sebep>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız vardır."
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "Gruba bir kişiyi yasaklamak"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, "**__Kendini yasaklayamazsın.__**")
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "**Yasaklanıyor!**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user_id, BANNED_RIGHTS))
    except BadRequestError:
        return await dogevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await dogevent.edit(
            "**Mesajları silmeye hakkım yok ama yine de yasaklandı**"
        )
    if reason:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}** yasaklandı!!**\n**Sebep:** `{reason}`"
        )
    else:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}** yasaklandı!!**"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#YASAKLAMA\
                \n**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\
                \n**Grup:** {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`\
                \n**Sebep:** {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#YASAKLAMA\
                \n**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\
                \n**Grup:** {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`",
            )


@doge.bot_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", plugin_category),
    info={
        "h": "Bu komutu kullandığınız gruptaki üyenin yasağı kaldırılır.",
        "d": "Kullanıcı hesabını grubun yasaklı listesinden kaldırır.",
        "u": [
            "{tr}unban <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}unban <ID/kullanıcı adı/yanıtlayarak> <sebep>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız var"
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "Bir kişinin yasağını açmak için"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    dogevent = await eor(event, "`Yasak kaldırılıyor...`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} **yasağı başarıyla kaldırıldı!**`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#YASAK_KALDIRMA\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Grup:** {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`",
            )
    except UserIdInvalidError:
        await dogevent.edit("**Hayatımda böyle kullanıcı görmedim, onun bir mesajını yanıtlarsan tanıyabilirim.**")
    except Exception as e:
        if BOTLOG:
            await dogevent.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
            await event.client.send_message(
                BOTLOG_CHATID, 
                "#YASAK_KALDIRMA_HATASI\n"
                f"**Hata:** {e}"
                )



@doge.bot_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.error(f"🚨 Susturulmuş kullanıcının mesajı silinemedi: {str(e)}")


@doge.bot_cmd(
    pattern="mute(?:\s|$)([\s\S]*)",
    command=("mute", plugin_category),
    info={
        "h": "Bu kullanıcının mesaj göndermesini engeller.",
        "d": "Eğer yönetici değilse, gruptaki iznini değiştirir.\
            ama eğer yönetici ise veya kişisel sohbette denerseniz, mesajları otomatik olarak silinir.",
        "u": [
            "{tr}mute <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}mute <ID/kullanıcı adı/yanıtlayarak> <sebep>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız var."
    },  # sourcery no-metrics
)
async def startmute(event):
    "Bu özel sohbette bir kişiyi susturmak için"
    if event.is_private:
        await event.edit("`Beklenmeyen sorunlar oluşabilir!`")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**Bu kullanıcı zaten susturulmuş!**"
            )
        if event.chat_id == doge.uid:
            return await edl(event, "**Kendini susturamazın!**")
        flag = await wowmydev(replied_user, event)
        if flag:
            return
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
                await event.client.send_message(
                    BOTLOG_CHATID, 
                    "#YASAK_KALDIRMA_HATASI\n"
                    f"**Hata:** {e}"
                    )
        else:
            await event.edit("**Kullanıcı başarıyla susturuldu!**\n｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_SUSTURULMASI\n"
                f"**Kullanıcı:** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(
                event, "**Yönetici hakları olmadan bir kişiyi susturamazsın Niqq.** ಥ﹏ಥ  "
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        user_id = user.id
        if user_id == doge.uid:
            return await eor(event, "**Kendini susturamazsın!**")
        flag = await wowmydev(user_id, event)
        if flag:
            return
        if is_muted(user_id, event.chat_id):
            return await eor(
                event, "`This user is already muted in this chat ~~lmfao sed rip~~`"
            )
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await eor(
                    event,
                    "**Bu kullanıcı zaten susturulmuş!**",
                )
        except AttributeError:
            pass
        except Exception as e:
            if BOTLOG:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
                return await event.client.send_message(
                    BOTLOG_CHATID, 
                    "#PM_SUSTURMA_HATASI\n"
                    f"**Hata:** {e}"
                    )
        try:
            await event.client(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await eor(
                        event,
                        "**Mesaj silme izniniz yoksa bir kişiyi susturamazsınız.** ಥ﹏ಥ",
                    )
            elif "creator" not in vars(chat):
                return await eor(
                    event, "**Yönetici hakları olmadan bir kişiyi susturamazsın.** ಥ﹏ಥ  "
                )
            mute(user_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
                return await event.client.send_message(
                    BOTLOG_CHATID, 
                    "#SUSTURMA_HATASI\n"
                    f"**Hata:** {e}"
                    )
        if reason:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name, user_id)}, {get_display_name(await event.get_chat())}** grubunda susturuldu!**\n"
                f"`Reason:`{reason}",
            )
        else:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user_id)}, {get_display_name(await event.get_chat())}** grubunda susturuldu!**\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SUSTURMA\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\n"
                f"**Grup:** {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`",
            )


@doge.bot_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", plugin_category),
    info={
        "h": "Kullanıcının tekrar mesaj göndermesine izin verir.",
        "d": "Mesaj göndermek için kullanıcı izinlerini değiştirir.",
        "u": [
            "{tr}unmute <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}unmute <ID/kullanıcı adı/yanıtlayarak> <sebep>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız var."
    },
)
async def endmute(event):
    "Bu özel sohbette bir kişiyi susturmak için"
    if event.is_private:
        await event.edit("`Beklenmeyen sorunlar ve hatalar oluşabilir!`")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "**__Bu kullanıcı bu sohbette zaten susturulmadı__**\n（ ^_^）o自自o（^_^ ）"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
                await event.client.send_message(
                    BOTLOG_CHATID, 
                    "#SUSTURMA_KALDIRMA_HATASI\n"
                    f"**Hata:** {e}"
                    )
        else:
            await event.edit(
                "**Susturulma başarılı bir şekilde kaldırıldı.**\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_SUSTURULMA_KALDIRILMASI\n"
                f"**User:** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await eor(
                event,
                "**Bu kullanıcı zaten bu sohbette serbestçe konuşabiliyor.**",
            )
        except Exception as e:
            if BOTLOG:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")
                return await event.client.send_message(
                    BOTLOG_CHATID, 
                    "#SUSTURMA_KALDIRMA_HATASI\n"
                    f"**Hata:** {e}"
                    )
            else:
                await event.edit("__Bir hatayla karşılaşıldı! Hata raporu Log grubunuza gönderildi. Lütfen kontrol ediniz.__")

        await eor(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)}, {get_display_name(await event.get_chat())} **grubunda sesi açıldı!**\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#SUSTURMA_KALDIRMA\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Grup:** {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`",
            )


@doge.bot_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", plugin_category),
    info={
        "h": "Bir kişiyi gruptan atar.",
        "d": "Kullanıcıyı gruptan atar, böylece geri katılabilir.",
        "u": [
            "{tr}kick <ID/kullanıcı adı/yanıtlayarak>",
            "{tr}kick <ID/kullanıcı adı/yanıtlayarak> <sebep>",
        ],
        "note": "Bunun için uygun haklara ihtiyacınız var."
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "Bunu sohbetten bir kullanıcıyı tekmelemek için kullanın"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    flag = await wowmydev(user_id, event)
    if flag:
        return
    dogevent = await eor(event, "`kullanıcı atılıyor...`")
    try:
        await event.client.kick_participant(event.chat_id, user_id)
    except Exception as e:
        return await dogevent.edit(NO_PERM)
    if reason:
        await dogevent.edit(
            f"**Atıldı:** [{user.first_name}](tg://user?id={user_id})**!**\n**Sebep:** `{reason}`"
        )
    else:
        await dogevent.edit(f"**Atıldı:** [{user.first_name}](tg://user?id={user_id})**!**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GRUPTAN_ATMA\n"
            f"USER: [{user.first_name}](tg://user?id={user_id})\n"
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@doge.bot_cmd(
    pattern="pin( s|$)",
    command=("pin", plugin_category),
    info={
        "h": "Sohbette mesajı sabitler.",
        "d": "Sohbette bunu sabitlemek için bir mesaja cevap verin.",
        "o": {"s": "Üyelere bildirim göndererek sabitler."},
        "u": [
            "{tr}pin <mesaj yanıtlyarak>",
            "{tr}pin s <mesaj yanıtlyarak>",
        ],
    },
)
async def pin(event):
    "Sohbette bir mesajı sabitlemek için"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edl(event, "**Sabitleyebilmek için bir mesaja cevap verin.**", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        if BOTLOG:
            await edl(event, "**Beklenmeyen bir hatayla karşılaşıldı! Lütfen BotLog grubunuza atılmış olan hatayı kontrol edin!**")
            return await event.client.send_message(BOTLOG, f"Mesaj sabitlerken bir hatayla karşılaşıldı: `{e}`")
        else:
            await edl(event, f"**Beklenmeyen bir hatayla karşılaşıldı! Hata Raporu:** {e}")
    await edl(event, "**Başarıyla sabitlendi!**", 5)
    if is_silent == True:
        a = "Evet"
    elif is_silent == False:
        a = "Hayır"
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#SABİTLEME\
                \n__Grupta mesaj başarıyla sabitlendi!__\
                \n**Grup:** {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \n**Sesli mi?**: {a}",
        )


@doge.bot_cmd(
    pattern="unpin(all|$)",
    command=("unpin", plugin_category),
    info={
        "h": "Sohbetteki mesajları sabitten çıkarır.",
        "d": "Sohbetteki mesajı sabitten çıkarmak için bir mesaja cevap verin.",
        "o": {"all": "Sohbetteki tüm sabitli mesajları kaldırır."},
        "u": [
            "{tr}unpin <yanıtlayarak>",
            "{tr}unpinall",
        ],
        "note": "Grupta kullanmak istiyorsanız, bunun için uygun haklara ihtiyacınız var."
    },
)
async def pin(event):
    "Gruptaki mesajları çıkarmak için"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edl(
            event,
            f"__Sabitteen kaldırmak istediğiniz mesajı yanıtlayın ya da hepsini kaldırmak için `{tr}unpinall` komutunu kullanın.",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edl(
                event, f"`Mesajları sabitliden çıkarmak için sabitli bir mesaja `{tr}unpinall` ile cevap verin.", 5
            )
    except BadRequestError:
        return await edl(event, NO_PERM, 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, "**Sabitleme başarıyla kaldırıldı!", 5)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#SABITLEME_KALDIRMA\
                \n**__Sabitli mesaj(lar) başarıyla sabitten kaldırıldı!__**\
                \n**Kullanıcı:**: {get_display_name(await event.get_chat())}\
                \n**Grup ID'si:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="undlt( .m)?(?: |$)(\d*)?",
    command=("undlt", plugin_category),
    info={
        "h": "Gruptaki son silinmiş mesajları alır.",
        "d": "Gruptaki son silinmiş mesajları kontrol etmek için, varsayılan olarak 5. gösterecek. 1 ila 15 mesaj alabilirsiniz.",
        "f": {
            "m": "gruptaki silinen son fotoğrafları direkt alabilir."
        },
        "u": [
            "{tr}undlt <sayı>",
            "{tr}undlt .m <sayı>",
        ],
        "e": [
            "{tr}undlt 7",
            "{tr}undlt .m 7 (Bu, 7 mesajın tümünü bu mesaja cevap verecektir).",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "Gruptaki son silinmiş mesajları kontrol etmek için"
    dogevent = await eor(event, "__Son eylemler aranıyor.....__")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**Bu gruptaki silinen son {lim} mesaj(lar):**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **Gönderen:** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **Gönderen:** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await eor(dogevent, deleted_msg)
    else:
        main_msg = await eor(dogevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**Gönderen:** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**Gönderen:** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
