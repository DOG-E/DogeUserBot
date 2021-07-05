# Credits to @jisan7509 (@jisan09)
#
# Forked, developed and edited for @DogeUserbot
#
import os

from telethon.errors.rpcerrorlist import YouBlockedUserError

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import asciiart, lines50art, clippyart
from . import _dogetools, doge, convert_toimage, mention, reply_id

plugin_category = "extra"


@doge.ub(
    pattern="iascii ?([\s\S]*)",
    command=("iascii", plugin_category),
    info={
        "header": "Convert media to ascii art.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into ascii.",
        "usage": [
            "{tr}iascii <reply to a media>",
        ],
    },
)
async def horny(event):
    "Make a media to ascii art"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    dogevent = await edit_or_reply(event, "```Wait making ASCII...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "DogeUserBot.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/DogeUserBot.jpg")
    await asciiart(event.client, output_file, event.chat_id, c_id)
    if os.path.exists(output_file):
        os.remove(output_file)


@doge.ub(
    pattern="line ?([\s\S]*)",
    command=("line", plugin_category),
    info={
        "header": "Convert media to line image.",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into line image.",
        "usage": [
            "{tr}line <reply to a media>",
        ],
    },
)
async def pussy(event):
    "Make a media to line image"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    dogevent = await edit_or_reply(event, "```Processing...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "DogeUserBot.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/DogeUserBot.jpg")
    await lines50art(event.client, output_file, event.chat_id, c_id)
    if os.path.exists(output_file):
        os.remove(output_file)


@doge.ub(
    pattern="clip ?([\s\S]*)",
    command=("clip", plugin_category),
    info={
        "header": "Convert media to sticker by clippy",
        "description": "Reply to any media files like pic, gif, sticker, video and it will convert into sticker by clippy.",
        "usage": [
            "{tr}clip <reply to a media>",
        ],
    },
)
async def fck(event):
    "Make a media to clippy sticker"
    reply_message = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply_message.media:
        return await edit_delete(event, "```Reply to a media file...```")
    dogevent = await edit_or_reply(event, "```Processing...```")
    c_id = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    output_file = os.path.join("./temp", "DogeUserBot.jpg")
    output = await _dogetools.media_to_pic(event, reply_message)
    outputt = convert_toimage(output[1], filename="./temp/DogeUserBot.jpg")
    await clippyart(event.client, output_file, event.chat_id, c_id)
    if os.path.exists(output_file):
        os.remove(output_file)
