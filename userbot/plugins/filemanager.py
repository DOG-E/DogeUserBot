from asyncio import sleep
from io import BytesIO
from os import getcwd, listdir
from os import path as osp
from os import stat
from pathlib import Path
from shutil import move
from time import ctime

from bs4 import BeautifulSoup
from requests import get

from . import (
    Config,
    _dogeutils,
    _format,
    deEmojify,
    doge,
    edl,
    eor,
    getTranslate,
    gvarstatus,
    humanbytes,
)

plugin_category = "bot"


@doge.bot_cmd(
    pattern="ls(?:\s|$)([\s\S]*)",
    command=("ls", plugin_category),
    info={
        "header": "To list all files and folders.",
        "description": "Will show all files and folders if no path is given or folder path is given else will show file details(if file path os given).",
        "usage": "{tr}ls <path>",
        "examples": "{tr}ls userbot",
    },
)
async def lst(event):  # sourcery no-metrics
    "To list all files and folders."
    dog = "".join(event.text.split(maxsplit=1)[1:])
    path = dog or getcwd()
    if not osp.exists(path):
        return await edl(
            event,
            f"There is no such directory or file with the name `{dog}` check again",
            15,
        )

    path = Path(dog) if dog else getcwd()
    if osp.isdir(path):
        if dog:
            msg = "Folders & Files in `{}`:\n".format(path)
        else:
            msg = "Folders & Files in Current Directory:\n"
        lists = listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            dogpath = osp.join(path, contents)
            if not osp.isdir(dogpath):
                size = stat(dogpath).st_size
                if str(contents).endswith(".py"):
                    files += f"🐾 `{contents}`\n"
                elif str(contents).endswith(".json"):
                    files += f"🦴 `{contents}`\n"
                elif str(contents).endswith(".yml"):
                    files += f"🧶 `{contents}`\n"
                elif str(contents).endswith(".exe"):
                    files += f"🔮 `{contents}`\n"
                elif str(contents).endswith(".opus"):
                    files += f"🔉 `{contents}`\n"
                elif str(contents).endswith((".flac", ".m4a", ".mp3", ".ogg", ".wav")):
                    files += f"🎵 `{contents}`\n"
                elif str(contents).endswith(
                    (".avi", ".flv", ".gif", ".mkv", ".mov", ".mp4", ".webm")
                ):
                    files += f"🎞 `{contents}`\n"
                elif str(contents).endswith(
                    (".bmp", ".ico", ".jpg", ".jpeg", ".png", ".webp")
                ):
                    files += f"🖼 `{contents}`\n"
                elif str(contents).endswith((".rar", ".tar", ".tar.gz", ".zip")):
                    files += f"🗃 `{contents}`\n"
                elif str(contents).endswith((".apk", ".xapk")):
                    files += f"📲 `{contents}`\n"
                elif str(contents).endswith((".log", ".md", ".text", ".txt")):
                    files += f"📄 `{contents}`\n"
                elif str(contents).endswith((".epub", ".pdf")):
                    files += f"📗 `{contents}`\n"
                elif "." in str(contents)[1:]:
                    files += f"💾 `{contents}`\n"
                else:
                    files += f"📙 `{contents}`\n"
            else:
                folders += f"🗂 `{contents}`\n"
        msg = msg + folders + files if files or folders else msg + "__Empty directory__"
    else:
        size = stat(path).st_size
        msg = "The details of given file:\n"
        if str(path).endswith(".py"):
            mode = "🐾"
        elif str(path).endswith(".json"):
            mode = "🦴"
        elif str(path).endswith(".yml"):
            mode = "🧶"
        elif str(path).endswith(".exe"):
            mode = "🔮"
        elif str(path).endswith(".opus"):
            mode = "🔉"
        elif str(path).endswith((".flac", ".m4a", ".mp3", ".ogg", ".wav")):
            mode = "🎵"
        elif str(path).endswith(
            (".avi", ".flv", ".gif", ".mkv", ".mov", ".mp4", ".webm")
        ):
            mode = "🎞"
        elif str(path).endswith((".bmp", ".ico", ".jpg", ".jpeg", ".png", ".webp")):
            mode = "🖼"
        elif str(path).endswith((".rar", ".tar", ".tar.gz", ".zip")):
            mode = "🗃"
        elif str(path).endswith((".apk", ".xapk")):
            mode = "📲"
        elif str(path).endswith((".log", ".md", ".text", ".txt")):
            mode = "📄"
        elif str(path).endswith((".epub", ".pdf")):
            mode = "📗"
        else:
            mode = "📙"
        ctime(osp.getctime(path))
        time2 = ctime(osp.getmtime(path))
        time3 = ctime(osp.getatime(path))
        msg += f"🧩 **Location:** `{path}`\n"
        msg += f"✨ **Icon:** `{mode}`\n"
        msg += f"📀 **Size:** `{humanbytes(size)}`\n"
        msg += f"📆 **Last Modified Time:** `{time2}`\n"
        msg += f"📅 **Last Accessed Time:** `{time3}`"
    if len(msg) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with BytesIO(str.encode(msg)) as out_file:
            out_file.name = "@DogeUserBot_ls.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=path,
            )
            await event.delete()
    else:
        await eor(event, msg)


