# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from os import remove

from telethon.tl.functions.channels import EditAdminRequest, InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import ChatAdminRights

from ..sql_helper.global_collectionjson import add_collection, get_collection
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    FBAN_GROUP_ID,
    _format,
    doge,
    edl,
    eor,
    fsmessage,
    get_user_from_event,
    logging,
    newmsgres,
    reply_id,
    tr,
    wowmydev,
)

plugin_category = "admin"
LOGS = logging.getLogger(__name__)

rose = "@MissRose_Bot"
fbanresults = [
    "New FedBan",
    "FedBan Reason update",
    "has already been fbanned, with the exact same reason.",
]
unfbanresults = ["I'll give", "Un-FedBan", "un-FedBan"]


@doge.bot_cmd(
    pattern="fban(?:\s|$)([\s\S]*)",
    command=("fban", plugin_category),
    info={
        "h": "Ban the person in your database federations",
        "d": "Will fban the person in the all feds of given category which you stored in database.",
        "u": "{tr}fban <userid/username/reply> <category> <reason>",
    },
)
async def group_fban(event):
    "fban a person."
    if FBAN_GROUP_ID is None:
        return await edl(
            event,
            "__For working of this cmd you need to set FBAN_GROUP_ID in vars__",
        )
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, "__You can't fban yourself.__")
    flag = await wowmydev(user_id, event)
    if flag:
        return
    if not reason:
        return await edl(
            event, "__You haven't mentioned category name and reason for fban__"
        )
    reasons = reason.split(" ", 1)
    fedgroup = reasons[0]
    reason = "Not Mentioned" if len(reasons) == 1 else reasons[1]
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup in feds:
        fedids = feds[fedgroup]
    else:
        return await edl(
            event, f"__There is no such '{fedgroup}' named fedgroup in your database.__"
        )
    dogevent = await eor(
        event, f"Fbanning {_format.mentionuser(user.first_name ,user_id)}.."
    )
    fedchat = FBAN_GROUP_ID
    success = 0
    errors = []
    total = 0
    for i in fedids:
        total += 1
        try:
            async with event.client.conversation(fedchat) as conv:
                await conv.send_message(f"/joinfed {i}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                if (
                    "All new federation bans will now also remove the members from this chat."
                    not in reply.text
                ):
                    return await edl(
                        dogevent,
                        "__You must be owner of the group(FBAN_GROUP_ID) to perform this action__",
                    )
                await conv.send_message(f"/fban {user_id} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                check = False
                for txt in fbanresults:
                    if txt in reply.text:
                        success += 1
                        check = True
                if not check:
                    errors.append(reply.text)
        except Exception as e:
            errors.append(str(e))
    success_report = f"{_format.mentionuser(user.first_name ,user_id)} is succesfully banned in {success} feds of {total}\
        \n**Reason:** __{reason}__.\n"
    if errors != []:
        success_report += "\n**Error:**"
        for txt in errors:
            success_report += f"\n☞ __{txt}__"
    await eor(dogevent, success_report)


# Credit: @teamultroid; https://github.com/TeamUltroid/Ultroid/blob/main/plugins/fedutils.py


@doge.bot_cmd(
    pattern="superfban(?:\s|$)([\s\S]*)",
    command=("superfban", plugin_category),
    info={
        "h": "Super Ban the person in your database all federations",
        "d": "Yanıtlanan ya da verilen kullanıcı kimliği/kullanıcı adı ile kullanıcıyı yönetici olduğunuz tüm federasyonlardan yasaklar.",
        "u": "{tr}superfban <userid/username/reply> <category> <reason>",
    },
)
async def superfban(event):
    msg = await eor(event, f"SüperFBan başlatılıyor...")
    inputt = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        FBAN = (await event.get_reply_message()).sender_id
        if inputt:
            REASON = inputt
    elif inputt:
        REASON = "#DOGE_SUPERFBAN"
        arg = event.text.split()
        if len(arg) == 2:
            FBAN = await event.client.parse_id(arg[1])
        elif len(arg) > 2:
            FBAN = await event.client.parse_id(arg[1])
            REASON = event.text.split(maxsplit=2)[-1]
        else:
            return await msg.edit(
                f"Lütfen geçerli bir kullanıcı adı ya da kullanıcı kimliği verin!"
            )
    else:
        return await msg.edit(
            "Kullanıcı belirtilmedi! SüperFBan kullanmak için lütfen bir kullanıcı belirtin ya da bir kullanıcısın mesajını yanıtlayın!"
        )
    flag = await wowmydev(FBAN, event)
    if flag:
        return
    if FBAN_GROUP_ID:
        chat = int(FBAN_GROUP_ID)
    else:
        return await msg.edit(
            f"SüperFBan özelliğini kullanmak için lütfen FBAN_GROUP_ID değeri ekleyin!"
        )
    fedList = []
    if not fedList:
        for a in range(3):
            async with event.client.conversation(rose) as bot_conv:
                await bot_conv.send_message("/start")
                await sleep(2)
                await bot_conv.send_message("/myfeds")
                await sleep(2)
                try:
                    response = await bot_conv.get_response()
                except TimeoutError:
                    return await msg.edit(
                        f"@MissRose_Bot cevap vermiyor!",
                    )
                await sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await sleep(3)
                    fedfile = await bot_conv.get_response()
                    await sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await doge.download_media(
                            fedfile,
                            "fedlist",
                        )
                        await sleep(6)
                        file = open(downloaded_file_name, errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "You can only use fed commands once every 5 minutes" in (
                        await bot_conv.get_edit
                    ):
                        return await msg.edit(
                            f"@MissRose_Bot kısıtlamaları yüzünden 5 dakika sonra tekrar deneyin!"
                        )
                if not fedList:
                    await msg.edit(
                        f"Yöneticisi olduğunuz federasyonlar bulunamadı! Tekrar deneniyor ({a+1}/3)...",
                    )
                else:
                    break
        else:
            await msg.edit("Hata")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
    if not fedList:
        return await msg.edit("Yöneticisi olduğunuz federasyonlar bulunamadı!")
    await msg.edit(f"{len(fedList)} tane federasyondan yasaklanıyor...")
    try:
        await add_rose_to_fban_group(FBAN_GROUP_ID)
        await doge.send_message(chat, "/start")
    except BaseException:
        return await msg.edit(
            f"Veritabanınızdaki FBAN_GROUP_ID değeri hatalı! Lütfen kontrol edip düznledikten sonra tekrar deneyin."
        )
    await sleep(3)
    for fed in fedList:
        await event.client.send_message(chat, f"/joinfed {fed}")
        await sleep(3)
        await event.client.send_message(chat, f"/fban {FBAN} {REASON}")
        await sleep(3)
    try:
        remove("fedlist")
    except Exception as e:
        print(f"Fedadmin dosyasını kaldırırken hata oluştu.\n{e}")
    await msg.edit(
        f"SüperFBan tamamlandı!\nToplam Federasyonlar - {len(fedList)}.\n#DOGE",
    )


@doge.bot_cmd(
    pattern="unfban(?:\s|$)([\s\S]*)",
    command=("unfban", plugin_category),
    info={
        "h": "UnBan the person in your database federations",
        "d": "Will unfban the person in the all feds of given category which you stored in database.",
        "u": "{tr}unfban <userid/username/reply> <category> <reason>",
    },
)
async def group_unfban(event):
    "unfban a person."
    if FBAN_GROUP_ID is None:
        return await edl(
            event,
            "__For working of this cmd you need to set FBAN_GROUP_ID in vars__",
        )
    user, reason = await get_user_from_event(event)
    if not user:
        return
    user_id = user.id
    if user_id == event.client.uid:
        return await edl(event, "__You can't unfban yourself.__")
    if not reason:
        return await edl(
            event, "__You haven't mentioned category name and reason for unfban__"
        )
    reasons = reason.split(" ", 1)
    fedgroup = reasons[0]
    reason = "Not Mentioned" if len(reasons) == 1 else reasons[1]
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup in feds:
        fedids = feds[fedgroup]
    else:
        return await edl(
            event, f"__There is no such '{fedgroup}' named fedgroup in your database.__"
        )
    dogevent = await eor(
        event, f"Unfbanning {_format.mentionuser(user.first_name ,user_id)}.."
    )
    fedchat = FBAN_GROUP_ID
    success = 0
    errors = []
    total = 0
    for i in fedids:
        total += 1
        try:
            async with event.client.conversation(fedchat) as conv:
                await conv.send_message(f"/joinfed {i}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                if (
                    "All new federation bans will now also remove the members from this chat."
                    not in reply.text
                ):
                    return await edl(
                        dogevent,
                        "__You must be owner of the group(FBAN_GROUP_ID) to perform this action__",
                    )
                await conv.send_message(f"/unfban {user_id} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )
                check = False
                for txt in unfbanresults:
                    if txt in reply.text:
                        success += 1
                        check = True
                if not check:
                    errors.append(reply.text)
        except Exception as e:
            errors.append(str(e))
    success_report = f"{_format.mentionuser(user.first_name ,user_id)} is succesfully unbanned in {success} feds of {total}\
        \n**Reason:** __{reason}__.\n"
    if errors != []:
        success_report += "\n**Error:**"
        for txt in errors:
            success_report += f"\n☞ __{txt}__"
    await eor(dogevent, success_report)


@doge.bot_cmd(
    pattern="superunfban(?:\s|$)([\s\S]*)",
    command=("superunfban", plugin_category),
    info={
        "h": "SuperUnBan the person in your database all federations",
        "d": "Yanıtlanan ya da verilen kullanıcı kimliği/kullanıcı adı ile kullanıcıyı yönetici olduğunuz tüm federasyonlardan yasağını kaldırır.",
        "u": "{tr}superunfban <userid/username/reply> <category> <reason>",
    },
)
async def _(event):
    msg = await eor(event, f"SüperUnFBan başlatılıyor..")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await doge.download_media(
                previous_message,
                "fedlist",
            )
            file = open(downloaded_file_name, encoding="utf8")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except BaseException:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            FBAN = arg[1]
            REASON = arg[2] if len(arg) > 2 else ""
        else:
            FBAN = previous_message.sender_id
            try:
                REASON = event.text.split(" ", maxsplit=1)[1]
            except BaseException:
                REASON = ""
            if REASON.strip() == "":
                REASON = ""
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            try:
                FBAN = arg[1]
                REASON = arg[2]
            except BaseException:
                return await msg.edit(
                    f"Lütfen geçerli bir kullanıcı adı ya da kullanıcı kimliği verin!"
                )
        else:
            try:
                FBAN = arg[1]
                REASON = " #DOGE_SUPERUNFBAN "
            except BaseException:
                return await msg.edit(
                    f"Lütfen geçerli bir kullanıcı adı ya da kullanıcı kimliği verin!"
                )
    if FBAN_GROUP_ID:
        chat = int(FBAN_GROUP_ID)
    else:
        chat = await event.get_chat()
    if not fedList:
        for a in range(3):
            async with event.client.conversation(rose) as bot_conv:
                await bot_conv.send_message("/start")
                await sleep(3)
                await bot_conv.send_message("/myfeds")
                await sleep(3)
                try:
                    response = await bot_conv.get_response()
                except TimeoutError:
                    return await msg.edit(
                        "@MissRose_Bot cevap vermiyor!",
                    )
                await sleep(3)
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await sleep(3)
                    fedfile = await bot_conv.get_response()
                    await sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await doge.download_media(
                            fedfile,
                            "fedlist",
                        )
                        await sleep(6)
                        file = open(downloaded_file_name, errors="ignore")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except BaseException:
                                pass
                    elif "You can only use fed commands once every 5 minutes" in (
                        await bot_conv.get_edit
                    ):
                        return await msg.edit(
                            "@MissRose_Bot kısıtlamaları yüzünden 5 dakika sonra tekrar deneyin!"
                        )
                if not fedList:
                    await msg.edit(
                        f"Yöneticisi olduğunuz federasyonlar bulunamadı! Tekrar deneniyor ({a+1}/3)...",
                    )
                else:
                    break
        else:
            await msg.edit("Hata")
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True
            elif In:
                tempFedId += x
    if not fedList:
        return await msg.edit("Yöneticisi olduğunuz federasyonlar bulunamadı!")
    await msg.edit(f"{len(fedList)} tane federasyondan yasağı kaldırılıyor...")
    try:
        await add_rose_to_fban_group(FBAN_GROUP_ID)
        await event.client.send_message(chat, "/start")
    except BaseException:
        return await msg.edit(
            "Veritabanınızdaki FBAN_GROUP_ID değeri hatalı! Lütfen kontrol edip düznledikten sonra tekrar deneyin."
        )
    await sleep(3)
    for fed in fedList:
        await doge.send_message(chat, f"/joinfed {fed}")
        await sleep(3)
        await doge.send_message(chat, f"/unfban {FBAN} {REASON}")
        await sleep(3)
    try:
        remove("fedlist")
    except Exception as e:
        print(f"Fedadmin dosyasını kaldırırken hata oluştu.\n{e}")
    await msg.edit(
        f"SüperUnFBan tamamlandı.\nToplam Federasyonlar - {len(fedList)}.\n#DOGE",
    )


@doge.bot_cmd(
    pattern="addfed (\w+|.all) ([-\w]+)",
    command=("addfed", plugin_category),
    info={
        "h": "Add the federation to given category in database.",
        "d": "You can add multiple federations to one category like a group of feds under one category. And you can access all thoose feds by that name.",
        "f": {
            ".all": "If you want to add all your feds to database then use this as {tr}addfed .all <category name>"
        },
        "u": [
            "{tr}addfed <category name> <fedid>",
            "{tr}addfed .all <category name>",
        ],
    },
)
async def quote_search(event):  # sourcery no-metrics
    "Add the federation to database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    await add_rose_to_fban_group(FBAN_GROUP_ID)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup == ".all":
        dogevent = await eor(event, "`Tüm federallerinizi veritabanına ekleniyor...`")
        fedidstoadd = []
        async with event.client.conversation(rose) as conv:
            try:
                await fsmessage(event, text="/myfeds", chat=rose)
                await sleep(2)
                try:
                    response = await newmsgres(conv, rose)
                except TimeoutError:
                    return await eor(
                        dogevent,
                        "`Rose` __cevap vermiyor tekrar deneyin.__",
                    )
                if "can only" in response.text:
                    return await edl(dogevent, f"__{response.text}__")
                if "make a file" in response.text or "Looks like" in response.text:
                    await response.click(0)
                    await sleep(2)
                    response_result = await newmsgres(conv, rose)
                    await sleep(2)
                    if response_result.media:
                        fed_file = await event.client.download_media(
                            response_result,
                            "fedlist",
                        )
                        await sleep(5)
                        fedfile = open(fed_file, errors="ignore")
                        lines = fedfile.readlines()
                        for line in lines:
                            try:
                                fedidstoadd.append(line[:36])
                            except Exception:
                                pass
                else:
                    text_lines = response.text.split("`")
                    for fed_id in text_lines:
                        if len(fed_id) == 36 and fed_id.count("-") == 4:
                            fedidstoadd.append(fed_id)
            except Exception as e:
                await edl(
                    dogevent,
                    f"**Error while fecthing myfeds:**\n__{e}__",
                )
            await conv.mark_read()
            await conv.cancel_all()
        if not fedidstoadd:
            return await eor(
                dogevent,
                "__I have failed to fetch your feds or you aren't admin of any fed.__",
            )
        feds[fedid] = fedidstoadd
        add_collection("fedids", feds)
        await eor(
            dogevent,
            f"__Successfully added all your feds to database group__ **{fedid}**.",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#ADDFEDID\
                \n**Fed Group:** `{fedid}`\
                \nSuccessfully added all your feds to above database category.",
            )
        return
    if fedgroup in feds:
        fed_ids = feds[fedgroup]
        if fedid in fed_ids:
            return await edl(
                event, "__This fed is already part of this fed category.__"
            )
        fed_ids.append(fedid)
        feds[fedgroup] = fed_ids
    else:
        feds[fedgroup] = [fedid]
    add_collection("fedids", feds)
    await eor(event, "__The given fed is succesfully added to fed category.__")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#ADDFEDID\
            \n**FedID:** `{fedid}`\
            \n**Fed Group:** `{fedgroup}`\
            \nThe above fedid is sucessfully added to that fed category.",
        )


@doge.bot_cmd(
    pattern="delfed (\w+|.all) ([-\w]+)",
    command=("delfed", plugin_category),
    info={
        "h": "Remove the federation from given category in database.",
        "d": "To remove given fed from the given category name",
        "f": {
            ".all": "If you want to delete compelete category then use this flag as {tr}delfed .all <category name>"
        },
        "u": [
            "{tr}delfed <category name> <fedid>",
            "{tr}delfed .all <category name>",
        ],
    },
)
async def quote_search(event):
    "To remove the federation from database."
    fedgroup = event.pattern_match.group(1)
    fedid = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    if fedgroup == ".all":
        if fedid not in feds:
            return await edl(event, "__There is no such fedgroup in your database.__")
        feds[fedid] = []
        add_collection("fedids", feds)
        await eor(event, f"__Succesfully removed all feds in the category {fedid}__")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#REMOVEFEDID\
            \n**Fed Group:** `{fedid}`\
            \nDeleted this Fed category in your database.",
            )
        return
    if fedgroup not in feds:
        return await edl(event, "__There is no such fedgroup in your database.__")
    fed_ids = feds[fedgroup]
    if fedid not in fed_ids:
        return await edl(event, "__This fed is not part of given fed category.__")
    fed_ids.remove(fedid)
    feds[fedgroup] = fed_ids
    add_collection("fedids", feds)
    await eor(event, "__The given fed is succesfully removed from fed category.__")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#REMOVEFEDID\
        \n**FedID:** `{fedid}`\
        \n**Fed Group:** `{fedgroup}`\
        \nThe above fedid is sucessfully removed that fed category.",
        )


