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

plugin_category = "admin"
LOGS = logging.getLogger(__name__)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
    send_polls=None,
    invite_users=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@doge.bot_cmd(
    pattern="(d|)gpic$",
    command=("gpic", plugin_category),
    info={
        "h": "Grup profil fotoğrafını değiştirir veya siler.",
        "d": "Bir resmi yanıtlarak kullanırsanız o görseli grup profil fotoğrafı yapar.",
        "f": {
            "d": "Grup fotoğrafını siler.",
        },
        "u": [
            "{tr}gpic <bir fotoğraf yanıtlayın>",
            "{tr}dgpic",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):
    "Grup profil fotoğrafını değiştirir veya siler."
    flag = (event.pattern_match.group(1)).strip()
    if flag == "d":
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edl(event, f"**Hata:** `{e}`")
        process = "sildim."
        await edl(event, "`Grup profil resmini başarıyla sildim.`")
    else:
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edl(event, "`Geçersiz uzantı.`")
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edl(event, "`Sohbet resmini başarıyla değiştirdim.`")
            except PhotoCropSizeSmallError:
                return await edl(event, "`Bu görsel çok küçük.`")
            except ImageProcessFailedError:
                return await edl(event, "`Görseli uygularken bir hata meydana geldi.`")
            except Exception as e:
                return await edl(event, f"**Hata:** `{str(e)}`")
            process = "değiştirdim."
    if BOTLOG:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            "#GRUP_RESIM_DEGISIKLIGI\n"
            f"Grup profil resmini başarıyla {process}"
            f"**Grup**: {get_display_name(await event.get_chat())}\
            \n**Sohbet ID:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", plugin_category),
    info={
        "h": "Bir kişi için yönetici hakları verir.",
        "d": "Sohbetteki bir üyeye yönetici hakları sağlar.",
        "u": [
            "{tr}promote <ID/kullanıcı adı/yanıt>",
            "{tr}promote <ID/kullanıcı adı/yanıt> <isteğe bağlı başlık>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "Bir kişi için yönetici hakları verir."
    new_rights = ChatAdminRights(
        change_info=False,
        invite_users=True,
        pin_messages=True,
        add_admins=False,
        ban_users=True,
        delete_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Yönetici"
    if not user:
        return
    dogevent = await eor(event, "`Yetkilendiriyorum...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await dogevent.edit("`Bunu yapabilmek için yeterli iznim yok!`")
    await dogevent.edit("**Kullanıcıyı başarıyla yetkilendirdim!**")
    if BOTLOG:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"#YETKILENDIRME\
            \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
            \n**Sohbet:** {get_display_name(await event.get_chat())}\
            \n**Sohbet ID:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", plugin_category),
    info={
        "h": "Bir kişiyi yönetici listesinden çıkarır.",
        "d": "Bu kişinin bu sohbet içindeki tüm yönetici haklarını kaldırır.",
        "u": [
            "{tr}demote <ID/kullanıcı adı/yanıt>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "Bir kişiyi yönetici listesinden çıkarır."
    user, _ = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if await wowmydev(user_id, event):
        return
    dogevent = await eor(event, "`Yetkiyi düşürüyorum...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "Yönetici"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await dogevent.edit("`Bunu yapabilmek için yeterli iznim yok!`")
    await dogevent.edit("**Yetkiyi başarıyla düşürdüm!**")
    if BOTLOG:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"#YETKİSİZLENDİRME\
            \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
            \n**Sohbet:** {get_display_name(await event.get_chat())}\
            \n**Sohbet ID:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", plugin_category),
    info={
        "h": "Gruptaki üyeni yasaklar.",
        "d": "Seçilen üye gruptan kalıcı olarak atılır ve yasağı kaldırılana kadar geri dönemez.",
        "u": [
            "{tr}ban <ID/kullanıcı adı/yanıt>",
            "{tr}ban <ID/kullanıcı adı/yanıt> <isteğe bağlı sebep>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "Gruptaki üyeyi yasaklar."
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, "**__Kendini yasaklayamazsın!__**")
    if await wowmydev(user_id, event):
        return
    dogevent = await eor(event, "**Yasaklıyorum...**")
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id,
                user_id,
                ChatBannedRights(until_date=None, view_messages=True),
            )
        )
    except BadRequestError:
        return await dogevent.edit("`Bunu yapabilmek için yeterli iznim yok!`")
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await dogevent.edit(
            "**Mesajları silmek için hakkım yok ama yine de onu yasakladım.**"
        )
    if reason:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}** yasakladım!**\n**Sebep:** `{reason}`"
        )
    else:
        await dogevent.edit(
            f"{_format.mentionuser(user.first_name ,user_id)}** yasakladım!**"
        )
    if BOTLOG:
        if reason:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"#YASAKLAMA\
                \n**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\
                \n**Sohbet:** {get_display_name(await event.get_chat())}\
                \n**Sohbet ID:** `{event.chat_id}`\
                \n**Sebep:** {reason}",
            )
        else:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                f"#YASAKLAMA\
                \n**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\
                \n**Sohbet:** {get_display_name(await event.get_chat())}\
                \n**Sohbet ID:** `{event.chat_id}`",
            )


@doge.bot_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", plugin_category),
    info={
        "h": "Gruptaki üyenin yasağını kaldırır.",
        "d": "Kullanıcı hesabını grubun yasaklı listesinden kaldırır.",
        "u": [
            "{tr}unban <ID/kullanıcı adı/yanıt>",
            "{tr}unban <ID/kullanıcı adı/yanıt> <isteğe bağlı sebep>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "Gruptaki üyenin yasağını kaldırır."
    user, reason = await get_user_from_event(event)
    if not user:
        return
    dogevent = await eor(event, "`Yasağını kaldırıyorum...`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        if reason:
            await dogevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)}** yasağını başarıyla kaldırdım!**\n**Sebep:** `{reason}`"
            )
        else:
            await dogevent.edit(
                f"{_format.mentionuser(user.first_name ,user.id)}** yasağını başarıyla kaldırdım!**"
            )
        if BOTLOG:
            if reason:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    f"#YASAK_KALDIRMA\
                    \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
                    \n**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`\
                    \n**Sebep:** {reason}",
                )
            else:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    f"#YASAK_KALDIRMA\
                    \n**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\
                    \n**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`",
                )
    except UserIdInvalidError:
        await dogevent.edit(
            "**Hayatımda hiç böyle birini görmedim, onun bir mesajını yanıtlarsan tanıyabilirim.**"
        )
    except Exception as e:
        if BOTLOG:
            await dogevent.edit(
                "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
            )
            await doge.bot.send_message(
                BOTLOG_CHATID, "#YASAK_KALDIRMA_HATASI\n" f"**Hata:** {e}"
            )


@doge.bot_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.error(f"🚨 Susturulmuş üyenin mesajını silemedim: {str(e)}")


@doge.bot_cmd(
    pattern="mute(?:\s|$)([\s\S]*)",
    command=("mute", plugin_category),
    info={
        "h": "Gruptaki üyenin mesaj göndermesini engeller.",
        "d": "Eğer yönetici değilse, gruptaki iznini değiştirir. Eğer yönetici ise veya kişisel sohbette denerseniz, mesajları otomatik olarak silinir.",
        "u": [
            "{tr}mute <ID/kullanıcı adı/yanıt>",
            "{tr}mute <ID/kullanıcı adı/yanıt> <isteğe bağlı sebep>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },  # sourcery no-metrics
)
async def startmute(event):
    "Gruptaki üyenin mesaj göndermesini engeller."
    if event.is_private:
        await event.edit("`Bu kullanıcının mesaj göndermesini engelliyorum...`")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit("**Bu kullanıcının zaten susturulmuş!**")
        if event.chat_id == doge.uid:
            return await edl(event, "**Kendini susturamazsın!**")
        if await wowmydev(replied_user, event):
            return
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )
                await doge.bot.send_message(
                    BOTLOG_CHATID, "#YASAK_KALDIRMA_HATASI\n" f"**Hata:** {e}"
                )
        else:
            await event.edit("**Kullanıcıyı başarıyla susturdum!**")
        if BOTLOG:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "#PM_SUSTURMA\n"
                f"**Kullanıcı:** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(
                event,
                "**Bunu yapabilmek için yeterli iznim yok!**",
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        user_id = user.id
        if user_id == doge.uid:
            return await eor(event, "**Kendini susturamazsın!**")
        if await wowmydev(user_id, event):
            return
        if is_muted(user_id, event.chat_id):
            return await eor(event, "**Bu kullanıcı zaten susturulmuş!**")
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
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )
                return await doge.bot.send_message(
                    BOTLOG_CHATID, "#SUSTURMA_HATASI\n" f"**Hata:** {e}"
                )
        try:
            await event.client(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await eor(
                        event,
                        "**Mesaj silme yetkim yok ve bir kişiyi susturamam.**",
                    )
            elif "creator" not in vars(chat):
                return await eor(
                    event,
                    "**Bunu yapabilmek için yeterli yetkim yok.**",
                )
            mute(user_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )
                return await doge.bot.send_message(
                    BOTLOG_CHATID, "#SUSTURMA_HATASI\n" f"**Hata:** {e}"
                )
        if reason:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name, user_id)} üyesini, {get_display_name(await event.get_chat())}** grubunda susturdum!**\n"
                f"**Sebep:** `{reason}`",
            )
        else:
            await eor(
                event,
                f"{_format.mentionuser(user.first_name ,user_id)} üyesini, {get_display_name(await event.get_chat())}** grubunda susturdum!**\n",
            )
        if BOTLOG:
            if reason:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    "#SUSTURMA\n"
                    f"**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\n"
                    f"**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`\
                    \n**Sebep:** {reason}",
                )
            else:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    "#SUSTURMA\n"
                    f"**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\n"
                    f"**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`",
                )


