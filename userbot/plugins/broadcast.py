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
        "header": "To message to person or to a chat.",
        "description": "Suppose you want to message directly to a person/chat from a paticular chat. Then simply reply to a person with this cmd and text or to a text with cmd and username/userid/chatid,",
        "usage": [
            "{tr}msgto <username/userid/chatid/chatusername> reply to message",
            "{tr}msgto <username/userid/chatid/chatusername> <text>",
        ],
        "examples": "{tr}msgto @SohbetDoge just a testmessage",
    },
)
async def dogebroadcast_add(event):
    "To message to person or to a chat."
    user, reason = await get_user_from_event(event)
    reply = await event.get_reply_message()
    if not user:
        return
    if not reason and not reply:
        return await edl(
            event, "__What should i send to the person. reply to msg or give text__"
        )
    if reply and reason and user.id != reply.sender_id:
        if BOTLOG:
            msg = await event.client.send_message(BOTLOG_CHATID, reason)
            await event.client.send_message(
                BOTLOG_CHATID,
                "The replied message was failed to send to the user. Confusion between to whom it should send.",
                reply_to=msg.id,
            )
        msglink = await event.client.get_msg_link(msg)
        return await eor(
            event,
            f"__Sorry! Confusion between users to whom should i send the person mentioned in message or to the person replied. text message was logged in [log group]({msglink}). you can resend message from there__",
        )
    if reason:
        msg = await event.client.send_message(user.id, reason)
    else:
        msg = await event.client.send_message(user.id, reply)
    await edl(event, "__Successfully sent the message.__")


@doge.bot_cmd(
    pattern="addto(?:\s|$)([\s\S]*)",
    command=("addto", plugin_category),
    info={
        "header": "Will add the specific chat to the mentioned category",
        "usage": "{tr}addto <category name>",
        "examples": "{tr}addto test",
    },
)
async def dogebroadcast_add(event):
    "To add the chat to the mentioned category"
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "In which category should i add this chat",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    check = is_in_broadcastlist(keyword, event.chat_id)
    if check:
        return await edl(
            event,
            f"This chat is already in this category {keyword}",
            parse_mode=_format.parse_pre,
        )
    add_to_broadcastlist(keyword, event.chat_id)
    await edl(
        event,
        f"This chat is Now added to category {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is added to category {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is added to category {keyword}",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="list(?:\s|$)([\s\S]*)",
    command=("list", plugin_category),
    info={
        "header": "will show the list of all chats in the given category",
        "usage": "{tr}list <category name>",
        "examples": "{tr}list test",
    },
)
async def dogebroadcast_list(event):
    "To list the all chats in the mentioned category."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "Which category Chats should i list ?\nCheck .listall",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await edl(
            event,
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event, f"Fetching info of the category {keyword}", parse_mode=_format.parse_pre
    )
    resultlist = f"**The category '{keyword}' have '{no_of_chats}' chats and these are listed below :**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **Channel** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **Group** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **User** \n  •  **Name : **{chatinfo.first_name} \n  •  **id : **`{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 __This id {int(chat)} in database probably you may left the chat/channel or may be invalid id.\
                            \nRemove this id from the database by using this command__ `.frmfrom {keyword} {int(chat)}` \n\n"
    finaloutput = resultlist + errorlist
    await eor(dogevent, finaloutput)


@doge.bot_cmd(
    pattern="listall$",
    command=("listall", plugin_category),
    info={
        "header": "Will show the list of all category names.",
        "usage": "{tr}listall",
    },
)
async def dogebroadcast_list(event):
    "To list all the category names."
    if num_broadcastlist_chats() == 0:
        return await edl(
            event,
            "you haven't created at least one category  check info for more help",
            parse_mode=_format.parse_pre,
        )
    chats = get_broadcastlist_chats()
    resultext = "**Here are the list of your category's :**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __contains {num_broadcastlist_chat(i)} chats__\n"
    await eor(event, resultext)


