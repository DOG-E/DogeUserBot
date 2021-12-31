# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from random import choice
from re import compile

from telethon import Button
from telethon.events import CallbackQuery
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.utils import get_display_name

from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from . import (
    BOT_USERNAME,
    BOTLOG_CHATID,
    _format,
    dgvar,
    doge,
    edl,
    eor,
    get_user_from_event,
    gvar,
    logging,
    mention,
    reply_id,
    sgvar,
    tr,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)
OWNER_ID = int(gvar("OWNER_ID"))


async def do_pm_permit_action(event, chat):  # sourcery no-metrics
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    try:
        MAX_FLOOD_IN_PMS = int(gvar("MAX_FLOOD_IN_PMS") or 6)
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 6
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
        custompmblock = gvar("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
                totalwarns=totalwarns,
                warns=warns,
                remwarns=remwarns,
            )
        else:
            USER_BOT_WARN_ZERO = f"**You were spamming my master** {my_mention}**'s inbox, henceforth you have been blocked.**"
        msg = await event.reply(USER_BOT_WARN_ZERO)
        await event.client(BlockRequest(chat.id))
        the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**Message Count:** {PM_WARNS[str(chat.id)]}"
        del PM_WARNS[str(chat.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
        try:
            return await event.client.send_message(
                BOTLOG_CHATID,
                the_message,
            )
        except BaseException:
            return
    custompmpermit = gvar("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(
            mention=mention,
            first=first,
            last=last,
            fullname=fullname,
            username=username,
            userid=userid,
            my_first=my_first,
            my_last=my_last,
            my_fullname=my_fullname,
            my_username=my_username,
            my_mention=my_mention,
            totalwarns=totalwarns,
            warns=warns,
            remwarns=remwarns,
        )
    elif gvar("pmmenu") is None:
        USER_BOT_NO_WARN = f"""__Hi__ {mention}__, I haven't approved you yet to personal message me.
You have {warns}/{totalwarns} warns until you get blocked by the DogeUserBot.
Choose an option from below to specify the reason of your message and wait for me to check it. __⬇️"""
    else:
        USER_BOT_NO_WARN = f"""__Hi__ {mention}__, I haven't approved you yet to personal message me.
You have {warns}/{totalwarns} warns until you get blocked by the DogeUserBot.
Don't spam my inbox. say reason and wait until my response.__"""
    sgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvar("pmmenu") is None:
            results = await event.client.inline_query(BOT_USERNAME, "pmpermit")
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            PM_PIC = gvar("PM_PIC")
            if PM_PIC:
                DOG = [x for x in PM_PIC.split()]
                PIC = list(DOG)
                DOG_IMG = choice(PIC)
            else:
                DOG_IMG = None
            if DOG_IMG is not None:
                msg = await event.client.send_file(
                    chat.id,
                    DOG_IMG,
                    caption=USER_BOT_NO_WARN,
                    reply_to=reply_to_id,
                    force_document=False,
                )
            else:
                msg = await event.client.send_message(
                    chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id
                )
    except Exception as e:
        LOGS.error(f"🚨 {e}")
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


async def do_pm_options_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "__Select option from above message and wait. Don't spam my inbox, this is your last warning.__"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**If I remember correctly I mentioned in my previous message that this is not the right place for you to spam. \
Though you ignored that message.So, I simply blocked you. \
Now you can't do anything unless my master comes online and unblocks you.**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**Reason:** __He/She didn't opt for any provided options and kept on messaging.__"
    sqllist.rm_from_list("pmoptions", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_enquire_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Hey! Have some patience. My master hasn't seen your message yet. \
My master usually responds to people, though idk about some exceptional users.__
__My master will respond when he/she comes online, if he/she wants to.__
**Please do not spam unless you wish to be blocked and reported.**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**If I remember correctly I mentioned in my previous message that this is not the right place for you to spam. \
Though you ignored that message. So, I simply blocked you. \
Now you can't do anything unless my master comes online and unblocks you.**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**Reason:** __He/She opted for enquire option but didn't wait after being told also and kept on messaging so blocked.__"
    sqllist.rm_from_list("pmenquire", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_request_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Hey have some patience. My master hasn't seen your message yet. \
My master usually responds to people, though idk about some exceptional users.__
__My master will respond when he/she comes back online, if he/she wants to.__
**Please do not spam unless you wish to be blocked and reported.**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**If I remember correctly I mentioned in my previous message that this is not the right place for you to spam. \
Though you ignored me and messaged me. So, i simply blocked you. \
Now you can't do anything unless my master comes online and unblocks you.**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**Reason:** __He/She opted for the request option but didn't wait after being told also so blocked.__"
    sqllist.rm_from_list("pmrequest", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_chat_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Heyy! I am busy right now I already asked you to wait know. After my work finishes. \
We can talk but not right know. Hope you understand.__
__My master will respond when he/she comes back online, if he/she wants to.__
**Please do not spam unless you wish to be blocked and reported.**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**If I remember correctly I mentioned in my previous message this is not the right place for you to spam. \
Though you ignored that message. So, I simply blocked you. \
Now you can't do anything unless my master comes online and unblocks you.**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                \n**Reason:** __He/She select opted for the chat option but didn't wait after being told also so blocked.__"
    sqllist.rm_from_list("pmchat", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_spam_action(event, chat):
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
    USER_BOT_WARN_ZERO = f"**If I remember correctly I mentioned in my previous message this is not the right place for you to spam. \
Though you ignored that message. So, I simply blocked you. \
Now you can't do anything unless my master comes online and unblocks you.**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**Reason:** he opted for spam option and messaged again."
    sqllist.rm_from_list("pmspam", chat.id)
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


@doge.bot_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvar("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return await do_pm_spam_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return await do_pm_chat_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return await do_pm_request_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return await do_pm_enquire_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return await do_pm_options_action(event, chat)
    await do_pm_permit_action(event, chat)


@doge.bot_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvar("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return
    if event.text and event.text.startswith(
        (
            f"{tr}block",
            f"{tr}disapprove",
            f"{tr}a",
            f"{tr}da",
            f"{tr}approve",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(
            chat.id, get_display_name(chat), start_date, chat.username, "For Outgoing"
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@doge.bot.on(CallbackQuery(data=compile(rb"show_pmpermit_options")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == OWNER_ID:
        text = "Idoit these options are for users who messages you, not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"""Ok, Now you're accessing the availabe menu of my master, {mention}.
__Let's make this smooth and let me know why you're here.__
**Choose one of the following reasons why you're here:**"""
    buttons = [
        (Button.inline(text="To enquire something.", data="to_enquire_something"),),
        (Button.inline(text="To request something.", data="to_request_something"),),
        (Button.inline(text="To chat with my master.", data="to_chat_with_my_master"),),
        (
            Button.inline(
                text="To spam my master's inbox.",
                data="to_spam_my_master_inbox",
            ),
        ),
    ]
    sqllist.add_to_list("pmoptions", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    await event.edit(text, buttons=buttons)


@doge.bot.on(CallbackQuery(data=compile(rb"to_enquire_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == OWNER_ID:
        text = "Idoit this options for user who messages you. not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Okay. Your request has been registered. Do not spam my master's inbox now. \
My master is busy right now, When My master comes online he/she will check your message and ping you. \
Then we can extend this conversation more but not right now.__"""
    sqllist.add_to_list("pmenquire", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@doge.bot.on(CallbackQuery(data=compile(rb"to_request_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == OWNER_ID:
        text = "Idoit this options for user who messages you. not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Okay. I have notified my master about this. When he/she comes comes online\
 or when my master is free he/she will look into this chat and will ping you so we can have a friendly chat.__\
**But right now please do not spam unless you wish to get blocked.**"""
    sqllist.add_to_list("pmrequest", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@doge.bot.on(CallbackQuery(data=compile(rb"to_chat_with_my_master")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == OWNER_ID:
        text = "Idoit these options are for users who message you. not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Yaa sure we can have a friendly chat but not right now. we can have this\
some other time. Right now I am a little busy. when I come online and if I am free. I will ping you ,this is Damm sure.__"""
    sqllist.add_to_list("pmchat", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@doge.bot.on(CallbackQuery(data=compile(rb"to_spam_my_master_inbox")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == OWNER_ID:
        text = "Idoit these options are for users who message you. not for you"
        return await event.answer(text, cache_time=0, alert=True)
    text = "`███████▄▄███████████▄\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓███░░░░░░░░░░░░█\
         \n██████▀▀▀█░░░░██████▀ \
         \n░░░░░░░░░█░░░░█\
         \n░░░░░░░░░░█░░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░░▀▀`\
         \n**So uncool, this is not your home. Go bother somewhere else.\
         \n\nAnd this is your last warning if you send one more message you will be blocked automatically.**"
    sqllist.add_to_list("pmspam", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmspam").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@doge.bot_cmd(
    pattern="pmguard (on|off)$",
    command=("pmguard", plugin_category),
    info={
        "h": "To turn on or turn off pmpermit.",
        "u": "{tr}pmguard on/off",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmpermit."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvar("pmpermit") is None:
            sgvar("pmpermit", "true")
            await edl(
                event, "__Pmpermit has been enabled for your account successfully.__"
            )
        else:
            await edl(event, "__Pmpermit is already enabled for your account__")
    elif gvar("pmpermit") is not None:
        dgvar("pmpermit")
        await edl(event, "__Pmpermit has been disabled for your account successfully__")
    else:
        await edl(event, "__Pmpermit is already disabled for your account__")


@doge.bot_cmd(
    pattern="pmmenu (on|off)$",
    command=("pmmenu", plugin_category),
    info={
        "h": "To turn on or turn off pmmenu.",
        "u": "{tr}pmmenu on/off",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmmenu."
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvar("pmmenu") is None:
            sgvar("pmmenu", "false")
            await edl(
                event,
                "__Pmpermit Menu has been disabled for your account successfully.__",
            )
        else:
            await edl(event, "__Pmpermit Menu is already disabled for your account__")
    elif gvar("pmmenu") is not None:
        dgvar("pmmenu")
        await edl(
            event, "__Pmpermit Menu has been enabled for your account successfully__"
        )
    else:
        await edl(event, "__Pmpermit Menu is already enabled for your account__")


@doge.bot_cmd(
    pattern="(a|approve)(?:\s|$)([\s\S]*)",
    command=("approve", plugin_category),
    info={
        "h": "To approve user to direct message you.",
        "u": [
            "{tr}a/approve <username/reply reason> in group",
            "{tr}a/approve <reason> in pm",
        ],
    },
)
async def approve_p_m(event):  # sourcery no-metrics
    "To approve user to pm"
    if gvar("pmpermit") is None:
        return await edl(
            event,
            f"__Turn on pmpermit by doing __`{tr}pmguard on` __for working of this plugin__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "Not mentioned"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(
            user.id, get_display_name(user), start_date, user.username, reason
        )
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edl(
            event,
            f"__Approved to pm__ [{user.first_name}](tg://user?id={user.id})\n**Reason:** __{reason}__",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.error(f"🚨 {str(e)}")
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edl(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __is already in approved list__",
        )


@doge.bot_cmd(
    pattern="(da|disapprove)(?:\s|$)([\s\S]*)",
    command=("disapprove", plugin_category),
    info={
        "h": "To disapprove user to direct message you.",
        "note": "This command works only for approved users",
        "o": {"all": "To disapprove all approved users"},
        "u": [
            "{tr}da/disapprove <username/reply> in group",
            "{tr}da/disapprove in pm",
            "{tr}da/disapprove all - To disapprove all users.",
        ],
    },
)
async def disapprove_p_m(event):
    "To disapprove user to direct message you."
    if gvar("pmpermit") is None:
        return await edl(
            event,
            f"__Turn on pmpermit by doing __`{tr}pmguard on` __for working of this plugin__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)

    else:
        reason = event.pattern_match.group(2)
        if reason != "all":
            user, reason = await get_user_from_event(event, secondgroup=True)
            if not user:
                return
    if reason == "all":
        pmpermit_sql.disapprove_all()
        return await edl(event, "__Ok! I have disapproved everyone successfully.__")
    if not reason:
        reason = "Not Mentioned."
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
        await eor(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __is disapproved to personal message me.__\n**Reason:**__ {reason}__",
        )
    else:
        await edl(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __is not yet approved__",
        )


@doge.bot_cmd(
    pattern="block(?:\s|$)([\s\S]*)",
    command=("block", plugin_category),
    info={
        "h": "To block user to direct message you.",
        "u": [
            "{tr}block <username/reply reason> in group",
            "{tr}block <reason> in pm",
        ],
    },
)
async def block_p_m(event):
    "To block user to direct message you."
    if gvar("pmpermit") is None:
        return await edl(
            event,
            f"__Turn on pmpermit by doing __`{tr}pmguard on` __for working of this plugin__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(user.id) in PM_WARNS:
        del PM_WARNS[str(user.id)]
    if str(user.id) in PMMESSAGE_CACHE:
        try:
            await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
        except Exception as e:
            LOGS.error(f"🚨 {str(e)}")
        del PMMESSAGE_CACHE[str(user.id)]
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    await event.client(BlockRequest(user.id))
    await edl(
        event,
        f"[{user.first_name}](tg://user?id={user.id}) __is blocked, he can no longer personal message you.__\n**Reason:** __{reason}__",
    )


@doge.bot_cmd(
    pattern="unblock(?:\s|$)([\s\S]*)",
    command=("unblock", plugin_category),
    info={
        "h": "To unblock a user.",
        "u": [
            "{tr}unblock <username/reply reason> in group",
            "{tr}unblock <reason> in pm",
        ],
    },
)
async def unblock_pm(event):
    "To unblock a user."
    if gvar("pmpermit") is None:
        return await edl(
            event,
            f"__Turn on pmpermit by doing __`{tr}pmguard on` __for working of this plugin__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    await event.client(UnblockRequest(user.id))
    await event.edit(
        f"[{user.first_name}](tg://user?id={user.id}) __is unblocked he/she can personal message you from now on.__\n**Reason:** __{reason}__"
    )


@doge.bot_cmd(
    pattern="l(ist)?a(pproved)?$",
    command=("listapproved", plugin_category),
    info={
        "h": "To see list of approved users.",
        "u": [
            "{tr}listapproved",
        ],
    },
)
async def approve_p_m(event):
    "To see list of approved users."
    if gvar("pmpermit") is None:
        return await edl(
            event,
            f"__Turn on pmpermit by doing __`{tr}pmguard on` __to work this plugin__",
        )
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "**Current Approved PMs**\n\n"
    if len(approved_users) > 0:
        for user in approved_users:
            APPROVED_PMs += f"• 👤 {_format.mentionuser(user.first_name, user.user_id)}\n**ID:** `{user.user_id}`\n**UserName:** @{user.username}\n**Date:** __{user.date}__\n**Reason:** __{user.reason}__\n\n"
    else:
        APPROVED_PMs = "`You haven't approved anyone yet`"
    await eor(
        event,
        APPROVED_PMs,
        file_name="approvedpms.txt",
        caption="`Current Approved PMs`",
    )
