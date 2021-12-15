# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
# _from googletrans import LANGUAGES

from . import BOTLOG, BOTLOG_CHATID, deEmojify, doge, edl, eor, gvar

plugin_category = "tool"


@doge.bot_cmd(
    pattern="tl ([\s\S]*)",
    command=("tl", plugin_category),
    info={
        "h": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "u": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "e": "{tr}tl tr ; DogeUserBot is one of the popular bot",
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
    # _try:
        # _translated = await getTranslate(text, dest=lang)
        # _after_tr_text = translated.text
        # _output_str = f"**TRANSLATED from {LANGUAGES[translated.src].title()} to {LANGUAGES[lang].title()}**\
        # _        \n`{after_tr_text}`"
        # _await eor(event, output_str)
    # _except Exception as exc:
        # _await edl(event, f"**Error:**\n`{exc}`", time=5)


@doge.bot_cmd(
    pattern="trt(?: |$)([\s\S]*)",
    command=("trt", plugin_category),
    info={
        "h": "To translate the text to required language.",
        "note": "for this command set lanuage by `{tr}lang trt` command.",
        "u": [
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

    TRT_LANG = gvar("TRT_LANG") or "en"
    # _try:
    # _    reply_text = await getTranslate(deEmojify(message), dest=TRT_LANG)
    # _except ValueError:
    # _    return await edl(trans, "`Invalid destination language.`", time=5)

    # _source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    # _transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    # _reply_text = f"**From {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}):**\n`{reply_text.text}`"
    # _await eor(trans, reply_text)
    # _if BOTLOG:
    # _    await trans.client.send_message(
    # _        BOTLOG_CHATID,
    # _        f"`Translated some {source_lan.title()} stuff to {transl_lan.title()} just now.`",
    # _    )
