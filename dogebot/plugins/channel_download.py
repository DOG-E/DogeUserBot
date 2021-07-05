# Credit: @Zero_cool7870
#
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import os
import subprocess

from ..Config import Config
from . import doge, edit_or_reply

plugin_category = "tools"


@doge.ub(
    pattern="getc(?:\s|$)([\s\S]*)",
    command=("getc", plugin_category),
    info={
        "header": "To download channel media files",
        "description": "pass username and no of latest messages to check to command \
             so the bot will download media files from that latest no of messages to server ",
        "usage": "{tr}getc count channel_username",
        "examples": "{tr}getc 10 @DogeUserBot",
    },
)
async def get_media(event):
    dogety = event.pattern_match.group(1)
    limit = int(dogety.split(" ")[0])
    channel_username = str(dogety.split(" ")[1])
    tempdir = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        os.makedirs(tempdir)
    except BaseException:
        pass
    event = await edit_or_reply(event, "`Downloading Media From this Channel.`")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", tempdir), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", " ")
    output = output.replace("\\n'", " ")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to tempdir"
    )


@doge.ub(
    pattern="geta(?:\s|$)([\s\S]*)",
    command=("geta", plugin_category),
    info={
        "header": "To download channel all media files",
        "description": "pass username to command so the bot will download all media files from that latest no of messages to server ",
        "note": "there is limit of 3000 messages for this process to prevent API limits. that is will download all media files from latest 3000 messages",
        "usage": "{tr}geta channel_username",
        "examples": "{tr}geta @DogeUserBot",
    },
)
async def get_media(event):
    channel_username = event.pattern_match.group(1)
    tempdir = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        os.makedirs(tempdir)
    except BaseException:
        pass
    event = await edit_or_reply(event, "`Downloading All Media From this Channel.`")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    i = 0
    for msg in msgs:
        mediatype = media_type(msg)
        if mediatype is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", tempdir), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to tempdir"
    )
