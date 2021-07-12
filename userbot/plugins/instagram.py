import os
from datetime import datetime

import instaloader
import requests
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from . import doge, edl, eor, hmention

plugin_category = "misc"
IGU = instaloader.Instaloader()


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
    async with doge.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
        except YouBlockedUserError:
            doge(UnblockRequest(chat))
            await conv.send_message("/start")
        await conv.get_response()
        await conv.send_message(link)
        video = await conv.get_response()
        await conv.get_response()
        await doge.send_read_acknowledge(conv.chat_id)
        await dogevent.delete()
        dog = await doge.send_file(
            event.chat_id,
            video,
        )
        end = datetime.now()
        ms = (end - start).seconds
        await dog.edit(
            f"<b><i>➥ Video uploaded in {ms} seconds.</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
            parse_mode="html",
        )


@doge.bot_cmd(
    pattern="iginfo(?:\s|$)([\s\S]*)",
    command=("iginfo", plugin_category),
    info={
        "header": "Learn information about the Instagram profile",
        "examples": [
            "{tr}insta <username>",
        ],
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
        profile = instaloader.Profile.from_username(IGU.context, last)
        pp = profile.get_profile_pic_url()
        name = profile.full_name
        if not name:
            name = "❗ This user has no name."
        bio = profile.biography
        if not bio:
            bio = "❗ This user has no bio."
        follower = profile.followers
        verif = profile.is_verified
        post = profile.mediacount
        follow = profile.followees
        url = profile.external_url
        busacc = profile.is_business_account
        priv = profile.is_private
        user = profile.userid
        r = requests.get(pp)
        with open("@DogeUserBot.jpg", "wb") as file:
            file.write(r.content)
        igtv = profile.igtvcount
        msg = f"""• Iɴsᴛᴀɢʀᴀᴍ Pʀᴏғɪʟᴇ Iɴғᴏʀᴍᴀᴛɪᴏɴ •

        **🔗 Lɪɴᴋ:** [{last}](https://instagr.am/{last})

        **🆔 Iᴅ:**   `{user}`
        **👤 Nᴀᴍᴇ:** `{name}`

        **📍 Bɪᴏ:**
`{bio}`

        **🔗 Bɪᴏ Lɪɴᴋ:** {url}

        **❤️ Fᴏʟʟᴏᴡᴇʀs:**   `{follower}`
        **👀 Fᴏʟʟᴏᴡᴇs:**    `{follow}`
        **📸 Pᴏsᴛ:**        `{post}`
        **📺 IɢTᴠ Pᴏsᴛ:**   `{igtv}`

        **✅ Vᴇʀɪғɪᴇᴅ ?:**  `{verif}`
        **💼 Bᴜssɪɴᴇss ?:** `{busacc}`
        **🔒 Pʀɪᴠᴀᴛᴇ ?:**    `{priv}`
            """
        await dogevent.delete()
        await doge.send_file(event.chat_id, "@DogeUserBot.jpg", caption=msg)
        os.remove("@DogeUserBot.jpg")
    except:
        await edl(
            dogevent,
            f"**⚠️ Error!\n❗ Instagram username `{last}` is incorrect.\n\n💫 Check & try again!**",
            time=30,
        )
