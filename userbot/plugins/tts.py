from datetime import datetime
from os import makedirs, path, remove
from subprocess import STDOUT, CalledProcessError, check_output

from gtts import gTTS

from . import deEmojify, doge, edl, eor, gvarstatus, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="tts(?:\s|$)([\s\S]*)",
    command=("tts", plugin_category),
    info={
        "header": "Text to speech command.",
        "usage": [
            "{tr}tts <text>",
            "{tr}tts <reply>",
            "{tr}tts <language code> ; <text>",
        ],
    },
)
async def _(event):
    "text to speech command"
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    reply_to_id = await reply_id(event)
    if ";" in input_str:
        lng, text = input_str.split(";")
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lng = input_str or gvarstatus("TTS_LANG") or "en"
    else:
        if not input_str:
            return await eor(event, "Invalid Syntax. Module stopping.")
        text = input_str
        lng = gvarstatus("TTS_LANG") or "en"
    dogevent = await eor(event, "`Recording......`")
    text = deEmojify(text.strip())
    lng = lng.strip()
    if not path.isdir("./temp/"):
        makedirs("./temp/")
    required_file_name = "./temp/" + "voice.ogg"
    try:
        # https://github.com/SpEcHiDe/UniBorg/commit/17f8682d5d2df7f3921f50271b5b6722c80f4106
        tts = gTTS(text, lang=lng)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            required_file_name + ".opus",
        ]
        try:
            t_response = check_output(command_to_execute, stderr=STDOUT)
        except (CalledProcessError, NameError, FileNotFoundError) as exc:
            await dogevent.edit(str(exc))
            # continue sending required_file_name
        else:
            remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.now()
        ms = (end - start).seconds
        await event.client.send_file(
            event.chat_id,
            required_file_name,
            reply_to=reply_to_id,
            allow_cache=False,
            voice_note=True,
        )
        remove(required_file_name)
        await edl(
            dogevent,
            "`Processed text {} into voice in {} seconds!`".format(text[0:20], ms),
        )
    except Exception as e:
        await eor(dogevent, f"**Error:**\n`{e}`")
