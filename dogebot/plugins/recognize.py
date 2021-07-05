# credits: @Mr_Hops
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from dogebot import doge

from ..core.managers import edit_or_reply
from ..helpers.functions.functions import rekognitionb

plugin_category = "utils"


@doge.ub(
    pattern="recognize ?([\s\S]*)",
    command=("recognize", plugin_category),
    info={
        "header": "To recognize a image",
        "description": "Get information about an image using AWS Rekognition. Find out information including detected labels, faces. text and moderation tags",
        "usage": "{tr}recognize",
    },
)
async def _(event):
    "To recognize a image."
    if not event.reply_to_msg_id:
        return await edit_or_reply(event, "Reply to any user's media message.")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await edit_or_reply(event, "reply to media file")
    if reply_message.sender.bot:
        return await event.edit("Reply to actual users message.")
    await edit_or_reply(event, "recognizeing this media")

    await rekognitionb(event.client, event.chat_id, reply_message)
