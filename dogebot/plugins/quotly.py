# imported from nicegrill
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import io
import os
import re
import textwrap
from textwrap import wrap

import requests
from PIL import Image, ImageDraw, ImageFont
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.utils import get_display_name

from dogebot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging
from ..helpers import convert_tosticker, media_type, process
from ..helpers.utils import _dogetools, reply_id

LOGS = logging.getLogger(__name__)
FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

plugin_category = "fun"


def get_warp_length(width):
    return int((20.0 / 1024.0) * (width + 0.0))


@doge.ub(
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
    black = re.findall(r"-b", args)
    sticker = re.findall(r"-s", args)
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
        return await edit_delete(
            event, "__Provide input along with cmd or reply to text message.__"
        )
    dogevent = await edit_or_reply(event, "__Making Quote pic....__")
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
            return await edit_delete(
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
            f.write(
                requests.get(
                    "https://telegra.ph/file/1fd74fa4a4dbf1655f3ec.jpg"
                ).content
            )
    text = "\n".join(textwrap.wrap(text, 25))
    text = "“" + text + "„"
    font = ImageFont.truetype(FONT_FILE_TO_USE, 50)
    img = Image.open(pfp)
    if black:
        img = img.convert("L")
    img = img.convert("RGBA").resize((1024, 1024))
    w, h = img.size
    nw, nh = 20 * (w // 100), 20 * (h // 100)
    nimg = Image.new("RGBA", (w - nw, h - nh), (0, 0, 0))
    nimg.putalpha(150)
    img.paste(nimg, (nw // 2, nh // 2), nimg)
    draw = ImageDraw.Draw(img)
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
    output = io.BytesIO()
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
        if os.path.lexists(i):
            os.remove(i)


@doge.ub(
    pattern="q(?:\s|$)([\s\S]*)",
    command=("q", plugin_category),
    info={
        "header": "Makes your message as sticker quote.",
        "usage": "{tr}q",
    },
)
async def stickerchat(dogequotes):
    "Makes your message as sticker quote"
    reply = await dogequotes.get_reply_message()
    if not reply:
        return await edit_or_reply(
            dogequotes, "`I cant quote the message . reply to a message`"
        )
    fetchmsg = reply.message
    repliedreply = None
    if reply.media and reply.media.document.mime_type in ("mp4"):
        return await edit_or_reply(dogequotes, "`this format is not supported now`")
    dogevent = await edit_or_reply(dogequotes, "`Making quote...`")
    user = (
        await dogequotes.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, dogemsg = await process(fetchmsg, user, dogequotes.client, reply, repliedreply)
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    dogemsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await dogequotes.client.send_file(dogequotes.chat_id, endfi, reply_to=reply)
    await dogevent.delete()
    os.remove(endfi)


@doge.ub(
    pattern="rq(?:\s|$)([\s\S]*)",
    command=("rq", plugin_category),
    info={
        "header": "Makes your message along with the previous replied message as sticker quote",
        "usage": "{tr}rq",
    },
)
async def stickerchat(dogequotes):
    "To make sticker message."
    reply = await dogequotes.get_reply_message()
    if not reply:
        return await edit_or_reply(
            dogequotes, "`I cant quote the message . reply to a message`"
        )
    fetchmsg = reply.message
    repliedreply = await reply.get_reply_message()
    if reply.media and reply.media.document.mime_type in ("mp4"):
        return await edit_or_reply(dogequotes, "`this format is not supported now`")
    dogevent = await edit_or_reply(dogequotes, "`Making quote...`")
    user = (
        await dogequotes.client.get_entity(reply.forward.sender)
        if reply.fwd_from
        else reply.sender
    )
    res, dogemsg = await process(fetchmsg, user, dogequotes.client, reply, repliedreply)
    if not res:
        return
    outfi = os.path.join("./temp", "sticker.png")
    dogemsg.save(outfi)
    endfi = convert_tosticker(outfi)
    await dogequotes.client.send_file(dogequotes.chat_id, endfi, reply_to=reply)
    await dogevent.delete()
    os.remove(endfi)


@doge.ub(
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
        return await edit_delete(
            event, "`Either reply to message or give input to function properly`"
        )
    dogevent = await edit_or_reply(event, "```Making a Quote```")
    chat = "@QuotLyBot"
    async with event.client.conversation(chat) as conv:
        try:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=chat)
                )
                if messages_id != []:
                    await event.client.forward_messages(chat, messages_id, event.chat_id)
                elif message != "":
                    await event.client.send_message(conv.chat_id, message)
                else:
                    return await edit_delete(
                        dogevent, "`I guess you have used a invalid syntax`"
                    )
            except YouBlockedUserError:
                event.client(UnblockRequest(chat))
                await dogevent.edit("**⛔ You've previously blocked @QuotLyBot!\
                    \n🔔 I unblocked @QuotLyBot and I'm trying again.**")
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=chat)
                )
                if messages_id != []:
                    await event.client.forward_messages(chat, messages_id, event.chat_id)
                elif message != "":
                    await event.client.send_message(conv.chat_id, message)
                else:
                    return await edit_delete(
                        dogevent, "`I guess you have used a invalid syntax`"
                    )
            
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
            await dogevent.delete()
            await event.client.send_message(
                event.chat_id, response.message, reply_to=reply_to
            )
        except:
            return await edit_delete(dogevent, "**🔔 Something went wrong!**")
