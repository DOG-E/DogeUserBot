from googletrans import LANGUAGES

from . import BOTLOG, BOTLOG_CHATID, deEmojify, doge, edl, eor, getTranslate, gvarstatus

plugin_category = "tool"


@doge.bot_cmd(
    pattern="tl ([\s\S]*)",
    command=("tl", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl tr ; DogeUserBot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    text = None
    if ";" in input_str:
        lang, text = input_str.split(";")
    elif event.reply_to_msg_id and not text:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lang = input_str or "en"
    else:
        return await edl(event, "`.tl LanguageCode` as reply to a message", time=5)
    text = deEmojify(text.strip())
    lang = lang.strip()
    try:
        translated = await getTranslate(text, dest=lang)
        after_tr_text = translated.text
        output_str = f"**TRANSLATED from {LANGUAGES[translated.src].title()} to {LANGUAGES[lang].title()}**\
                \n`{after_tr_text}`"
        await eor(event, output_str)
    except Exception as exc:
        await edl(event, f"**Error:**\n`{exc}`", time=5)


@doge.bot_cmd(
    pattern="trt(?: |$)([\s\S]*)",
    command=("trt", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "for this command set lanuage by `{tr}lang trt` command.",
        "usage": [
            "{tr}trt",
            "{tr}trt <text>",
        ],
    },
)
async def translateme(trans):
    "To translate the text to required language."
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await eor(trans, "`Give a text or reply to a message to translate!`")

    TRT_LANG = gvarstatus("TRT_LANG") or "en"
    try:
        reply_text = await getTranslate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        return await edl(trans, "`Invalid destination language.`", time=5)

    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**From {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}):**\n`{reply_text.text}`"
    await eor(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.`",
        )
