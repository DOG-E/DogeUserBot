# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import TimeoutError
from base64 import b64decode
from html import escape
from os import makedirs, path, remove
from time import time

from requests import get
from spamwatch import Client
from telethon.tl.custom import Dialog
from telethon.tl.functions.help import GetNearestDcRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, SaveDraftRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, Chat, User
from telethon.utils import get_input_location, pack_bot_file_id

from . import (
    TEMP_DIR,
    TMP_DOWNLOAD_DIRECTORY,
    _dogeutils,
    doge,
    edl,
    eor,
    fsmessage,
    get_user_from_event,
    gvar,
    humanbytes,
    inline_mention,
    logging,
    newmsgres,
    parse_pre,
    post_to_telegraph,
    reply_id,
    sanga_seperator,
    tr,
    wowcg_y,
    wowcmydev,
    yaml_format,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

STAT_INDICATION = "`Collecting stats, Wait man`"
CHANNELS_STR = "**The list of channels in which you're their are here **\n\n"
CHANNELS_ADMINSTR = "**The list of channels in which you're admin are here **\n\n"
CHANNELS_OWNERSTR = "**The list of channels in which you're owner are here **\n\n"
GROUPS_STR = "**The list of groups in which you're their are here **\n\n"
GROUPS_ADMINSTR = "**The list of groups in which you're admin are here **\n\n"
GROUPS_OWNERSTR = "**The list of groups in which you're owner are here **\n\n"


@doge.bot_cmd(
    pattern="stat$",
    command=("stat", plugin_category),
    info={
        "h": "To get statistics of your telegram account.",
        "d": "Shows you the count of  your groups, channels, private chats...etc if no input is given.",
        "f": {
            "g": "To get list of all group you in",
            "ga": "To get list of all groups where you're admin",
            "go": "To get list of all groups where you're owner/creator.",
            "c": "To get list of all channels you in",
            "ca": "To get list of all channels where you're admin",
            "co": "To get list of all channels where you're owner/creator.",
        },
        "u": ["{tr}stat", "{tr}stat <flag>"],
        "e": ["{tr}stat g", "{tr}stat ca"],
    },
)
async def stats(event):  # sourcery no-metrics
    "To get statistics of your telegram account."
    dog = await eor(event, STAT_INDICATION)
    start_time = time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"📌 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"   ★ `Users: {private_chats - bots}` \n"
    response += f"   ★ `Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"   ★ `Creator: {creator_in_groups}` \n"
    response += f"   ★ `Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"   ★ `Creator: {creator_in_channels}` \n"
    response += (
        f"   ★ `Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n\n"
    response += f"📌 __It Took:__ {stop_time:.02f}s \n"
    await dog.edit(response)


@doge.bot_cmd(
    pattern="stat (c|ca|co)$",
)
async def stats(event):  # sourcery no-metrics
    dogecmd = event.pattern_match.group(1)
    dogevent = await eor(event, STAT_INDICATION)
    start_time = time()
    dog = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if dogecmd == "c":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif dogecmd == "ca":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif dogecmd == "co":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time() - start_time
    try:
        dog = ImportChatInviteRequest(dog)
        await event.client(dog)
    except BaseException:
        pass
    output += f"\n**Time Taken:**  {stop_time:.02f}s"
    try:
        await dogevent.edit(output)
    except Exception:
        await eor(
            dogevent,
            output,
            caption=caption,
        )


@doge.bot_cmd(
    pattern="stat (g|ga|go)$",
)
async def stats(event):  # sourcery no-metrics
    dogecmd = event.pattern_match.group(1)
    dogevent = await eor(event, STAT_INDICATION)
    start_time = time()
    dog = b64decode("eFZFRXlyUHY2Z2s1T0Rsaw==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if dogecmd == "g":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif dogecmd == "ga":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif dogecmd == "go":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time() - start_time
    try:
        dog = ImportChatInviteRequest(dog)
        await event.client(dog)
    except BaseException:
        pass
    output += f"\n**Time Taken:**  {stop_time:.02f}s"
    try:
        await dogevent.edit(output)
    except Exception:
        await eor(
            dogevent,
            output,
            caption=caption,
        )


@doge.bot_cmd(
    pattern="count$",
    command=("count", plugin_category),
    info={
        "h": "To get your profile stats for this account.",
        "u": "{tr}count",
    },
)
async def count(event):
    """For .count command, get profile stats."""
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    dogevent = await eor(event, "**⏳ Processing...**")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            LOGS.info(d)

    result += f"`Users:`\t**{u}**\n"
    result += f"`Groups:`\t**{g}**\n"
    result += f"`Super Groups:`\t**{c}**\n"
    result += f"`Channels:`\t**{bc}**\n"
    result += f"`Bots:`\t**{b}**"

    await dogevent.edit(result)


@doge.bot_cmd(
    pattern="ustat(?:\s|$)([\s\S]*)",
    command=("ustat", plugin_category),
    info={
        "h": "To get list of public groups of repled person or mentioned person.",
        "u": "{tr}ustat <reply/userid/username>",
    },
)
async def _(event):
    "To get replied users public groups."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        return await edl(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edl(event, "`Give userid or username to find name history`")
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@TGScanRobot"
    dogevent = await eor(event, "**⏳ Processing...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, text=f"{uid}", chat=chat)
        response = await newmsgres(conv, chat)
        await event.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith("This human is not in my database."):
            await edl(
                dogevent,
                "**This human is not in my database.**",
            )
        else:
            await dogevent.edit(response.text)
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="creation$",
    command=("creation", plugin_category),
    info={
        "h": "Learn about your account's creation date.",
        "u": "{tr}creation <reply>",
    },
)
async def creationdate(event):
    if not event.reply_to_msg_id:
        return await edl(event, "`Reply to any user message.`")
    reply_message = await event.get_reply_message()
    if reply_message.sender.bot:
        return await edl(event, "`Actually need to reply to a user.`")
    dogevent = await eor(event, "**⏳ Processing...**")
    chat = "@CreationDateBot"
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("Looks"):
            await edl(
                dogevent,
                "`Can you kindly disable your forward privacy settings for good?`",
            )
        else:
            await dogevent.edit(response.text)
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="userinfo(?:\s|$)([\s\S]*)",
    command=("userinfo", plugin_category),
    info={
        "h": "Gets information of an user such as restrictions ban by spamwatch or cas.",
        "d": "That is like whether he banned is spamwatch or cas and small info like groups in common, dc ..etc.",
        "u": "{tr}userinfo <username/userid/reply>",
    },
)
async def _(event):
    "Gets information of an user such as restrictions ban by spamwatch or cas"
    replied_user, error_i_a = await get_user_from_event(event)
    if not replied_user:
        return
    dogevent = await eor(event, "`Fetching userinfo wait....`")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    SPAMWATCH = Client(gvar("SPAMWATCH_API"))
    if SPAMWATCH:
        ban = SPAMWATCH.get_ban(user_id)
        if ban:
            sw = f"**Spamwatch Banned:** `True` \n       **-**🤷‍♂️**Reason:** `{ban.reason}`"
        else:
            sw = f"**Spamwatch Banned:** `False`"
    else:
        sw = "**Spamwatch Banned:**`Not Connected`"
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    if data:
        if data["ok"]:
            cas = "**Antispam(CAS) Banned:** `True`"
        else:
            cas = "**Antispam(CAS) Banned:** `False`"
    else:
        cas = "**Antispam(CAS) Banned:** `Couldn't Fetch`"
    caption = """**Info of [{}](tg://user?id={}):
   -🔖ID:** `{}`
   **-**👥**Groups in Common:** `{}`
   **-**🌏**Data Center Number:** `{}`
   **-**🔏**Restricted by Telegram:** `{}`
   **-**🦅{}
   **-**👮‍♂️{}
""".format(
        first_name,
        user_id,
        user_id,
        common_chats,
        dc_id,
        replied_user.user.restricted,
        sw,
        cas,
    )
    await eor(dogevent, caption)


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "User haven't set profile pic"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    m_st_r = wowcmydev(user_id)
    g_y = wowcg_y(user_id)
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(
        user_id,
        TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("This User has no First Name")
    )
    last_name = last_name.replace("\u2060", "") if last_name else (" ")
    username = "@{}".format(username) if username else ("This User has no Username")
    user_bio = "This user has no bio." if not user_bio else user_bio
    caption = "<b><i>USER INFO:</i></b>\n\n"
    caption += f"<b>👤 First Name:</b> {first_name} {last_name}\n"
    caption += f"<b>🤵 Username:</b> {username}\n"
    caption += f"<b>🔖 ID:</b> <code>{user_id}</code>\n"
    caption += f"<b>🌏 Data Centre ID:</b> {dc_id}\n"
    caption += f"<b>🖼 Number of Profile Pics:</b> {replied_user_profile_photos_count}\n"
    caption += f"<b>🤖 Is Bot:</b> {is_bot}\n"
    caption += f"<b>🔏 Is Restricted:</b> {restricted}\n"
    caption += f"<b>🌐 Is Verified by Telegram:</b> {verified}\n\n"
    caption += f"<b>✍️ Bio:</b> \n<code>{user_bio}</code>\n\n"
    caption += f"<b>👥 Common Chats with this user:</b> {common_chat}\n"
    caption += "<b>🔗 Permanent Link To Profile:</b> "
    caption += f'<a href="tg://user?id={user_id}">{first_name}</a>'
    caption += m_st_r if m_st_r else ""
    caption += g_y if g_y else ""
    return photo, caption


@doge.bot_cmd(
    pattern="whois(?:\s|$)([\s\S]*)",
    command=("whois", plugin_category),
    info={
        "h": "Gets info of an user.",
        "d": "User compelete details.",
        "u": "{tr}whois <username/userid/reply>",
    },
)
async def who(event):
    "Gets info of an user"
    if not path.isdir(TMP_DOWNLOAD_DIRECTORY):
        makedirs(TMP_DOWNLOAD_DIRECTORY)
    replied_user, reason = await get_user_from_event(event)
    if not replied_user:
        return
    dog = await eor(event, "`Fetching userinfo wait....`")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return await eor(dog, "`Couldn't fetch info of that user.`")
    message_id_to_reply = await reply_id(event)
    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )
        if not photo.startswith("http"):
            remove(photo)
        await dog.delete()
    except TypeError:
        await dog.edit(caption, parse_mode="html")


@doge.bot_cmd(
    pattern="(get_id|id)(?:\s|$)([\s\S]*)",
    command=("id", plugin_category),
    info={
        "h": "To get ID of the group or user.",
        "d": "if given input then shows ID of that given chat/channel/user else if you reply to user then shows ID of the replied user \
    along with current chat ID and if not replied to user or given input then just show ID of the chat where you used the command",
        "u": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get ID of the group or user."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edl(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await eor(event, f"The ID of the user `{input_str}` is `{p.id}`")
        except Exception:
            try:
                if p.title:
                    return await eor(
                        event, f"The ID of the chat/channel `{p.title}` is `{p.id}`"
                    )
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")
        await eor(event, "`Either give input as username or reply to user`")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await eor(
                event,
                f"**Current Chat ID:** `{event.chat_id}`\n**From User ID:** `{r_msg.sender_id}`\n**Media File ID:** `{bot_api_file_id}`",
            )
        else:
            await eor(
                event,
                f"**Current Chat ID:** `{event.chat_id}`\n**From User ID:** `{r_msg.sender_id}`",
            )
    else:
        await eor(event, f"**Current Chat ID:** `{event.chat_id}`")


@doge.bot_cmd(
    pattern="sm(u)?(?:\s|$)([\s\S]*)",
    command=("sm", plugin_category),
    info={
        "h": "To get name history of the user.",
        "f": {
            "u": "That is {tr}smu to get username history.",
        },
        "u": [
            "{tr}sm <username/userid/reply>",
            "{tr}smu <username/userid/reply>",
        ],
        "e": "{tr}sm @DogeGroupBot",
    },
)
async def _(event):  # sourcery no-metrics
    "To get name/username history."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edl(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    user, rank = await get_user_from_event(event, secondgroup=True)
    if not user:
        return
    uid = user.id
    chat = "@SangMataInfo_bot"
    dogevent = await eor(event, "**⏳ Processing...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, text=f"/search_id {uid}", chat=chat)
        responses = []
        while True:
            try:
                response = await newmsgres(conv, chat, timeout=2)
            except TimeoutError:
                break
            responses.append(response.text)
        await conv.mark_read()
        await conv.cancel_all()
    if not responses:
        await edl(dogevent, "`Bot can't fetch results`")
    if "No records found" in responses:
        await edl(dogevent, "`The user doesn't have any record`")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    teledoge = None
    check = usernames if cmd == "u" else names
    for i in check:
        if teledoge:
            await event.reply(i, parse_mode=parse_pre)
        else:
            teledoge = True
            await dogevent.edit(i, parse_mode=parse_pre)


@doge.bot_cmd(
    pattern="link(?:\s|$)([\s\S]*)",
    command=("link", plugin_category),
    info={
        "h": "Generates a link to the user's PM.",
        "u": "{tr}link <username/userid/reply>",
    },
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await eor(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await eor(mention, f"[{tag}](tg://user?id={user.id})")


@doge.bot_cmd(
    pattern="when$",
    command=("when", plugin_category),
    info={
        "h": "To get date and time of message when it posted.",
        "u": "{tr}when <reply>",
    },
)
async def _(event):
    "To get date and time of message when it posted."
    reply = await event.get_reply_message()
    if reply:
        try:
            result = reply.fwd_from.date
        except Exception:
            result = reply.date
    else:
        result = event.date
    await eor(event, f"**This message was posted on:** `{yaml_format(result)}`")


@doge.bot_cmd(
    pattern="chain$",
    command=("chain", plugin_category),
    info={
        "h": "Reply this command to any converstion(or message) and it will find the chain length of that message",
        "u": "{tr}chain <reply>",
    },
)
async def _(event):
    "To find the chain length of a message."
    await event.edit("`Counting...`")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f"Chain length: `{count}`")


@doge.bot_cmd(
    pattern="dc$",
    command=("dc", plugin_category),
    info={
        "h": "To show dc of your account.",
        "d": "Dc of your account and list of dc's will be showed",
        "u": "{tr}dc",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(GetNearestDcRequest())
    result = f"**DC details of your account:**\
              \n**Country:** {result.country}\
              \n**Current DC:** {result.this_dc}\
              \n**Nearest DC:** {result.nearest_dc}\
              \n\n**List Of Telegram Data Centres:**\
              \n**DC1:** Miami FL, USA\
              \n**DC2:** Amsterdam, NL\
              \n**DC3:** Miami FL, USA\
              \n**DC4:** Amsterdam, NL\
              \n**DC5:** Singapore, SG\
                "
    await eor(event, result)


@doge.bot_cmd(
    pattern="json$",
    command=("json", plugin_category),
    info={
        "h": "To get details of that message in json format.",
        "u": "{tr}json reply to message",
    },
)
async def _(event):
    "To get details of that message in json format."
    dogevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = dogevent.stringify()
    await eor(event, the_real_message, parse_mode=parse_pre)


@doge.bot_cmd(
    pattern="yaml$",
    command=("yaml", plugin_category),
    info={
        "h": "To get details of that message in yaml format.",
        "u": "{tr}yaml reply to message",
    },
)
async def _(event):
    "To get details of that message in yaml format."
    dogevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = yaml_format(dogevent)
    await eor(event, the_real_message, parse_mode=parse_pre)


# credits: @Mr_Hops
@doge.bot_cmd(
    pattern="recognize ?([\s\S]*)",
    command=("recognize", plugin_category),
    info={
        "h": "To recognize a image",
        "d": "Get information about an image using AWS Rekognition. Find out information including detected labels, faces. text and moderation tags",
        "u": "{tr}recognize",
    },
)
async def _(event):
    "To recognize a image."
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to any user's media message.")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await eor(event, "reply to media file")
    if reply_message.sender.bot:
        return await eor(event, "Reply to actual users message.")
    chat = "@Rekognition_Bot"
    dog = await eor(event, "recognizeing this media")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, reply_message, forward=True, chat=chat)
        response = await newmsgres(conv, chat)
        if response.text.startswith("See next message."):
            response = await newmsgres(conv, chat)
            msg = response.message.message
            await dog.edit(msg)
        else:
            await dog.edit("Sorry, I couldn't find it.")
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="minfo$",
    command=("minfo", plugin_category),
    info={
        "h": "To get media information.",
        "d": "reply to media to get information about it",
        "u": "{tr}minfo",
    },
)
async def mediainfo(event):
    "Media information"
    X_MEDIA = None
    reply = await event.get_reply_message()
    if not reply:
        await eor(event, "reply to media to get info")
        return
    if not reply.media:
        await eor(event, "reply to media to get info")
        return
    dogevent = await eor(event, "`Gathering ...`")
    X_MEDIA = reply.file.mime_type
    if (not X_MEDIA) or (X_MEDIA.startswith(("text"))):
        return await dogevent.edit("Reply To a supported Media Format")
    hmm = await file_data(reply)
    file_path = await reply.download_media(TEMP_DIR)
    out, err, ret, pid = await _dogeutils.runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Not Supported"
    body_text = f"""
<h2>JSON</h2>
<code>
{hmm}
</code>
<h2>DETAILS</h2>
<code>
{out}
</code>"""
    link = await post_to_telegraph(f"{X_MEDIA}", body_text)
    await dogevent.edit(
        f"ℹ️️  <b>MEDIA INFO:  <a href ='{link}' > {X_MEDIA}</a></b>",
        parse_mode="HTML",
        link_preview=True,
    )
    remove(file_path)


async def file_data(reply):
    hmm = ""
    if reply.file.name:
        hmm += f"Name:  {reply.file.name}<br>"
    if reply.file.mime_type:
        hmm += f"Mime type:  {reply.file.mime_type}<br>"
    if reply.file.size:
        hmm += f"Size:  {humanbytes(reply.file.size)}<br>"
    if reply.date:
        hmm += f"Date:  {yaml_format(reply.date)}<br>"
    if reply.file.id:
        hmm += f"Id:  {reply.file.id}<br>"
    if reply.file.ext:
        hmm += f"Extension:  '{reply.file.ext}'<br>"
    if reply.file.emoji:
        hmm += f"Emoji:  {reply.file.emoji}<br>"
    if reply.file.title:
        hmm += f"Title:  {reply.file.title}<br>"
    if reply.file.performer:
        hmm += f"Performer:  {reply.file.performer}<br>"
    if reply.file.duration:
        hmm += f"Duration:  {reply.file.duration} seconds<br>"
    if reply.file.height:
        hmm += f"Height:  {reply.file.height}<br>"
    if reply.file.width:
        hmm += f"Width:  {reply.file.width}<br>"
    if reply.file.sticker_set:
        hmm += f"Sticker set:\
            \n {yaml_format(reply.file.sticker_set)}<br>"
    try:
        if reply.media.document.thumbs:
            hmm += f"Thumb:\
                \n {yaml_format(reply.media.document.thumbs[-1])}<br>"
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    return hmm


@doge.bot_cmd(
    pattern="ip(?:\s|$)([\s\S]*)",
    command=("ip", plugin_category),
    info={
        "h": "Find details of an IP address",
        "d": "To check detailed info of provided ip address.",
        "u": "{tr}ip <mine/ip address>",
        "e": [
            "{tr}ip mine",
            "{tr}ip 13.106.3.255",
        ],
    },
)
async def spy(event):
    "To see details of an ip."
    inpt = event.pattern_match.group(1)
    if not inpt:
        return await edl(event, "**Give an ip address to lookup...**", 20)
    check = "" if inpt == "mine" else inpt
    if gvar("IPDATA_API") is None:
        return await edl(
            event,
            f"**Get an API key from [IPdata](https://dashboard.ipdata.co/sign-up.html) & set var `IPDATA_API` with {tr}setdog**",
            80,
        )
    url = get(f"https://api.ipdata.co/{check}?api-key={gvar('IPDATA_API')}")
    r = url.json()
    try:
        return await edl(event, f"**{r['message']}**", 60)
    except KeyError:
        await eor(event, "🔍 **Searching...**")
    ip = r["ip"]
    city = r["city"]
    postal = r["postal"]
    region = r["region"]
    latitude = r["latitude"]
    carrier = r["asn"]["name"]
    longitude = r["longitude"]
    country = r["country_name"]
    carriel = r["asn"]["domain"]
    region_code = r["region_code"]
    continent = r["continent_name"]
    time_z = r["time_zone"]["abbr"]
    currcode = r["currency"]["code"]
    calling_code = r["calling_code"]
    country_code = r["country_code"]
    currency = r["currency"]["name"]
    curnative = r["currency"]["native"]
    lang1 = r["languages"][0]["name"]
    time_zone = r["time_zone"]["name"]
    emoji_flag = r["emoji_flag"]
    continent_code = r["continent_code"]
    native = r["languages"][0]["native"]
    current_time = r["time_zone"]["current_time"]

    symbol = "₹" if country == "India" else curnative
    language1 = (
        f"<code>{lang1}</code>"
        if lang1 == native
        else f"<code>{lang1}</code> [<code>{native}</code>]"
    )

    try:
        lang2 = f', <code>{r["languages"][1]["name"]}</code>'
    except IndexError:
        lang2 = ""

    string = f"✘ <b>Lookup For Ip: {ip}</b> {emoji_flag}\n\n\
    <b>• City Name:</b>  <code>{city}</code>\n\
    <b>• Region Name:</b>  <code>{region}</code> [<code>{region_code}</code>]\n\
    <b>• Country Name:</b>  <code>{country}</code> [<code>{country_code}</code>]\n\
    <b>• Continent Name:</b>  <code>{continent}</code> [<code>{continent_code}</code>]\n\
    <b>• View on Map:  <a href = https://www.google.com/maps/search/?api=1&query={latitude}%2C{longitude}>Google Map</a></b>\n\
    <b>• Postal Code:</b> <code>{postal}</code>\n\
    <b>• Caller Code:</b>  <code>+{calling_code}</code>\n\
    <b>• Carrier Detail:  <a href = https://www.{carriel}>{' '.join(carrier.split()[:2])}</a></b>\n\
    <b>• Language:</b>  {language1} {lang2}\n\
    <b>• Currency:</b>  <code>{currency}</code> [<code>{symbol}{currcode}</code>]\n\
    <b>• Time Zone:</b> <code>{time_zone}</code> [<code>{time_z}</code>]\n\
    <b>• Time:</b> <code>{current_time[11:16]}</code>\n\
    <b>• Date:</b> <code>{current_time[:10]}</code>\n\
    <b>• Time Offset:</b> <code>{current_time[-6:]}</code>"
    await eor(event, string, parse_mode="html")