@doge.bot_cmd(
    pattern="sendto(?:\s|$)([\s\S]*)",
    command=("sendto", plugin_category),
    info={
        "header": "will send the replied message to all chats in the given category",
        "usage": "{tr}sendto <category name>",
        "examples": "{tr}sendto test",
    },
)
async def dogebroadcast_send(event):
    "To send the message to all chats in the mentioned category."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "To which category should i send this message",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    dog = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edl(
            event,
            "what should i send to to this category ?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    group_ = Get(dog)
    if no_of_chats == 0:
        return await edl(
            event,
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event,
        "sending this message to all groups in the category",
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
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in category {keyword}.`"
    await edl(dogevent, resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is sent to {i} chats out of {no_of_chats} chats in category {keyword}",
            parse_mode=_format.parse_pre,
        )


@doge.bot_cmd(
    pattern="fwdto(?:\s|$)([\s\S]*)",
    command=("fwdto", plugin_category),
    info={
        "header": "Will forward the replied message to all chats in the given category",
        "usage": "{tr}fwdto <category name>",
        "examples": "{tr}fwdto test",
    },
)
async def dogebroadcast_send(event):
    "To forward the message to all chats in the mentioned category."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "To which category should i send this message",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    dog = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edl(
            event,
            "what should i send to to this category ?",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    no_of_chats = num_broadcastlist_chat(keyword)
    group_ = Get(dog)
    if no_of_chats == 0:
        return await edl(
            event,
            f"There is no category with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = get_chat_broadcastlist(keyword)
    dogevent = await eor(
        event,
        "sending this message to all groups in the category",
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
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in category {keyword}.`"
    await edl(dogevent, resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is forwared to {i} chats out of {no_of_chats} chats in category {keyword}",
            parse_mode=_format.parse_pre,
        )


@doge.bot_cmd(
    pattern="rmfrom(?:\s|$)([\s\S]*)",
    command=("rmfrom", plugin_category),
    info={
        "header": "Will remove the specific chat to the mentioned category",
        "usage": "{tr}rmfrom <category name>",
        "examples": "{tr}rmfrom test",
    },
)
async def dogebroadcast_remove(event):
    "To remove the chat from the mentioned category"
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "From which category should i remove this chat",
            parse_mode=_format.parse_pre,
        )
    keyword = doginput_str.lower()
    check = is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await edl(
            event,
            f"This chat is not in the category {keyword}",
            parse_mode=_format.parse_pre,
        )
    rm_from_broadcastlist(keyword, event.chat_id)
    await edl(
        event,
        f"This chat is Now removed from the category {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is removed from category {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from category {keyword}",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="frmfrom(?:\s|$)([\s\S]*)",
    command=("frmfrom", plugin_category),
    info={
        "header": " To force remove the given chat from a category.",
        "description": "Suppose if you are muted or group/channel is deleted you can't send message there so you can use this cmd to the chat from that category",
        "usage": "{tr}frmfrom <category name> <chatid>",
        "examples": "{tr}frmfrom test -100123456",
    },
)
async def dogebroadcast_remove(event):
    "To force remove the given chat from a category."
    doginput_str = event.pattern_match.group(1)
    if not doginput_str:
        return await edl(
            event,
            "From which category should i remove this chat",
            parse_mode=_format.parse_pre,
        )
    args = doginput_str.split(" ")
    if len(args) != 2:
        return await edl(
            event,
            "Use proper syntax as shown .frmfrom category_name groupid",
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
                "Use proper syntax as shown .frmfrom category_name groupid",
                parse_mode=_format.parse_pre,
            )
    keyword = keyword.lower()
    check = is_in_broadcastlist(keyword, int(groupid))
    if not check:
        return await edl(
            event,
            f"This chat {groupid} is not in the category {keyword}",
            parse_mode=_format.parse_pre,
        )
    rm_from_broadcastlist(keyword, groupid)
    await edl(
        event,
        f"This chat {groupid} is Now removed from the category {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {chat.title} is removed from category {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from category {keyword}",
                parse_mode=_format.parse_pre,
            )


@doge.bot_cmd(
    pattern="delc(?:\s|$)([\s\S]*)",
    command=("delc", plugin_category),
    info={
        "header": "To Deletes the category completely from database",
        "usage": "{tr}delc <category name>",
        "examples": "{tr}delc test",
    },
)
async def dogebroadcast_delete(event):
    "To delete a category completely."
    doginput_str = event.pattern_match.group(1)
    check1 = num_broadcastlist_chat(doginput_str)
    if check1 < 1:
        return await edl(
            event,
            f"Are you sure that there is category {doginput_str}",
            parse_mode=_format.parse_pre,
        )
    try:
        del_keyword_broadcastlist(doginput_str)
        await eor(
            event,
            f"Successfully deleted the category {doginput_str}",
            parse_mode=_format.parse_pre,
        )
    except Exception as e:
        await edl(
            event,
            str(e),
            parse_mode=_format.parse_pre,
        )
