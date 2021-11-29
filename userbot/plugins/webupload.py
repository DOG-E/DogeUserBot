# Ported from https://github.com/Total-Noob-69/X-tra-Telegram/blob/master/userbot/plugins/webupload.py
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import dumps, loads
from os import path, remove
from re import DOTALL, compile, findall
from subprocess import STDOUT, CalledProcessError, check_output

from requests import post

from . import TMP_DOWNLOAD_DIRECTORY, _dogeutils, doge, eor, logging

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

link_regex = compile(
    "((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", DOTALL
)


@doge.bot_cmd(
    pattern="labstack(?:\s|$)([\s\S]*)",
    command=("labstack", plugin_category),
    info={
        "h": "To upload media to labstack.",
        "d": "Will upload media to labstack and shares you link so that you can share with friends and it expires automatically after 7 days",
        "u": "{tr}labstack <reply to media or provide path of media>",
    },
)
async def labstack(event):
    "to upload media to labstack"
    editor = await eor(event, "**⏳ Processing...**")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filebase = input_str
    elif reply:
        filebase = await event.client.download_media(
            reply.media, TMP_DOWNLOAD_DIRECTORY
        )
    else:
        return await editor.edit(
            "Reply to a media file or provide a directory to upload the file to labstack"
        )
    filesize = path.getsize(filebase)
    filename = path.basename(filebase)
    headers2 = {"Up-User-ID": "IZfFbjUcgoo3Ao3m"}
    files2 = {
        "ttl": 604800,
        "files": [{"name": filename, "type": "", "size": filesize}],
    }
    r2 = post("https://up.labstack.com/api/v1/links", json=files2, headers=headers2)
    r2json = loads(r2.text)

    url = "https://up.labstack.com/api/v1/links/{}/send".format(r2json["code"])
    max_days = 7
    command_to_exec = [
        "curl",
        "-F",
        "files=@" + filebase,
        "-H",
        "Transfer-Encoding: chunked",
        "-H",
        "Up-User-ID: IZfFbjUcgoo3Ao3m",
        url,
    ]
    try:
        t_response = check_output(command_to_exec, stderr=STDOUT)
    except CalledProcessError as exc:
        LOGS.info("Status: FAIL", exc.returncode, exc.output)
        return await editor.edit(exc.output.decode("UTF-8"))
    else:
        LOGS.info(t_response)
        t_response_arry = "https://up.labstack.com/api/v1/links/{}/receive".format(
            r2json["code"]
        )
    await editor.edit(
        t_response_arry + "\nMax Days:" + str(max_days), link_preview=False
    )


@doge.bot_cmd(
    pattern="webupload ?(.+?|) --(fileio|anonfiles|transfer|filebin|anonymousfiles|bayfiles)",
    command=("webupload", plugin_category),
    info={
        "h": "To upload media to some online media sharing platforms.",
        "d": "you can upload media to any of the sites mentioned. so you can share link to others.",
        "o": {
            "fileio": "to file.io site",
            "anonfiles": "to anonfiles site",
            "transfer": "to transfer.sh site",
            "filebin": "to file bin site",
            "anonymousfiles": "to anonymousfiles site",
            "bayfiles": "to bayfiles site",
        },
        "u": [
            "{tr}webupload --option",
            "{tr}webupload path --option",
        ],
        "e": "{tr}.webupload --fileio reply this to media file.",
    },
)
async def _(event):
    "To upload media to some online media sharing platforms"
    editor = await eor(event, "**⏳ Processing...**")
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    dogecheck = None
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await event.client.download_media(
            reply.media, TMP_DOWNLOAD_DIRECTORY
        )
        dogecheck = True
    CMD_WEB = {
        "fileio": 'curl -F "file=@{full_file_path}" https://file.io',
        "oload": 'curl -F "file=@{full_file_path}" https://api.openload.cc/upload',
        "anonfiles": 'curl -F "file=@{full_file_path}" https://api.anonfiles.com/upload',
        "transfer": 'curl --upload-file "{full_file_path}" https://transfer.sh/'
        + path.basename(file_name),
        "filebin": 'curl -X POST --data-binary "@{full_file_path}" -H "filename: {bare_local_name}" "https://filebin.net"',
        "anonymousfiles": 'curl -F "file=@{full_file_path}" https://api.anonymousfiles.io/',
        "vshare": 'curl -F "file=@{full_file_path}" https://api.vshare.is/upload',
        "bayfiles": 'curl -F "file=@{full_file_path}" https://bayfiles.com/api/upload',
    }
    filename = path.basename(file_name)
    try:
        selected_one = CMD_WEB[selected_transfer].format(
            full_file_path=file_name, bare_local_name=filename
        )
    except KeyError:
        return await editor.edit("Invalid selected Transfer")
    cmd = selected_one
    t_response, err = _dogeutils.cmdrun(cmd)
    if t_response:
        try:
            t_response = dumps(loads(t_response), sort_keys=True, indent=4)
        except Exception as e:
            LOGS.info(str(e))
        urls = links = findall(link_regex, t_response)
        result = ""
        for i in urls:
            if not result:
                result = "**Uploaded File link/links:**"
            result += f"\n{i[0]}"
        await editor.edit(result)
    else:
        await editor.edit(err)
    if dogecheck:
        remove(file_name)
