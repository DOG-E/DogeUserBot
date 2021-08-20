from datetime import datetime
from os import remove

from instaloader import Instaloader
from instaloader.Profile import from_username
from requests import get

from . import doge, edl, eor, fsmessage, hmention

plugin_category = "misc"

IGU = Instaloader()


@doge.bot_cmd(
    pattern="insta ([\s\S]*)",
    command=("insta", plugin_category),
    info={
        "header": "To download instagram video/photo",
        "description": "Note downloads only public profile photos/videos.",
        "examples": [
            "{tr}insta <link>",
        ],
    },
)
async def kakashi(event):
    "For downloading instagram media"
    chat = "@instasavegrambot"
    link = event.pattern_match.group(1)
    if "www.instagram.com" or "instagram.com" not in link:
        await edl(event, "` I need a Instagram link to download it's video...`(*_*)")
    else:
        start = datetime.now()
        dogevent = await eor(event, "**Downloading...**")
    async with event.client.conversation(chat) as conv:
        await fsmessage(event, text=link, chat=chat)
        video = await conv.get_response()
        await conv.get_response()
        await dogevent.delete()
        dog = await event.client.send_file(
            event.chat_id,
            video,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await dog.edit(
            f"<b><i>➥ Video uploaded in {ms} seconds.</i></b>\n<b><i>➥ Uploaded by: {hmention}</i></b>",
            parse_mode="html",
        )
        await conv.mark_read()
        await conv.cancel_all()


@doge.bot_cmd(
    pattern="iginfo(?:\s|$)([\s\S]*)",
    command=("iginfo", plugin_category),
    info={
        "header": "Learn information about the Instagram profile",
        "examples": ["{tr}iginfo <username>", "{tr}iginfo <reply username>"],
    },
)
async def iginfo(event):
    username = event.pattern_match.group(1)
    if not username:
        replyusername = await event.get_reply_message()
        username = replyusername.text
    if not username:
        return await edl(event, "Give me an Instagram username.")
    last = username.lower()
    try:
        dogevent = await eor(
            event, "⏳ I bring the information of the desired Instagram profile..."
        )
        profile = from_username(IGU.context, last)
        pp = profile.get_profile_pic_url()
        name = profile.full_name
        if not name:
            name = "🚨 This user has no name."
        bio = profile.biography
        if not bio:
            bio = "🚨 This user has no bio."
        follower = profile.followers
        verif = profile.is_verified
        post = profile.mediacount
        follow = profile.followees
        url = profile.external_url
        busacc = profile.is_business_account
        priv = profile.is_private
        user = profile.userid
        r = get(pp)
        with open("@DogeUserBot.jpg", "wb") as file:
            file.write(r.content)
        igtv = profile.igtvcount
        msg = f"""**• Iɴsᴛᴀɢʀᴀᴍ Pʀoғɪʟᴇ Iɴғoʀᴍᴀᴛɪoɴ •**

        **🔗 Lɪɴᴋ:** [{last}](https://instagr.am/{last})

        **🆔 Iᴅ:**   `{user}`
        **👤 Nᴀᴍᴇ:** `{name}`

        **📍 Bɪo:**
        `{bio}`

        **🔗 Bɪo Lɪɴᴋ:** {url}

        **❤️ Foʟʟoᴡᴇʀs:**  `{follower}`
        **👀 Foʟʟoᴡᴇs:**   `{follow}`
        **📸 Posᴛ:**       `{post}`
        **📺 IɢTᴠ Posᴛ:**  `{igtv}`

        **✅ Vᴇʀɪғɪᴇᴅ?:**  `{verif}`
        **💼 Bᴜssɪɴᴇss?:** `{busacc}`
        **🔒 Pʀɪᴠᴀᴛᴇ?:**    `{priv}`"""
        await dogevent.delete()
        await doge.send_file(event.chat_id, "@DogeUserBot.jpg", caption=msg)
        remove("@DogeUserBot.jpg")
    except:
        await edl(
            dogevent,
            f"**🚨 ERROR:\n⛔ Instagram username **`{last}`** is incorrect.\n\n💫 Check & try again!**",
            15,
        )