@doge.bot_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", plugin_category),
    info={
        "h": "Kullanıcının tekrar mesaj göndermesine izin verir.",
        "d": "Mesaj göndermek için kullanıcı izinlerini değiştirir.",
        "u": [
            "{tr}unmute <ID/kullanıcı adı/yanıt>",
            "{tr}unmute <ID/kullanıcı adı/yanıt> <isteğe bağlı sebep>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },  # sourcery no-metrics
)
async def endmute(event):
    "Kullanıcının tekrar mesaj göndermesine izin verir."
    if event.is_private:
        await event.edit("`Bu kullanıcının mesaj göndermesine izin veriyorum...`")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit("**__Bu kullanıcı zaten özgürce konuşabiliyor.__**")
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            if BOTLOG:
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )
                await doge.bot.send_message(
                    BOTLOG_CHATID, "#PM_SUSTURMA_KALDIRMA_HATASI\n" f"**Hata:** {e}"
                )
        else:
            await event.edit("**Bu kullanıcı artık özgürce konuşabilir.**")
        if BOTLOG:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "#PM_SUSTURULMA_KALDIRILMASI\n"
                f"**Kullanıcı:** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, reason = await get_user_from_event(event)
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
                "**Bu kullanıcı zaten bu sohbette özgürce konuşabiliyor.**",
            )
        except Exception as e:
            if BOTLOG:
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )
                return await doge.bot.send_message(
                    BOTLOG_CHATID, "#SUSTURMA_KALDIRMA_HATASI\n" f"**Hata:** {e}"
                )
            else:
                await event.edit(
                    "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__"
                )

        await eor(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)}, {get_display_name(await event.get_chat())} **grubunda sesi açıldı!**\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍",
        )
        if BOTLOG:
            if reason:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    "#SUSTURMA_KALDIRMA\n"
                    f"**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\n"
                    f"**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`\
                    \n**Sebep:** {reason}",
                )
            else:
                await doge.bot.send_message(
                    BOTLOG_CHATID,
                    "#SUSTURMA_KALDIRMA\n"
                    f"**Kullanıcı:** [{user.first_name}](tg://user?id={user.id})\n"
                    f"**Sohbet:** {get_display_name(await event.get_chat())}\
                    \n**Sohbet ID:** `{event.chat_id}`",
                )


