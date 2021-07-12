# torrent module for catuserbot
from asyncio import sleep

from userbot import doge

from ..core.logger import logging
from ..core.managers import edl, eor
from . import aria2, check_metadata, check_progress_for_dl, subprocess_run

LOGS = logging.getLogger(__name__)
plugin_category = "misc"


@doge.bot_cmd(
    pattern="fromurl(?: |$)(.*)",
    command=("fromurl", plugin_category),
    info={
        "header": "To get random quotes on given topic.",
        "description": "Downloads the file into your userbot server storage",
        "usage": "{tr}fromurl URL",
    },
)
async def aurl_download(event):
    "Add url Into Queue."
    uri = [event.pattern_match.group(1)]
    try:  # Add URL Into Queue
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        return await edl(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    dogevent = await eor(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=dogevent, previous=None)
    t_file = aria2.get_download(gid)
    if t_file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=dogevent, previous=None)


@doge.bot_cmd(
    pattern="amag(?: |$)(.*)",
    command=("amag", plugin_category),
    info={
        "header": "Add Magnet URI Into Queue",
        "description": "Downloads the file into your userbot server storage.",
        "usage": "{tr}amag <URL of torrent file>",
    },
)
async def magnet_download(event):
    "Add Magnet URI Into Queue"
    magnet_uri = event.pattern_match.group(1)
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        return await edl(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    dogevent = await eor(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=dogevent, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=dogevent, previous=None)


@doge.bot_cmd(
    pattern="ator(?: |$)(.*)",
    command=("ator", plugin_category),
    info={
        "header": "Add Torrent Into Queue",
        "description": "First download tor file using {tr}download cmd and then use that path for this cmd. This cmd will Download the file into your userbot server storage.",
        "usage": "{tr}ator <path to torrent file>",
    },
)
async def torrent_download(event):
    "Add Torrent Into Queue"
    torrent_file_path = event.pattern_match.group(1)
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await edl(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    dogevent = await eor(event, "`Processing......`")
    await check_progress_for_dl(gid=gid, event=dogevent, previous=None)


@doge.bot_cmd(
    pattern="aclear$",
    command=("aclear", plugin_category),
    info={
        "header": "Clear the aria Queue.",
        "description": "Clears the download queue, deleting all on-going downloads.",
        "usage": "{tr}aclear",
    },
)
async def remove_all(event):
    "Clear the aria Queue."
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge()
    except Exception as e:
        event = await eor(event, f"**Error :**\n`{str(e)}`")
        await sleep(5)
    if not removed:  # If API returns False Try to Remove Through System Call.
        subprocess_run("aria2p remove-all")
    await eor(event, "`Clearing on-going downloads... `")
    await sleep(2.5)
    await eor(event, "`Successfully cleared all downloads.`")


@doge.bot_cmd(
    pattern="apause$",
    command=("apause", plugin_category),
    info={
        "header": "Pause ALL Currently Running Downloads.",
        "description": "Pause on-going downloads.",
        "usage": "{tr}apause <topic>",
        "examples": "{tr}apause love",
    },
)
async def pause_all(event):
    "Pause ALL Currently Running Downloads."
    dogevent = await eor(event, "`Pausing downloads...`")
    aria2.pause_all(force=True)
    await sleep(2.5)
    await dogevent.edit("`Successfully paused on-going downloads.`")


@doge.bot_cmd(
    pattern="aresume$",
    command=("aresume", plugin_category),
    info={
        "header": "TResume ALL Currently Running Downloads..",
        "description": "Resumes on-going downloads.",
        "usage": "{tr}aresume",
    },
)
async def resume_all(event):
    "Resume ALL Currently Running Downloads."
    dogevent = await eor(event, "`Resuming downloads...`")
    aria2.resume_all()
    await sleep(1)
    await edl(dogevent, "`Downloads resumed.`")


@doge.bot_cmd(
    pattern="ashow$",
    command=("ashow", plugin_category),
    info={
        "header": "Shows current aria progress.",
        "description": "Shows progress of the on-going downloads.",
        "usage": "{tr}ashow",
    },
)
async def show_all(event):
    "Shows current aria progress of queue"
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = (
            msg
            + "**File: **`"
            + str(download.name)
            + "`\n**Speed : **"
            + str(download.download_speed_string())
            + "\n**Progress : **"
            + str(download.progress_string())
            + "\n**Total Size : **"
            + str(download.total_length_string())
            + "\n**Status : **"
            + str(download.status)
            + "\n**ETA : **"
            + str(download.eta_string())
            + "\n\n"
        )
    await eor(event, "**On-going Downloads: **\n" + msg)
