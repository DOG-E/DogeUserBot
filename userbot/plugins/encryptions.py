from asyncio import get_event_loop
from base64 import b64decode, b64encode
from datetime import datetime
from os import path, remove
from subprocess import PIPE
from subprocess import run as runapp
from time import time

from barcode import get
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L

from . import Config, _dogeutils, doge, edl, eor, media_type, progress, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="decode$",
    command=("decode", plugin_category),
    info={
        "header": "To decode qrcode or barcode",
        "description": "Reply to qrcode or barcode to decode it and get text.",
        "usage": "{tr}decode",
    },
)
async def parseqr(event):
    "To decode qrcode or barcode"
    dogevent = await eor(event, "`Decoding....`")
    reply = await event.get_reply_message()
    downloaded_file_name = await reply.download_media()
    # parse the Official ZXing webpage to decode the QRCode
    command_to_exec = f"curl -s -F f=@{downloaded_file_name} https://zxing.org/w/decode"
    t_response, e_response = (await _dogeutils.runcmd(command_to_exec))[:2]
    if path.exists(downloaded_file_name):
        remove(downloaded_file_name)
    soup = BeautifulSoup(t_response, "html.parser")
    try:
        qr_contents = soup.find_all("pre")[0].text
        await eor(dogevent, f"**The decoded message is:**\n`{qr_contents}`")
    except IndexError:
        result = soup.text
        await eor(dogevent, f"**Failed to Decode:**\n`{result}`")
    except Exception as e:
        await eor(dogevent, f"**Error:**\n`{e}`")


@doge.bot_cmd(
    pattern="barcode ?([\s\S]*)",
    command=("barcode", plugin_category),
    info={
        "header": "To get barcode of given text.",
        "usage": "{tr}barcode <text>",
        "example": "{tr}barcode www.google.com",
    },
)
async def _(event):
    "to make barcode of given content."
    dogevent = await eor(event, "...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = await reply_id(event)
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") + "\r\n" for m in m_list)
            remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        remove(filename)
    except Exception as e:
        return await dogevent.edit(str(e))
    end = datetime.now()
    ms = (end - start).seconds
    await edl(dogevent, "Created BarCode in {} seconds".format(ms))


@doge.bot_cmd(
    pattern="makeqr(?:\s|$)([\s\S]*)",
    command=("makeqr", plugin_category),
    info={
        "header": "To get makeqr of given text.",
        "usage": "{tr}makeqr <text>",
        "example": "{tr}makeqr www.google.com",
    },
)
async def make_qr(makeqr):
    "make a QR Code containing the given content."
    input_str = makeqr.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = await reply_id(makeqr)
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = "".join(media.decode("UTF-8") + "\r\n" for media in m_list)
            remove(downloaded_file_name)
        else:
            message = previous_message.message
    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(
        makeqr.chat_id, "img_file.webp", reply_to=reply_msg_id
    )
    remove("img_file.webp")
    await makeqr.delete()


@doge.bot_cmd(
    pattern="hash ([\s\S]*)",
    command=("hash", plugin_category),
    info={
        "header": "Find the md5, sha1, sha256, sha512 of the string when written into a txt file.",
        "usage": "{tr}hash <text>",
        "examples": "{tr}hash DogeUserBot",
    },
)
async def gethash(hash_q):
    "Find the md5, sha1, sha256, sha512 of the string when written into a txt file."
    hashtxt_ = "".join(hash_q.text.split(maxsplit=1)[1:])
    with open("hashdis.txt", "w+") as hashtxt:
        hashtxt.write(hashtxt_)
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE)
    runapp(["rm", "hashdis.txt"], stdout=PIPE)
    sha512 = sha512.stdout.decode()
    ans = f"**Text : **\
            \n`{hashtxt_}`\
            \n**MD5 : **`\
            \n`{md5}`\
            \n**SHA1 : **`\
            \n`{sha1}`\
            \n**SHA256 : **`\
            \n`{sha256}`\
            \n**SHA512 : **`\
            \n`{sha512[:-1]}`\
         "
    await eor(hash_q, ans)


@doge.bot_cmd(
    pattern="hbase (en|de) ([\s\S]*)",
    command=("hbase", plugin_category),
    info={
        "header": "Find the base64 encoding or decoding of the given string.",
        "flags": {
            "en": "Use this to encode the given text.",
            "de": "use this to decode the given text.",
        },
        "usage": ["{tr}hbase en <text to encode>", "{tr}hbase de <encoded text>"],
        "examples": ["{tr}hbase en DogeUserBot", "{tr}hbase de Q2F0dXNlcmJvdA=="],
    },
)
async def endecrypt(event):
    "To encode or decode the string using base64"
    string = "".join(event.text.split(maxsplit=2)[2:])
    dogevent = event
    if event.pattern_match.group(1) == "en":
        if string:
            result = b64encode(bytes(string, "utf-8")).decode("utf-8")
            result = f"**Shhh! It's Encoded : **\n`{result}`"
        else:
            reply = await event.get_reply_message()
            if not reply:
                return await edl(event, "`What should i encode`")
            mediatype = media_type(reply)
            if mediatype is None:
                result = b64encode(bytes(reply.text, "utf-8")).decode("utf-8")
                result = f"**Shhh! It's Encoded : **\n`{result}`"
            else:
                dogevent = await eor(event, "`Encoding ...`")
                c_time = time()
                downloaded_file_name = await event.client.download_media(
                    reply,
                    Config.TMP_DOWNLOAD_DIRECTORY,
                    progress_callback=lambda d, t: get_event_loop().create_task(
                        progress(d, t, dogevent, c_time, "trying to download")
                    ),
                )
                dogevent = await eor(event, "`Encoding ...`")
                with open(downloaded_file_name, "rb") as image_file:
                    result = b64encode(image_file.read()).decode("utf-8")
                remove(downloaded_file_name)
        await eor(dogevent, result, file_name="encodedfile.txt", caption="It's Encoded")
    else:
        try:
            lething = str(
                b64decode(bytes(event.pattern_match.group(2), "utf-8"), validate=True)
            )[2:]
            await eor(event, "**Decoded text :**\n`" + lething[:-1] + "`")
        except Exception as e:
            await edl(event, f"**Error:**\n__{e}__")
