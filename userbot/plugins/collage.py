# collage plugin for catuserbot by @sandy1709

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.import os

import os

from userbot import doge

from ..core.managers import edl, eor
from ..helpers import _dogeutils, reply_id
from . import make_gif

plugin_category = "utils"


@doge.bot_cmd(
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
    doginput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    dogid = await reply_id(event)
    event = await eor(
        event, "```collaging this may take several minutes too..... 😁```"
    )
    if not (reply and (reply.media)):
        await event.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    dogsticker = await reply.download_media(file="./temp/")
    if not dogsticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(dogsticker)
        await event.edit("`Media format is not supported...`")
        return
    if doginput:
        if not doginput.isdigit():
            os.remove(dogsticker)
            await event.edit("`You input is invalid, check help`")
            return
        doginput = int(doginput)
        if not 0 < doginput < 10:
            os.remove(dogsticker)
            await event.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        doginput = 3
    if dogsticker.endswith(".tgs"):
        hmm = await make_gif(event, dogsticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(dogsticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = dogsticker
    endfile = "./temp/collage.png"
    dogecmd = f"vcsi -g {doginput}x{doginput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _dogeutils.runcmd(dogecmd))[:2]
    if not os.path.exists(endfile):
        for files in (dogsticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edl(
            event, f"`media is not supported or try with smaller grid size`", 5
        )
    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=dogid,
    )
    await event.delete()
    for files in (dogsticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)
