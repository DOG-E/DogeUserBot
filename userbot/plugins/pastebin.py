from os import path as osp
from os import remove
from re import findall

from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from requests import get
from requests.exceptions import HTTPError, Timeout, TooManyRedirects
from telethon.utils import get_extension
from urlextract import URLExtract

from ..core.events import MessageEdited
from . import (
    Config,
    doge,
    edl,
    eor,
    fsmessage,
    logging,
    media_type,
    pastetext,
    reply_id,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

extractor = URLExtract()
pastebins = {
    "Pasty": "p",
    "Neko": "n",
    "Spacebin": "s",
    "Dog": "d",
}


def get_key(val):
    for key, value in pastebins.items():
        if val == value:
            return key


@doge.bot_cmd(
    pattern="pcode(?:\s|$)([\s\S]*)",
    command=("pcode", plugin_category),
    info={
        "header": "Will paste the entire text on the blank white image.",
        "flags": {
            "f": "Use this flag to send it as file rather than image",
        },
        "usage": ["{tr}pcode <reply>", "{tr}pcode text"],
    },
)
async def paste_img(event):
    "To paste text to image."
    reply_to = await reply_id(event)
    d_file_name = None
    dogevent = await eor(event, "`Pasting the text on image`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    ext = findall(r"-f", input_str)
    extension = None
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply.text:
            text_to_print = reply and reply.raw_text
        else:
            return await edl(
                dogevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    highlight(
        text_to_print,
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "out.png",
    )
    try:
        await event.client.send_file(
            event.chat_id,
            "out.png",
            force_document=bool(extension),
            reply_to=reply_to,
        )
        await dogevent.delete()
        remove("out.png")
        if d_file_name is not None:
            remove(d_file_name)
    except Exception as e:
        await edl(
            dogevent,
            f"**Error:**\n`{e}`",
        )


@doge.bot_cmd(
    pattern="(d|p|s|n)?(paste|neko)(?:\s|$)([\S\s]*)",
    command=("paste", plugin_category),
    info={
        "header": "To paste text to a paste bin.",
        "description": "Uploads the given text to website so that you can share text/code with others easily. If no flag is used then it will use p as default",
        "flags": {
            "d": "Will paste text to dog.bin",
            "p": "Will paste text to pasty.lus.pm",
            "s": "Will paste text to spaceb.in (language extension not there at present.)",
        },
        "usage": [
            "{tr}{flags}paste <reply/text>",
            "{tr}{flags}paste {extension} <reply/text>",
        ],
        "examples": [
            "{tr}spaste <reply/text>",
            "{tr}ppaste -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def paste_bin(event):
    "To paste text to a paste bin."
    dogevent = await eor(event, "`pasting text to paste bin....`")
    input_str = event.pattern_match.group(3)
    reply = await event.get_reply_message()
    ext = findall(r"-\w+", input_str)
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    if event.pattern_match.group(2) == "neko":
        pastetype = "n"
    else:
        pastetype = event.pattern_match.group(1) or "p"
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            if extension is None:
                extension = get_extension(reply.document)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply.text:
            text_to_print = reply and reply.raw_text
        else:
            return await edl(
                dogevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pastetext(text_to_print, pastetype, extension)
        if "error" in response:
            return await edl(
                dogevent,
                "**Error while pasting text:**\n`Unable to process your request may be pastebins are down.`",
            )
        result = ""
        if pastebins[response["bin"]] != pastetype:
            result += f"<b>{get_key(pastetype)} is down, So </b>"
        result += f"<b>Pasted to: <a href={response['url']}>{response['bin']}</a></b>"
        if response["raw"] != "":
            result += f"\n<b>Raw link: <a href={response['raw']}>Raw</a></b>"
        await dogevent.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await edl(dogevent, f"**Error while pasting text:**\n`{e}`")


@doge.bot_cmd(
    command=("neko", plugin_category),
    info={
        "header": "To paste text to a neko bin.",
        "description": "Uploads the given text to nekobin so that you can share text/code with others easily.",
        "usage": ["{tr}neko <reply/text>", "{tr}neko {extension} <reply/text>"],
        "examples": [
            "{tr}neko <reply/text>",
            "{tr}neko -py await event.client.send_message(chat,'Hello! testing123 123')",
        ],
    },
)
async def _(event):
    "To paste text to a neko bin."
    # just to show in help menu as seperate


@doge.bot_cmd(
    pattern="g(et)?paste(?:\s|$)([\s\S]*)",
    command=("getpaste", plugin_category),
    info={
        "header": "To paste text into telegram from pastebin link.",
        "description": "Gets the content of a pastebin. You can provide link along with cmd or reply to link.",
        "Support bins": ["pasty", "spacebin", "nekobin", "dogbin"],
        "usage": ["{tr}getpaste <link>", "{tr}gpaste <link>"],
    },
)
async def get_dogbin_content(event):
    "To paste text into telegram from del dog link."
    textx = await event.get_reply_message()
    url = event.pattern_match.group(2)
    if not url and textx.text:
        urls = extractor.find_urls(textx.text)
        for iurl in urls:
            if (
                ("pasty" in iurl)
                or ("spaceb" in iurl)
                or ("nekobin" in iurl)
                or ("dog" in iurl)
            ):
                url = iurl
                break
    if not url:
        return await edl(event, "__I can't find any pastebin link.__")
    dogevent = await eor(event, "`Getting Contents of pastebin.....`")
    rawurl = None
    if "raw" in url:
        rawurl = url
    if rawurl is None:
        fid = osp.splitext((osp.basename(url)))
        if "pasty" in url:
            rawurl = f"https://pasty.lus.pm/{fid[0]}/raw"
        elif "spaceb" in url:
            rawurl = f"https://spaceb.in/api/v1/documents/{fid[0]}/raw"
        elif "nekobin" in url:
            rawurl = f"nekobin.com/raw/{fid[0]}"
        elif "dog" in url:
            rawurl = f"https://del.dog/raw/{fid[0]}"
    resp = get(rawurl)
    try:
        resp.raise_for_status()
    except HTTPError as HTTPErr:
        return await dogevent.edit(
            f"**Request returned an unsuccessful status code.**\n\n__{str(HTTPErr)}__"
        )
    except Timeout as TimeoutErr:
        return await dogevent.edit(f"**Request timed out.**__{str(TimeoutErr)}__")
    except TooManyRedirects as RedirectsErr:
        return await dogevent.edit(
            (
                f"**Request exceeded the configured number of maximum redirections.**__{str(RedirectsErr)}__"
            )
        )
    reply_text = f"**Fetched dogbin URL content successfully!**\n\n**Content:** \n```{resp.text}```"
    await eor(dogevent, reply_text)


@doge.bot_cmd(
    pattern="paster(?:\s|$)([\s\S]*)",
    command=("paster", plugin_category),
    info={
        "header": "Create a instant view or a paste it in telegraph file.",
        "usage": ["{tr}paster <reply>", "{tr}paster text"],
    },
)
async def _(event):
    "Create a instant view or a paste it in telegraph file."
    dogevent = await eor(event, "`pasting text to paste bin....`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    pastetype = "d"
    text_to_print = input_str or ""
    if text_to_print == "" and reply and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply.text:
            text_to_print = reply and reply.raw_text
        else:
            return await edl(
                dogevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    try:
        response = await pastetext(text_to_print, pastetype, extension="txt")
        if "error" in response:
            return await edl(
                dogevent,
                "**Error while pasting text:**\n`Unable to process your request may be pastebins are down.`",
            )
    except Exception as e:
        return await edl(dogevent, f"**Error while pasting text:**\n`{e}`")
    url = response["url"]
    chat = "@CorsaBot"
    await dogevent.edit("`Making instant view...`")
    async with event.client.conversation(chat) as conv:
        response = conv.wait_event(
            MessageEdited(incoming=True, from_users=conv.chat_id), timeout=10
        )
        await fsmessage(event, url, chat=chat)
        response = await response
        result = ""
        if response:
            urls = extractor.find_urls(response.text)
            if urls:
                result = f"The instant preview is [here]({urls[0]})"
        if result == "":
            result = "I can't make it as instant view"
        await dogevent.edit(result, link_preview=True)
        await conv.mark_read()
        await conv.cancel_all()
