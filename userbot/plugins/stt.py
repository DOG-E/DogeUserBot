# speech to text module for catuserbot by uniborg (@spechide)
from datetime import datetime
from os import makedirs, path, remove

from requests import post
from telethon.events import MessageEdited

from . import Config, doge, edl, eor, fsmessage, lan, media_type

plugin_category = "tool"

chat = "@VoicyBot"


@doge.bot_cmd(
    pattern="(stt|voicy)$",
    command=("stt", plugin_category),
    info={
        "header": "Speech to text module.",
        "usage": ["{tr}stt", "{tr}voicy"],
    },
)
async def _(event):
    "Speech to text."
    try:
        reply = await event.get_reply_message()
        mediatype = media_type(reply)
        if not reply or (mediatype and mediatype not in ["Voice", "Audio"]):
            return await edl(
                event,
                "`Reply to a voice message or audio, to get the relevant transcript.`",
            )
        dogevent = await eor(event, "`I'm listening to voice...`")
        async with doge.conversation(chat) as conv:
            response = conv.wait_event(MessageEdited(incoming=True, from_users=chat))
            await fsmessage(event, reply, forward=True, chat=chat)
            response = await response
            if response.text.startswith("👋"):
                await eor(
                    dogevent,
                    "**You need to start the @VoicyBot\n& write /language\n& choose your language.**",
                )
            elif response.text.startswith("__👮"):
                await edl(
                    dogevent, "**The sound is broken.\nI didn't understand what said.**"
                )
            else:
                res = response.text.replace(
                    "Powered by [Todorant](https://todorant.com/?utm_source=voicy)",
                    "`\n🧡 Doɢᴇ UsᴇʀBoᴛ 🐾",
                )
                await dogevent.edit(f"**I heard something: **\n\n`{res}`")
            await conv.mark_read()
            await conv.cancel_all()

    except:
        if (
            Config.IBM_WATSON_CRED_URL is None
            or Config.IBM_WATSON_CRED_PASSWORD is None
        ):
            return await edl(
                event,
                "`You need to set the required ENV variables for this module. \nModule stopping`",
            )
        start = datetime.now()
        langu = "en"
        if not path.isdir(Config.TEMP_DIR):
            makedirs(Config.TEMP_DIR)
        reply = await event.get_reply_message()
        mediatype = media_type(reply)
        if not reply or (mediatype and mediatype not in ["Voice", "Audio"]):
            return await edl(
                event,
                "`Reply to a voice message or audio, to get the relevant transcript.`",
            )
        dogevent = await eor(event, "`Downloading to my local, for analysis  🙇`")
        required_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
        await dogevent.edit("`Starting analysis, using IBM WatSon Speech To Text`")
        headers = {
            "Content-Type": reply.media.document.mime_type,
        }
        data = open(required_file_name, "rb").read()
        response = post(
            Config.IBM_WATSON_CRED_URL + "/v1/recognize",
            headers=headers,
            data=data,
            auth=("apikey", Config.IBM_WATSON_CRED_PASSWORD),
        )
        r = response.json()
        if "results" not in r:
            return await dogevent.edit(r["error"])
        # process the json to appropriate string format
        results = r["results"]
        transcript_response = ""
        transcript_confidence = ""
        for alternative in results:
            alternatives = alternative["alternatives"][0]
            transcript_response += " " + str(alternatives["transcript"])
            transcript_confidence += " " + str(alternatives["confidence"])
        end = datetime.now()
        ms = (end - start).seconds
        if transcript_response == "":
            string_to_show = "**Language: **`{}`\n**Time Taken: **`{} seconds`\n**No Results Found**".format(
                langu, ms
            )
        else:
            string_to_show = "**Language: **`{}`\n**Transcript: **`{}`\n**Time Taken: **`{} seconds`\n**Confidence: **`{}`".format(
                langu, transcript_response, ms, transcript_confidence
            )
        await dogevent.edit(string_to_show)
        # now, remove the temporary file
        remove(required_file_name)


@doge.bot_cmd(
    pattern="voicya$",
    command=("voicya", plugin_category),
    info={
        "header": "Sets whether the Voicy bot recognizes all audio files.",
        "usage": "{tr}voicya",
        "note": "The setting is turned on or off each time you write the {tr}`voicya` command.",
    },
)
async def _(event):
    dogevent = await eor(event, lan("processing"))
    async with doge.conversation(chat) as conv:
        await fsmessage(event=event, text="/files", chat=chat)
        response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
        response = await response
        if response.text.startswith("📁"):
            await eor(
                dogevent,
                f"**Changed the setting:\n\n{response.text}**",
            )
        else:
            await edl(dogevent, "**Voicy not working!**")
        await conv.mark_read()
        await conv.cancel_all()
