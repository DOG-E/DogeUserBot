# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.import os
#
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import os

from userbot import doge

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _dogeutils, reply_id
from . import make_gif

plugin_category = "utils"


@doge.ub(
    pattern="collage(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    dogeinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    dogeid = await reply_id(event)
    event = await edit_or_reply(
        event, "```collaging this may take several minutes too..... 😁```"
    )
    if not (reply and (reply.media)):
        await event.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    dogesticker = await reply.download_media(file="./temp/")
    if not dogesticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(dogesticker)
        await event.edit("`Media format is not supported...`")
        return
    if dogeinput:
        if not dogeinput.isdigit():
            os.remove(dogesticker)
            await event.edit("`You input is invalid, check help`")
            return
        dogeinput = int(dogeinput)
        if not 0 < dogeinput < 10:
            os.remove(dogesticker)
            await event.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        dogeinput = 3
    if dogesticker.endswith(".tgs"):
        hmm = await make_gif(event, dogesticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(dogesticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = dogesticker
    endfile = "./temp/collage.png"
    dogecmd = f"vcsi -g {dogeinput}x{dogeinput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _dogeutils.runcmd(dogecmd))[:2]
    if not os.path.exists(endfile):
        for files in (dogesticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            event, f"`media is not supported or try with smaller grid size`", 5
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=dogeid,
    )
    await event.delete()
    for files in (dogesticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