@doge.bot_cmd(
    pattern="rem ([\s\S]*)",
    command=("rem", plugin_category),
    info={
        "header": "To delete a file or folder from the server",
        "usage": "{tr}rem <path>",
        "examples": "{tr}rem Dockerfile",
    },
)
async def lst(event):
    "To delete a file or folder."
    dog = event.pattern_match.group(1)
    if dog:
        path = Path(dog)
    else:
        return await eor(event, "what should i delete")

    if not osp.exists(path):
        return await eor(
            event,
            f"there is no such directory or file with the name `{dog}` check again",
        )

    dogecmd = f"rm -rf {path}"
    if osp.isdir(path):
        await _dogeutils.runcmd(dogecmd)
        await eor(event, f"Successfully removed `{path}` directory")
    else:
        await _dogeutils.runcmd(dogecmd)
        await eor(event, f"Successfully removed `{path}` file")


@doge.bot_cmd(
    pattern="mkdir(?:\s|$)([\s\S]*)",
    command=("mkdir", plugin_category),
    info={
        "header": "To create a new directory.",
        "usage": "{tr}mkdir <topic>",
        "examples": "{tr}mkdir dog",
    },
)
async def _(event):
    "To create a new directory."
    pwd = getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(
            event,
            "What should i create ?",
            parse_mode=_format.parse_pre,
        )

    original = osp.join(pwd, input_str.strip())
    if osp.exists(original):
        return await edl(
            event,
            f"Already a directory named {original} exists",
        )

    mone = await eor(event, "creating the directory ...", parse_mode=_format.parse_pre)
    await sleep(2)
    try:
        await _dogeutils.runcmd(f"mkdir {original}")
        await mone.edit(f"Successfully created the directory `{original}`")
    except Exception as e:
        await edl(mone, str(e), parse_mode=_format.parse_pre)


@doge.bot_cmd(
    pattern="cpto(?:\s|$)([\s\S]*)",
    command=("cpto", plugin_category),
    info={
        "header": "To copy a file from one directory to other directory",
        "usage": "{tr}cpto from ; to destination",
        "examples": "{tr}cpto sample_config.py ; downloads",
    },
)
async def _(event):
    "To copy a file from one directory to other directory"
    pwd = getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(
            event,
            "What and where should i move the file/folder.",
            parse_mode=_format.parse_pre,
        )

    loc = input_str.split(";")
    if len(loc) != 2:
        return await edl(
            event,
            "use proper syntax .cpto from ; to destination",
            parse_mode=_format.parse_pre,
        )

    original = osp.join(pwd, loc[0].strip())
    location = osp.join(pwd, loc[1].strip())
    if not osp.exists(original):
        return await edl(
            event,
            f"there is no such directory or file with the name `{original}` check again",
        )

    mone = await eor(event, "copying the file ...", parse_mode=_format.parse_pre)
    await sleep(2)
    try:
        await _dogeutils.runcmd(f"cp -r {original} {location}")
        await mone.edit(f"Successfully copied the `{original}` to `{location}`")
    except Exception as e:
        await edl(mone, str(e), parse_mode=_format.parse_pre)


@doge.bot_cmd(
    pattern="mvto(?:\s|$)([\s\S]*)",
    command=("mvto", plugin_category),
    info={
        "header": "To move a file from one directory to other directory.",
        "usage": "{tr}mvto frompath ; topath",
        "examples": "{tr}mvto stringsession.py ; downloads",
    },
)
async def _(event):
    "To move a file from one directory to other directory"
    pwd = getcwd()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(
            event,
            "What and where should i move the file/folder.",
            parse_mode=_format.parse_pre,
        )

    loc = input_str.split(";")
    if len(loc) != 2:
        return await edl(
            event,
            "use proper syntax .mvto from ; to destination",
            parse_mode=_format.parse_pre,
        )

    original = osp.join(pwd, loc[0].strip())
    location = osp.join(pwd, loc[1].strip())
    if not osp.exists(original):
        return await edl(
            event,
            f"there is no such directory or file with the name `{original}` check again",
        )

    mone = await eor(event, "Moving the file ...", parse_mode=_format.parse_pre)
    await sleep(2)
    try:
        move(original, location)
        await mone.edit(f"Successfully moved the `{original}` to `{location}`")
    except Exception as e:
        await edl(mone, str(e), parse_mode=_format.parse_pre)


@doge.bot_cmd(
    pattern="filext(?:\s|$)([\s\S]*)",
    command=("filext", plugin_category),
    info={
        "header": "Shows you the detailed information of given extension type. Only English.",
        "usage": "{tr}filext <extension>",
        "examples": "{tr}filext py",
    },
)
async def _(event):
    "Shows you the detailed information of given extension type."
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        DOGELANG = gvarstatus("DOGELANG") or "en"
        translated = await getTranslate(deEmojify(ext_details), dest=DOGELANG)
        await eor(
            event,
            f"**File Extension**: `{input_str}`\n**Description**: `{translated}`",
        )
    else:
        await eor(
            event,
            f"https://www.fileext.com/ responded with {status_code} for query: {input_str}",
        )
