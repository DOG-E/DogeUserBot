from os import makedirs
from os import path as osp
from os import remove

from googletrans import LANGUAGES
from requests import post

from . import (
    Config,
    _dogetools,
    convert_toimage,
    deEmojify,
    doge,
    edl,
    eor,
    getTranslate,
    gvarstatus,
)

plugin_category = "tool"


async def ocr_space_file(
    filename, overlay=False, api_key=Config.OCRSPACE_API, language="eng"
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        r = post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.json()


@doge.bot_cmd(
    pattern="(|t)ocr(?:\s|$)([\s\S]*)",
    command=("ocr", plugin_category),
    info={
        "header": "To read text in image/gif/sticker/video and print it.",
        "description": "Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi).",
        "usage": "{tr}ocr <language code>",
        "examples": "{tr}ocr eng",
    },
)
async def ocr(event):
    "To read text in media."
    reply = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply.media:
        return await edl(event, "__Reply to a media to read text on it__")
    dogevent = await eor(event, "`Reading...`")
    if not osp.isdir(Config.TEMP_DIR):
        makedirs(Config.TEMP_DIR)
    cmd = event.pattern_match.group(1)
    arg = event.pattern_match.group(2)
    if arg == "ar":
        arg = "ara"
    elif arg == "bg":
        arg = "bul"
    elif arg == "cs":
        arg = "cze"
    elif arg == "da":
        arg = "dan"
    elif arg == "de":
        arg = "ger"
    elif arg == "el":
        arg = "gre"
    elif arg == "en":
        arg = "eng"
    elif arg == "es":
        arg = "spa"
    elif arg == "fi":
        arg = "fn"
    elif arg == "fr":
        arg = "fre"
    elif arg == "hr":
        arg = "hrv"
    elif arg == "hu":
        arg = "hun"
    elif arg == "it":
        arg = "ita"
    elif arg == "ja":
        arg = "jpn"
    elif arg == "ko":
        arg = "kor"
    elif arg == "nl":
        arg = "dut"
    elif arg == "pl":
        arg = "pol"
    elif arg == "pt":
        arg = "por"
    elif arg == "ru":
        arg = "rus"
    elif arg == "sl":
        arg = "slv"
    elif arg == "sv":
        arg = "swe"
    elif arg == "tr":
        arg = "tur"
    elif arg == "zh-cn" or arg == "cn":
        arg = "chs"
    elif arg == "zh-tw":
        arg = "cht"
    output_file = osp.join(Config.TEMP_DIR, "ocr.jpg")
    try:
        output = await _dogetools.media_to_pic(event, reply)
        outputt = convert_toimage(output[1], filename=output_file)
    except AttributeError:
        await dogevent.edit("`Couldn't read it.. you sure this readable !?`")
    test_file = await ocr_space_file(filename=output_file, language=arg)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await dogevent.edit("`Couldn't read it.`\n`I guess I need new glasses.`")
    else:
        if cmd == "":
            await dogevent.edit(
                f"**Here's what I could read from it:**\n\n`{ParsedText}`"
            )
        if cmd == "t":
            TRT_LANG = gvarstatus("TOCR_LANG") or "en"
            try:
                reply_text = await getTranslate(deEmojify(ParsedText), dest=TRT_LANG)
            except ValueError:
                return await edl(event, "`Invalid destination language.`", time=5)
            source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
            transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
            tran_text = f"📜**Translate:\nFrom {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}) :**\n\n`{reply_text.text}`"
            await dogevent.edit(
                f"🧧 **Here's what I could read from it:**\n\n`{ParsedText}`\n\n{tran_text}"
            )
    remove(output_file)


@doge.bot_cmd(
    pattern="tocr",
    command=("tocr", plugin_category),
    info={
        "header": "To read text in image/gif/sticker/video and print it with its translation.",
        "description": "Reply to an image/gif/sticker/video to extract text from it and print it with its translation.\n\nGet language codes from [here](https://ocr.space/ocrapi).",
        "note": "for this command transalted language set lanuage by `.lang tocr` command.",
        "usage": "{tr}tocr <language code>",
        "examples": "{tr}tocr en",
    },
)
async def ocr(event):
    "To read text in media & paste with translated."