@doge.bot_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", plugin_category),
    info={
        "h": "Bir kişiyi gruptan atar.",
        "d": "Kullanıcıyı gruptan atar, böylece geri katılabilir.",
        "u": [
            "{tr}kick <ID/kullanıcı adı/yanıt>",
            "{tr}kick <ID/kullanıcı adı/yanıt> <isteğe bağlı sebep>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "Bir kişiyi gruptan atar."
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if await wowmydev(user_id, event):
        return
    dogevent = await eor(event, "`Kullanıcıyı atıyorum...`")
    try:
        await event.client.kick_participant(event.chat_id, user_id)
    except Exception:
        return await dogevent.edit("`Bunu yapabilmek için yeterli iznim yok.`")
    if reason:
        await dogevent.edit(
            f"[{user.first_name}](tg://user?id={user_id}) **buradan atıldın!**\n**Sebep:** `{reason}`"
        )
    else:
        await dogevent.edit(
            f"[{user.first_name}](tg://user?id={user_id}) **buradan atıldın!**"
        )
    if BOTLOG:
        if reason:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "#GRUPTAN_ATMA\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\n"
                f"**Sohbet:** {get_display_name(await event.get_chat())}\
                \n**Sohbet ID:** `{event.chat_id}`\
                \n**Sebep:** {reason}",
            )
        else:
            await doge.bot.send_message(
                BOTLOG_CHATID,
                "#GRUPTAN_ATMA\n"
                f"**Kullanıcı:** [{user.first_name}](tg://user?id={user_id})\n"
                f"**Sohbet:** {get_display_name(await event.get_chat())}\
                \n**Sohbet ID:** `{event.chat_id}`",
            )


@doge.bot_cmd(
    pattern="pin( s|$)",
    command=("pin", plugin_category),
    info={
        "h": "Sohbette mesajı sabitler.",
        "d": "Sohbette bir mesajı sabitlemek için mesaja yanıt verin.",
        "o": {"s": "Üyelere bildirim göndererek sabitler."},
        "u": [
            "{tr}pin <yanıt>",
            "{tr}pin s <yanıt>",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
)
async def pin(event):
    "Sohbette mesajı sabitler."
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edl(event, "**Sabitleyebilmek için bir mesaja cevap verin.**", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edl(event, "`Bunu yapabilmek için yeterli iznim yok.`", 5)
    except Exception as e:
        if BOTLOG:
            await edl(
                event,
                "__Oops..! Bir hatayla karşılaştım! Hata raporunu Log grubunuza gönderdim. Lütfen kontrol edin.__",
            )
            return await doge.bot.send_message(
                BOTLOG_CHATID, f"Mesaj sabitlerken bir hatayla karşılaşıldı: `{e}`"
            )
        else:
            await edl(
                event, f"**Beklenmeyen bir hatayla karşılaşıldı! Hata Raporu:** {e}"
            )
    await edl(event, "**Mesajı sabitledim!**", 5)
    a = "Hayır" if not is_silent else "Evet"
    if BOTLOG and not event.is_private:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"#SABİTLEME\
            \n__Gruptaki mesajı başarıyla sabitledim!__\
            \n**Sohbet:** {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
            \n**Sesli**: {a}",
        )


@doge.bot_cmd(
    pattern="unpin(all|$)",
    command=("unpin", plugin_category),
    info={
        "h": "Sohbetteki mesajları sabitten çıkarır.",
        "d": "Sabitten kaldırmak istediğiniz mesajı yanıtlayın ya da hepsini kaldırmak için `{tr}unpinall` komutunu kullanın.",
        "o": {"all": "Sohbetteki tüm sabitli mesajları kaldırır."},
        "u": [
            "{tr}unpin <yanıt>",
            "{tr}unpinall",
        ],
        "note": "Bunu yapabilmek için yeterli haklarınız olmalıdır.",
    },
)
async def pin(event):
    "Sohbetteki mesajları sabitten çıkarır."
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edl(
            event,
            f"__Sabitten kaldırmak istediğiniz mesajı yanıtlayın ya da hepsini kaldırmak için__ `{tr}unpinall` __komutunu kullanın.__",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edl(
                event,
                f"__Sabitten kaldırmak istediğiniz mesajı yanıtlayın ya da hepsini kaldırmak için__ `{tr}unpinall` __komutunu kullanın.__",
                5,
            )
    except BadRequestError:
        return await edl(event, "`Bunu yapabilmek için yeterli iznim yok.`", 5)
    except Exception as e:
        return await edl(event, f"`{e}`", 5)
    await edl(event, "**Sabitli mesaj(lar)ı başarıyla kaldırdım!**", 5)
    if BOTLOG and not event.is_private:
        await doge.bot.send_message(
            BOTLOG_CHATID,
            f"#SABITLEME_KALDIRMA\
            \n**__Sabitli mesaj(lar)ı başarıyla sabitten kaldırdım!__**\
            \n**Sohbet:**: {get_display_name(await event.get_chat())}\
            \n**Sohbet ID:** `{event.chat_id}`",
        )


@doge.bot_cmd(
    pattern="undlt( .m)?(?: |$)(\d*)?",
    command=("undlt", plugin_category),
    info={
        "h": "Gruptaki son silinmiş mesajları getirir.",
        "d": "Gruptaki son silinmiş mesajları varsayılan olarak 5 tane getirir. 1 ila 15 mesaj getirebilir.",
        "f": {"m": "Gruptaki silinen son fotoğrafları getirir."},
        "u": [
            "{tr}undlt <sayı>",
            "{tr}undlt .m <sayı>",
        ],
        "e": [
            "{tr}undlt 7",
            "{tr}undlt .m 3",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):
    "Gruptaki son silinmiş mesajları getirir."
    dogevent = await eor(event, "__Son eylemler aranıyor...__")
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