@doge.bot_cmd(
    pattern="listfed(s)?(?:\s|$)([\s\S]*)",
    command=("listfed", plugin_category),
    info={
        "h": "To list all feds in your database.",
        "d": "if you give input then will show only feds in that category else will show all feds in your database",
        "u": ["{tr}listfed", "{tr}listfed <category name>"],
    },
)
async def quote_search(event):
    "To list federations in database."
    fedgroup = event.pattern_match.group(2)
    if get_collection("fedids") is not None:
        feds = get_collection("fedids").json
    else:
        feds = {}
    output = ""
    if not fedgroup:
        for fedgrp in feds:
            fedids = feds[fedgrp]
            if fedids != []:
                output += f"\n• **{fedgrp}:**\n"
                for fid in fedids:
                    output += f"☞ `{fid}`\n"
    elif fedgroup in feds:
        fedids = feds[fedgroup]
        if fedids != []:
            output += f"\n• **{fedgroup}:**\n"
            for fid in fedids:
                output += f"☞ `{fid}`\n"
    else:
        return await edl(event, "__There is no such fedgroup in your database.__")
    if output != "" and fedgroup:
        output = (
            f"**The list of feds in the category** `{fedgroup}` **are:**\n" + output
        )
    elif output != "":
        output = "**The list of all feds in your database are:**\n" + output
    else:
        output = f"__There are no feds in your database try by adding them using {tr}addfed__"
    await eor(event, output)


