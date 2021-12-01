# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import User

from ..core.logger import logging
from ..sql_helper.globals import gvar, sgvar

LOGS = logging.getLogger("DogeUserBot")
odogeubc = "🧡 @DogeUserBot"


async def create_supergroup(group_name, client, botusername, descript, photo):
    try:
        result = await client(
            CreateChannelRequest(
                title=group_name,
                about=descript,
                megagroup=True,
            )
        )
        created_chat_id = result.chats[0].id
        result = await client(
            ExportChatInviteRequest(
                peer=created_chat_id,
            )
        )
        await client(
            InviteToChannelRequest(
                channel=created_chat_id,
                users=[botusername],
            )
        )
        if photo:
            await client(
                EditPhotoRequest(
                    channel=created_chat_id,
                    photo=photo,
                )
            )
    except Exception as e:
        return "error", str(e)
    if not str(created_chat_id).startswith("-100"):
        created_chat_id = int("-100" + str(created_chat_id))
    return result, created_chat_id


async def create_channel(channel_name, client, descript, photo):
    try:
        result = await client(
            CreateChannelRequest(
                title=channel_name,
                about=descript,
                megagroup=False,
            )
        )
        created_chat_id = result.chats[0].id
        result = await client(
            ExportChatInviteRequest(
                peer=created_chat_id,
            )
        )
        if photo:
            await client(
                EditPhotoRequest(
                    channel=created_chat_id,
                    photo=photo,
                )
            )
    except Exception as e:
        return "error", str(e)
    if not str(created_chat_id).startswith("-100"):
        created_chat_id = int("-100" + str(created_chat_id))
    return result, created_chat_id


async def autobotlog(BOTLOG, BOTLOG_CHATID, Config, doge):
    if BOTLOG:
        vinfo = "PRIVATE_GROUP_BOT_API_ID"
        try:
            entity = await doge.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.error(
                        f"🚨Belirtilen {vinfo} için mesaj göndermeyi eksik olan izinler."
                    )
                    return False
                if entity.default_banned_rights.invite_users:
                    LOGS.error(
                        f"🚨 Belirtilen {vinfo} için üye ekleme izni eksik. Lütfen kontrol edin!."
                    )
                    return False
        except ValueError:
            LOGS.error(
                f"🚨 {vinfo} değerini bulamadım. Lütfen doğru olduğundan emin olun!"
            )
            return False
        except TypeError:
            LOGS.error(
                f"🚨 {vinfo} desteklenmiyor/hatalı. Lütfen doğru olduğundan emin olun!"
            )
            return False
        except Exception as e:
            LOGS.error(
                f"🚨 {vinfo} değerini doğrulamaya çalışırken bir hata oluştu.\nHATA: {str(e)}"
            )
            return False
    else:
        descript = f"🚧 BU GRUBU SİLMEYİN!\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Doge çalışmayacaktır!\n\
        \n{odogeubc}"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogeBotLog.jpg")
        _, groupid = await create_supergroup(
            f"🐾 Doɢᴇ Boᴛ Loɢ", doge, Config.BOT_USERNAME, descript, gphoto
        )
        descmsg = f"**🚧 BU GRUPTAN AYRILMAYIN\
        \n🚧 BU GRUBU SİLMEYİN\
        \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🐾 Doge çalışmayacaktır!\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(groupid, descmsg)
        await msg.pin()
        sgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        vinfo = "PRIVATE_GROUP_BOT_API_ID"
        LOGS.info(
            f"✅ {vinfo} için özel grup başarıyla oluşturuldu ve değişkenler veritabanına yazıldı."
        )
    return True


