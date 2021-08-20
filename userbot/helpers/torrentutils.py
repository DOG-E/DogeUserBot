from math import floor
from os import path, makedirs, getcwd
from asyncio import sleep
from subprocess import PIPE, Popen

from aria2p import API, Client
from requests import get

from ..Config import Config
from ..core.logger import logging
from . import humanbytes

LOGS = logging.getLogger(__name__)


def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        return
    return talk


# Get best trackers for improved download speeds, thanks K-E-N-W-A-Y.
trackers_list = get(
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
).text.replace("\n\n", ",")

trackers = f"[{trackers_list}]"

cmd = f"aria2c \
--enable-rpc \
--rpc-listen-all=false \
--rpc-listen-port 8210 \
--max-connection-per-server=10 \
--rpc-max-request-size=1024M \
--check-certificate=false \
--bt-max-peers=0 \
--follow-torrent=mem \
--seed-time=0.01 \
--max-upload-limit=5K \
--max-concurrent-downloads=5 \
--min-split-size=10M \
--follow-torrent=mem \
--split=10 \
--bt-tracker={trackers} \
--daemon=true \
--allow-overwrite=true"

subprocess_run(cmd)

if not path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

download_path = path.join(getcwd(), Config.TMP_DOWNLOAD_DIRECTORY)

aria2 = API(Client(host="http://localhost", port=8210, secret=""))

aria2.set_global_options({"dir": download_path})


async def check_metadata(gid):
    t_file = aria2.get_download(gid)
    new_gid = t_file.followed_by_ids[0]
    LOGS.info("Changing GID " + gid + " to" + new_gid)
    return new_gid


async def check_progress_for_dl(gid, event, previous):  # sourcery no-metrics
    complete = None
    while not complete:
        t_file = aria2.get_download(gid)
        complete = t_file.is_complete
        try:
            if not complete and not t_file.error_message:
                percentage = int(t_file.progress)
                downloaded = percentage * int(t_file.total_length) / 100
                prog_str = "Downloading | [{0}{1}] {2}".format(
                    "".join(
                        Config.FINISHED_PROGRESS_STR
                        for i in range(floor(percentage / 10))
                    ),
                    "".join(
                        Config.UNFINISHED_PROGRESS_STR
                        for i in range(10 - floor(percentage / 10))
                    ),
                    t_file.progress_string(),
                )
                msg = (
                    f"**Name**: `{t_file.name}`\n"
                    f"**Status** -> `{t_file.status.capitalize()}`\n"
                    f"`{prog_str}`\n"
                    f"`{humanbytes(downloaded)} of {t_file.total_length_string()}"
                    f"@ {t_file.download_speed_string()}`\n"
                    f"**ETA** -> {t_file.eta_string()}\n"
                )
                if msg != previous:
                    await event.edit(msg)
                    previous = msg
            else:
                await event.edit(f"`{msg}`")
            await sleep(5)
            await check_progress_for_dl(gid, event, previous)
            t_file = aria2.get_download(gid)
            complete = t_file.is_complete
            if complete:
                return await event.edit(
                    f"**Name:** `{t_file.name}`\n"
                    f"**Size:** `{t_file.total_length_string()}`\n"
                    f"**Path:** `{path.join(Config.TMP_DOWNLOAD_DIRECTORY , t_file.name)}`\n"
                    "**Response:** __OK - Successfully downloaded...__"
                )
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                if "Your Torrent/Link is Dead." not in event.text:
                    await event.edit(f"**Download Canceled:**\n`{t_file.name}`")
            elif "depth exceeded" in str(e):
                t_file.remove(force=True)
                await event.edit(
                    f"**Download Auto Canceled:**\n`{t_file.name}`\nYour Torrent/Link is Dead."
                )
