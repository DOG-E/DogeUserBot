
from asyncio import sleep
from re import findall

from bs4 import BeautifulSoup
from requests import get

from . import edl, eor, doge, logging, lan, aria2, check_metadata, check_progress_for_dl, subprocess_run, paste_links

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}


@doge.bot_cmd(
    pattern="fromurl(?:\s|$)([\s\S]*)",
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
    dogevent = await eor(event, lan("processing"))
    await check_progress_for_dl(gid=gid, event=dogevent, previous=None)
    t_file = aria2.get_download(gid)
    if t_file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, event=dogevent, previous=None)


@doge.bot_cmd(
    pattern="amag(?:\s|$)([\s\S]*)",
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
    dogevent = await eor(event, lan("processing"))
    await check_progress_for_dl(gid=gid, event=dogevent, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=dogevent, previous=None)


@doge.bot_cmd(
    pattern="ator(?:\s|$)([\s\S]*)",
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
    reply = await event.get_reply_message()
    if not torrent_file_path and reply and reply.media:
        torrent_file_path = await reply.download_media()
    if not torrent_file_path:
        return await edl(event,"__Provide either path of file or reply to .torrent files.__")
    try:
        print(torrent_file_path)
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None
        )
    except Exception as e:
        return await edl(event, f"**Error :**\n`{str(e)}`", time=15)
    gid = download.gid
    dogevent = await eor(event, lan("processing"))
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
    await eor(event,"`Clearing on-going downloads... `")
    await sleep(2.5)
    await eor(event,"`Successfully cleared all downloads.`")


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


@doge.bot_cmd(
    pattern="tsearch(?:\s|$)([\s\S]*)",
    command=("tsearch", plugin_category),
    info={
        "header": "To search torrents.",
        "flags": {".l": "for number of search results to check."},
        "usage": "{tr}tsearch <query>",
        "examples": ["{tr}tsearch avatar", "{tr}tsearch .l5 avatar"],
    },
)
async def tor_search(event):  # sourcery no-metrics
    """
    To search torrents
    """
    search_str = event.pattern_match.group(1)
    lim = findall(r".l\d+", search_str)
    try:
        lim = lim[0]
        lim = lim.replace(".l", "")
        search_str = search_str.replace(".l" + lim, "")
        lim = int(lim)
        if lim < 1 or lim > 20:
            lim = 10
    except IndexError:
        lim = 10
    dogevent = await eor(
        event, f"`Searching torrents for " + search_str + ".....`"
    )
    if " " in search_str:
        search_str = search_str.replace(" ", "+")
        res = get(
            "https://www.torrentdownloads.me/search/?new=1&s_doge=0&search="
            + search_str,
            headers,
        )
    else:
        res = get(
            "https://www.torrentdownloads.me/search/?search=" + search_str, headers
        )
    source = BeautifulSoup(res.text, "lxml")
    urls = []
    magnets = []
    titles = []
    counter = 0
    lim = lim+2
    for div in source.find_all("div", {"class": "grey_bar3 back_none"}):
        try:
            title = div.p.a["title"]
            title = title[20:]
            titles.append(title)
            urls.append("https://www.torrentdownloads.me" + div.p.a["href"])
        except (KeyError, TypeError, AttributeError):
            pass
        except Exception as e:
            return await edl(
                dogevent, f"**Error while doing torrent search:**\n{str(e)}"
            )
        if counter == lim:
            break
        counter += 1
    if not urls:
        return await edl(
            dogevent, "__Either the query was restricted or not found..__"
        )
    for url in urls:
        res = get(url, headers)
        source = BeautifulSoup(res.text, "lxml")
        for div in source.find_all("div", {"class": "grey_bar1 back_none"}):
            try:
                mg = div.p.a["href"]
                magnets.append(mg)
            except TypeError:
                pass
            except Exception as e:
                LOGS.info(str(e))
    if not magnets:
        return await edl(dogevent, "__Unable to fetch magnets.__")
    shorted_links = await paste_links(magnets)
    if shorted_links is None:
        return await edl(dogevent, "__Unable to fetch results.__")
    msg = f"**Torrent Search Query**\n`{search_str.replace('+', ' ')}`\n**Results**\n"
    counter = 0
    while counter != len(shorted_links):
        msg += f"⁍ [{titles[counter]}]({shorted_links[counter]})\n\n"
        counter += 1
    await dogevent.edit(msg, link_preview=False)