async def autopmlog(PM_LOGGER_GROUP_ID, Config, doge):
    if Config.PMLOGGER:
        if PM_LOGGER_GROUP_ID != -100 or gvar("PM_LOGGER_GROUP_ID"):
            return True
        descript = f"🚧 BU GRUBU SİLMEYİN\n\
        \n🗑 Eğer silerseniz,\
        \n🚫 PM Logger çalışmayacaktır.\n\
        \n{odogeubc}"
        gphoto = await doge.upload_file(file="userbot/helpers/resources/DogePmLog.jpg")
        _, groupid = await create_supergroup(
            f"🐾 Doɢᴇ Pᴍ Loɢ", doge, Config.BOT_USERNAME, descript, gphoto
        )
        descmsg = f"**🚧 BU GRUPTAN AYRILMAYIN\
        \n🚧 BU GRUBU SİLMEYİN\
        \n🚧 BU GRUBU DEĞİŞTİRMEYİN!**\n\
        \n🗑 Eğer bu grubu silerseniz,\
        \n🚫 PM Logger özeliiği çalışmayacaktır.\n\
        \n**🦴 EĞER GRUBU SİLMEK İSTERSENİZ,\
        \n🔅 İLK ÖNCE ŞUNU YAZIN:**\
        \n`.set var PMLOGGER False`\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(groupid, descmsg)
        await msg.pin()
        sgvar("PM_LOGGER_GROUP_ID", groupid)
        LOGS.info(f"✅ PM_LOGGER_GROUP_ID için grup başarıyla oluşturuldu ve değerler yazıldı!")
    return True


async def checkingpmlog(PM_LOGGER_GROUP_ID, doge):
    if PM_LOGGER_GROUP_ID != -100:
        vinfo = "PM_LOGGER_GROUP_ID"
        try:
            entity = await doge.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.error(
                        f"🚨 Belirlilen {vinfo} için mesaj gönderme izni eksik. Doğruluğundan emin olun!"
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.error(
                        f"🚨Belirtilen {vinfo} için üye ekleme izni eksik. Doğruluğundan emin olun!"
                    )
        except ValueError:
            LOGS.error(f"🚨 {vinfo} değerini bulamadım. Doğruluğundan emin olun.")
        except TypeError:
            LOGS.error(f"🚨 {vinfo} desteklenmiyor. Doğruluğundan emin olun.")
        except Exception as e:
            LOGS.error(
                f"🚨 {vinfo} doğrulanmaya çalışırken bir hata oluştu.\nHATA: {str(e)}"
            )


async def autopluginch(PLUGIN_CHANNEL, Config, doge):
    if Config.PLUGINS:
        if PLUGIN_CHANNEL:
            return True
        descript = f"🚧 BU KANALI SİLMEYİN!\n\
        \n🗑 Eğer bu kanalı silerseniz;,\
        \n🧩 yüklenen tüm ekstra pluginler silinecektir!\n\
        \n{odogeubc}"
        cphoto = await doge.upload_file(
            file="userbot/helpers/resources/DogeExtraPlugin.jpg"
        )
        _, channelid = await create_channel(
            f"🐾 Doɢᴇ Eᴋsᴛʀᴀ Pʟᴜɢɪɴʟᴇʀ", doge, descript, cphoto
        )
        descmsg = f"**🚧 BU KANALI SİLMEYİN!\
        \n🚧 BU KANALI SİLMEYİN!\
        \n🚧 BU KANALDA DEĞİŞİKLİK YAPMAYIN!**\n\
        \n🗑 Eğer silerseniz,\
        \n🧩 yüklenen tüm ekstra pluginler silinecektir.\n\
        \n**🦴 EĞER KANALI SİLMEK İSTERSENİZ,\
        \n🔅 İLK ÖNCE ŞUNU YAZIN:**\
        \n`.set var PLUGINS False`\n\
        \n**{odogeubc}**"
        msg = await doge.send_message(channelid, descmsg)
        await msg.pin()
        sgvar("PLUGIN_CHANNEL", channelid)
        LOGS.info(
            "✅ PLUGIN_CHANNEL için gizli bir kanal başarıyla oluşturuldu ve veriler veritabanına yazıldı."
        )
    return True
