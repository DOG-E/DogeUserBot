# ported from paperplaneExtended by avinashreddy3108 for media support

from ..sql_helper.notes_sql import add_note, del_note, get_note, get_notes
from . import BOTLOG, BOTLOG_CHATID, doge, edl, eor, get_message_link, reply_id

plugin_category = "misc"


@doge.bot_cmd(
    pattern="\#(\S+)",
)
async def incom_note(event):
    if not BOTLOG:
        return
    try:
        if not (await event.get_sender()).bot:
            notename = event.text[1:]
            notename = notename.lower()
            note = get_note(notename)
            message_id_to_reply = await reply_id(event)
            if note:
                if note.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(note.f_mesg_id)
                    )
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        msg_o,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
                elif note.reply:
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        note.reply,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
    except AttributeError:
        pass


@doge.bot_cmd(
    pattern="note (\w*)",
    command=("note", plugin_category),
    info={
        "header": "To save notes to the bot.",
        "description": "Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!. and get them by using #notename",
        "usage": "{tr}note <keyword>",
    },
)
async def add_noter(event):
    "To save notes to bot."
    if not BOTLOG:
        return await edl(
            event, "`To save notes you need to set PRIVATE_GROUP_BOT_API_ID`"
        )
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    keyword = keyword.lower()
    if msg and not string:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#NOTE\
            \n**Keyword:** `#{keyword}`\
            \n\nThe following message is saved as the note in your bot, DON'T delete it!",
        )
        msg_o = await event.client.forward_messages(
            entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
        )
        msg_id = msg_o.id
    elif msg:
        return await edl(
            event,
            "`What should i save for your note either do reply or give note text along with keyword`",
        )
    if not msg:
        if string:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#NOTE\
            \n**Keyword:** `#{keyword}`\
            \n\nThe following message is saved as the note in your bot, DON'T delete it!",
            )
            msg_o = await event.client.send_message(BOTLOG_CHATID, string)
            msg_id = msg_o.id
            string = None
        else:
            return await edl(event, "`What should i save for your note?`")
    success = "Note {} is successfully {}. Use `#{}` to get it"
    if add_note(keyword, string, msg_id) is False:
        del_note(keyword)
        if add_note(keyword, string, msg_id) is False:
            return await eor(event, f"Error in saving the given note {keyword}")
        return await eor(event, success.format(keyword, "updated", keyword))
    return await eor(event, success.format(keyword, "added", keyword))


@doge.bot_cmd(
    pattern="notes$",
    command=("notes", plugin_category),
    info={
        "header": "To list all notes in bot.",
        "usage": "{tr}notes",
    },
)
async def on_note_list(event):
    "To list all notes in bot."
    message = "You haven't saved any notes."
    notes = get_notes()
    if not BOTLOG:
        return await edl(
            event, "`For saving note you must set PRIVATE_GROUP_BOT_API_ID`"
        )
    for note in notes:
        if message == "You haven't saved any notes.":
            message = "Notes saved in your bot are\n\n"
        message += f"👉 `#{note.keyword}`"
        if note.f_mesg_id:
            msglink = await get_message_link(BOTLOG_CHATID, note.f_mesg_id)
            message += f"  [preview]({msglink})\n"
        else:
            message += "  No preview\n"
    await eor(event, message)


@doge.bot_cmd(
    pattern="dnote (\S+)",
    command=("dnote", plugin_category),
    info={
        "header": "To delete paticular note in bot.",
        "usage": "{tr}dnote <keyword>",
    },
)
async def on_note_delete(event):
    "To delete paticular note in bot."
    name = event.pattern_match.group(1)
    name = name.lower()
    dognote = get_note(name)
    if dognote:
        del_note(name)
    else:
        return await eor(event, f"Are you sure that `#{name}` is saved as note?")
    await eor(event, f"Note `#{name}` deleted successfully!")
