"""
Telegram Channel Media Downloader Plugin for userbot.
usage: .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]
       .getc number_of_messsages channel_username
By: @Zero_cool7870
"""
from os import makedirs, path
from subprocess import PIPE, Popen, check_output

from . import Config, doge, eor, media_type

plugin_category = "tool"


@doge.bot_cmd(
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
    dogty = event.pattern_match.group(1)
    limit = int(dogty.split(" ")[0])
    channel_username = str(dogty.split(" ")[1])
    tempdir = path.join(Config.TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        makedirs(tempdir)
    except BaseException:
        pass
    event = await eor(event, "`Downloading Media From this Channel.`")
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
    ps = Popen(("ls", tempdir), stdout=PIPE)
    output = check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", " ")
    output = output.replace("\\n'", " ")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to tempdir"
    )


@doge.bot_cmd(
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
    tempdir = path.join(Config.TMP_DOWNLOAD_DIRECTORY, channel_username)
    try:
        makedirs(tempdir)
    except BaseException:
        pass
    event = await eor(event, "`Downloading All Media From this Channel.`")
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
    ps = Popen(("ls", tempdir), stdout=PIPE)
    output = check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit(
        f"Successfully downloaded {output} number of media files from {channel_username} to tempdir"
    )
