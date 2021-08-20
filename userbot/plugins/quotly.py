"""
imported from nicegrill
modified by @mrconfused
QuotLy: Avaible commands: .qbot
"""
from io import BytesIO
from os import path, remove
from re import findall
from textwrap import wrap

from PIL.Image import new as Imnew
from PIL.Image import open as Imopen
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from requests import get
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.events import NewMessage
from telethon.tl.functions.contacts import UnblockRequest
from telethon.utils import get_display_name

from . import (
    _dogetools,
    convert_tosticker,
    doge,
    edl,
    eor,
    get_warp_length,
    logging,
    media_type,
    process,
    reply_id,
)

plugin_category = "fun"
LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "userbot/helpers/resources/fonts/spacemono_regular.ttf"


@doge.bot_cmd(
    pattern="qpic(?:\s|$)([\s\S]*)",
    command=("qpic", plugin_category),
    info={
        "header": "Makes quote pic.",
        "flags": {
            "-b": "To get black and white output.",
            "-s": "To output file as sticker",
        },
        "usage": "{tr}qpic <flag> <input/reply to text msg>",
        "examples": ["{tr}qpic DogeUserBot.", "{tr}qpic -b DogeUserBot."],
    },
)
async def q_pic(event):  # sourcery no-metrics
    args = event.pattern_match.group(1)
    black = findall(r"-b", args)
    sticker = findall(r"-s", args)
    args = args.replace("-b", "")
    args = args.replace("-s", "")
    input_str = args.strip()
    pfp = None
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    if reply and input_str or not reply and input_str:
        text = input_str
    elif reply and reply.raw_text:
        text = reply.raw_text
    else:
        return await edl(
            event, "__Provide input along with cmd or reply to text message.__"
        )
    dogevent = await eor(event, "__Making Quote pic....__")
    mediatype = media_type(reply)
    if (
        (not reply)
        or (not mediatype)
        or (mediatype not in ["Photo", "Sticker"])
        or (
            mediatype == "Sticker"
            and reply.document.mime_type == "application/i-tgsticker"
        )
    ):
        user = reply.sender_id if reply else event.client.uid
        pfp = await event.client.download_profile_photo(user)
    else:
        imag = await _dogetools.media_to_pic(event, reply, noedits=True)
        if imag[1] is None:
            return await edl(
                imag[0], "__Unable to extract image from the replied message.__"
            )
        user = event.client.uid
        pfp = imag[1]
    try:
        user = await event.client.get_entity(user)
    except Exception as e:
        LOGS.info(str(e))
        user = None
    if not pfp:
        pfp = "profilepic.jpg"
        with open(pfp, "wb") as f:
            f.write(get("https://telegra.ph/file/1fd74fa4a4dbf1655f3ec.jpg").content)
    text = "\n".join(wrap(text, 25))
    text = "“" + text + "„"
    font = truetype(FONT_FILE_TO_USE, 50)
    img = Imopen(pfp)
    if black:
        img = img.convert("L")
    img = img.convert("RGBA").resize((1024, 1024))
    w, h = img.size
    nw, nh = 20 * (w // 100), 20 * (h // 100)
    nimg = Imnew("RGBA", (w - nw, h - nh), (0, 0, 0))
    nimg.putalpha(150)
    img.paste(nimg, (nw // 2, nh // 2), nimg)
    draw = Draw(img)
    tw, th = draw.textsize(text=text, font=font)
    x, y = (w - tw) // 2, (h - th) // 2
    draw.text((x, y), text=text, font=font, fill="#ffffff", align="center")
    if user is not None:
        credit = "\n".join(
            wrap(f"by {get_display_name(user)}", int(get_warp_length(w / 2.5)))
        )
        tw, th = draw.textsize(text=credit, font=font)
        draw.text(
            ((w - nw + tw) // 1.6, (h - nh - th)),
            text=credit,
            font=font,
            fill="#ffffff",
            align="left",
        )
    output = BytesIO()
    if sticker:
        output.name = "DogeUserBot.Webp"
        img.save(output, "webp")
    else:
        output.name = "DogeUserBot.png"
        img.save(output, "PNG")
    output.seek(0)
    await event.client.send_file(event.chat_id, output, reply_to=reply_to)
    await dogevent.delete()
    for i in [pfp]:
        if path.lexists(i):
            remove(i)


@doge.bot_cmd(
    pattern="q(?:\s|$)([\s\S]*)",
    command=("q", plugin_category),
    info={
        "header": "Makes your message as sticker quote.",
        "usage": "{tr}q",
    },
)
async def stickerchat(dogquotes):
    "Makes your message as sticker quote"
    reply = await dogquotes.get_reply_message()
    if not reply:
        return await eor(dogquotes, "`I can't quote the message . reply to a message`")
    fetchmsg = reply.message
    repliedreply = None
    mediatype = media_type(reply)
    if mediatype and mediatype in ["Photo", "Round Video", "Gif"]:
        return await eor(dogquotes, "`Replied message is not supported now`")
    dogevent = await eor(dogquotes, "`Making quote...`")
    user = (
        await dogquotes.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, dogmsg = await process(fetchmsg, user, dogquotes.client, reply, repliedreply)
    if not res:
        return
    outfi = path.join("./temp", "sticker.png")
    dogmsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await dogquotes.client.send_file(dogquotes.chat_id, endfi, reply_to=reply)
    await dogevent.delete()
    remove(endfi)


@doge.bot_cmd(
    pattern="rq(?:\s|$)([\s\S]*)",
    command=("rq", plugin_category),
    info={
        "header": "Makes your message along with the previous replied message as sticker quote",
        "usage": "{tr}rq",
    },
)
async def stickerchat(dogquotes):
    "To make sticker message."
    reply = await dogquotes.get_reply_message()
    if not reply:
        return await eor(dogquotes, "`I can't quote the message . reply to a message`")
    fetchmsg = reply.message
    repliedreply = await reply.get_reply_message()
    mediatype = media_type(reply)
    if mediatype and mediatype in ["Photo", "Round Video", "Gif"]:
        return await eor(dogquotes, "`Replied message is not supported now`")
    dogevent = await eor(dogquotes, "`Making quote...`")
    user = (
        await dogquotes.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, dogmsg = await process(fetchmsg, user, dogquotes.client, reply, repliedreply)
    if not res:
        return
    outfi = path.join("./temp", "sticker.png")
    dogmsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await dogquotes.client.send_file(dogquotes.chat_id, endfi, reply_to=reply)
    await dogevent.delete()
    remove(endfi)


@doge.bot_cmd(
    pattern="qbot(?:\s|$)([\s\S]*)",
    command=("qbot", plugin_category),
    info={
        "header": "Makes your message as sticker quote by @quotlybot",
        "usage": "{tr}qbot",
    },
)
async def _(event):
    "Makes your message as sticker quote by @quotlybot"
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    message = ""
    messages_id = []
    if reply:
        if input_str and input_str.isnumeric():
            messages_id.append(reply.id)
            async for message in event.client.iter_messages(
                event.chat_id,
                limit=(int(input_str) - 1),
                offset_id=reply.id,
                reverse=True,
            ):
                if message.id != event.id:
                    messages_id.append(message.id)
        elif input_str:
            message = input_str
        else:
            messages_id.append(reply.id)
    elif input_str:
        message = input_str
    else:
        return await edl(
            event, "`Either reply to message or give input to function properly`"
        )
    chat = "@QuotLyBot"
    dogevent = await eor(event, "```Making a Quote```")
    async with event.client.conversation(chat) as conv:
        response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
        try:
            if messages_id != []:
                await event.client.forward_messages(chat, messages_id, event.chat_id)
            elif message != "":
                await event.client.send_message(conv.chat_id, message)
            else:
                return await edl(dogevent, "`I guess you have used a invalid syntax`")
        except YouBlockedUserError:
            await event.client(UnblockRequest(chat))
            if messages_id != []:
                await event.client.forward_messages(chat, messages_id, event.chat_id)
            elif message != "":
                await event.client.send_message(conv.chat_id, message)
            else:
                return await edl(dogevent, "`I guess you have used a invalid syntax`")
        response = await response
        await event.client.send_read_acknowledge(conv.chat_id)
        await dogevent.delete()
        await event.client.send_message(
            event.chat_id, response.message, reply_to=reply_to
        )
        await conv.mark_read()
        await conv.cancel_all()