@doge.bot_cmd(
    pattern="f(ed)?info(?:\s|$)([\s\S]*)",
    command=("fedinfo", plugin_category),
    info={
        "h": "To get fedinfo from rose.",
        "d": "If no reply is given then shows you fedinfo of which you created",
        "u": "{tr}fedinfo <fedid>",
    },
)
async def fetch_fedinfo(event):
    "To fetch fedinfo."
    input_str = (
        event.pattern_match.group(2).strip()
        if event.pattern_match.group(2) is not None
        else ""
    )
    dogevent = await eor(event, "`Fetching info about given fed...`")
    async with event.client.conversation(rose) as conv:
        try:
            await fsmessage(event, text=f"/fedinfo {input_str}", chat=rose)
            response = await newmsgres(conv, rose)
            await dogevent.edit(response.text)
        except Exception as e:
            await edl(
                dogevent,
                f"**Error while fecthing fedinfo:**\n__{e}__",
            )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="f(ed)?admins(?:\s|$)([\s\S]*)",
    command=("fadmins", plugin_category),
    info={
        "h": "To get fed admins from rose.",
        "d": "If no reply is given then shows you fedinfo of which you created",
        "u": "{tr}fedadmins <fedid>",
    },
)
async def fetch_fedinfo(event):
    "To fetch fed admins."
    input_str = (
        event.pattern_match.group(2).strip()
        if event.pattern_match.group(2) is not None
        else ""
    )
    dogevent = await eor(event, "`Fetching admins list of given fed...`")
    async with event.client.conversation(rose) as conv:
        try:
            await fsmessage(event, text=f"/fedadmins {input_str}", chat=rose)
            response = await newmsgres(conv, rose)
            await dogevent.edit(
                f"**FedID:** ```{input_str}```\n\n" + response.text
                if input_str
                else response.text
            )
        except Exception as e:
            await edl(
                dogevent,
                f"**Error while fecthing fedinfo:**\n__{e}__",
            )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="myfeds$",
    command=("myfeds", plugin_category),
    info={
        "h": "To get all feds where you're admin.",
        "u": "{tr}myfeds",
    },
)
async def myfeds_fedinfo(event):
    "list all feds in which you're admin."
    dogevent = await eor(event, "`Fetching list of feds...`")
    replyid = await reply_id(event)
    async with event.client.conversation(rose) as conv:
        try:
            await fsmessage(event, text="/myfeds", chat=rose)
            response = await newmsgres(conv, rose)
            if "can only" in response.text:
                return await edl(dogevent, f"__{response.text}__")
            if "Looks like" in response.text:
                await response.click(0)
                response = await newmsgres(conv, rose)
                await event.client.send_read_acknowledge(conv.chat_id)
                user = await event.client.get_me()
                await event.client.send_file(
                    event.chat_id,
                    response.message.media,
                    caption=f"List of feds in which {_format.mentionuser('I am' ,user.id)} admin are.",
                    reply_to=replyid,
                )
                await dogevent.delete()
                return
            await dogevent.edit(response.text)
        except Exception as e:
            await edl(
                dogevent,
                f"**Error while fecthing myfeds:**\n__{e}__",
            )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="f(ed)?stat(?:\s|$)([\s\S]*)",
    command=("fstat", plugin_category),
    info={
        "h": "To get fedstat data from rose.",
        "d": "If you haven't replied to any user or mentioned any user along with command then by default you will be input else mentioned user or replied user.",
        "u": [
            "{tr}fstat list of all federations you're banned in.",
            "{tr}fstat <fedid> shows you info of you in the given fed."
            "{tr}fstat <userid/username/reply> list of all federations he is banned in.",
            "{tr}fstat <userid/username/reply> <fedid> shows you info of the that user in the given fed.",
        ],
    },
)
async def fstat_rose(event):
    "To get fedstat data from rose."
    dogevent = await eor(event, "`Fetching fedstat from given deatils...`")
    user, fedid = await get_user_from_event(
        event, dogevent, secondgroup=True, noedits=True
    )
    if user is None:
        user = await event.client.get_me()
    user_id = user.id
    if fedid is None:
        fedid = ""
    replyid = await reply_id(event)
    async with event.client.conversation(rose) as conv:
        try:
            await fsmessage(
                event, text=f"/fedstat {user_id} {fedid.strip()}", chat=rose
            )
            response = await newmsgres(conv, rose)
            await event.client.send_read_acknowledge(conv.chat_id)
            if "can only" in response.text:
                return await edl(dogevent, f"__{response.text}__")
            if fedid == "":
                response = await conv.get_edit()
                result = f"**List of feds** {_format.mentionuser(user.first_name ,user_id)} **has been banned in are.**\n\n"
            else:
                result = f"**Fban info about** {_format.mentionuser(user.first_name ,user_id)} **is**\n\n"
            if "Looks like" in response.message:
                await response.click(0)
                response = await newmsgres(conv, rose)
                await event.client.send_read_acknowledge(conv.chat_id)
                await event.client.send_file(
                    event.chat_id,
                    response.message.media,
                    caption=f"List of feds {_format.mentionuser(user.first_name ,user_id)} has been banned in are.",
                    reply_to=replyid,
                )
                await dogevent.delete()
                return
            await dogevent.edit(result + response.text)
        except Exception as e:
            await edl(
                dogevent,
                f"**Error while fecthing fedstat:**\n__{e}__",
            )
        await conv.mark_read()
        await conv.cancel_all()


async def add_rose_to_fban_group(chat_id):
    try:
        await doge(
            AddChatUserRequest(
                chat_id=chat_id,
                user_id=rose,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await doge(
                InviteToChannelRequest(
                    channel=chat_id,
                    users=[rose],
                )
            )
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
    sleep(0.75)
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    try:
        await doge(EditAdminRequest(chat_id, rose, rights, "Rose"))
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
