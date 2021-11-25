# Button post maker thanks to uniborg for the base
# Credits: @sandy1709 (@mrconfused)
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import remove
from re import compile

from . import BOT_USERNAME, doge, edl, ibuild_keyboard, reply_id, tr

plugin_category = "tool"
# Regex obtained from: https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
BTN_URL_REGEX = compile(r"(\[([^\[]+?)\]\<(?:/{0,2})(.+?)(:same)?\>)")


@doge.bot_cmd(
    pattern="bbutton(?:\s|$)([\s\S]*)",
    command=("bbutton", plugin_category),
    info={
        "header": "To create button posts.",
        "note": f"For working of this you need your bot ({BOT_USERNAME}) in the group/channel where you're using and Markdown is default to HTML.",
        "options": "If you button to be in same row as other button then follow this (link:same) in 2nd button.",
        "usage": f"{tr}bbutton <text> [Name on button](link you want to open)",
        "examples": f"{tr}bbutton Test [🔎 Google]<https://www.google.com> [🐶 Doge UserBot]<https://t.me/DogeUserBot:same> [🐾 Support]<https://t.me/DogeSup>",
    },
)
async def bbutton(event):
    "To create button posts."
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edl(event, "`🔲 What text should I use in button post?`")

    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        if n_escapes % 2 == 0:
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        elif n_escapes % 2 == 1:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
        else:
            break
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip() or None
    tl_ib_buttons = ibuild_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message and reply_message.media:
        tgbot_reply_message = await event.client.download_media(reply_message.media)
    if tl_ib_buttons == []:
        tl_ib_buttons = None
    await event.client.tgbot.send_message(
        entity=event.chat_id,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
    )
    await event.delete()
    if tgbot_reply_message:
        remove(tgbot_reply_message)


@doge.bot_cmd(
    pattern="button(?:\s|$)([\s\S]*)",
    command=("button", plugin_category),
    info={
        "header": "To create button posts via inline.",
        "note": "Markdown is default to HTML.",
        "options": "If you button to be in same row as other button then follow this (link:same) in 2nd button.",
        "usage": f"{tr}button <text> [Name on button](link you want to open)",
        "examples": f"{tr}button Test [🔎 Google]<https://www.google.com> [🐶 Doge UserBot]<https://t.me/DogeUserBot:same> [🐾 Support]<https://t.me/DogeSup>",
    },
)
async def button(event):
    "To create button posts via inline."
    reply_to_id = await reply_id(event)
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edl(event, "`🔲 What text should I use in button post?`")

    doginput = "Inline buttons " + markdown_note
    results = await event.client.inline_query(BOT_USERNAME, doginput)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()
