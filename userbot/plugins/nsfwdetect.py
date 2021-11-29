# Copyright (C) 2020 - github.com/code-rgb [TG - @deleteduser420]
# Credits: @mrconfused (@sandy1709)
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from os import remove

from requests import post

from . import DEEPAI_API, doge, edl, eor, tr

plugin_category = "hub"


@doge.bot_cmd(
    pattern="detect$",
    command=("detect", plugin_category),
    info={
        "h": "To detect the nudity in reply image.",
        "d": "Reply detect command to any image or non animated sticker to detect the nudity in that",
        "u": "{tr}detect",
    },
)
async def detect(event):
    "To detect the nudity in reply image."
    if DEEPAI_API is None:
        return await edl(
            event,
            f"__You haven't set the api value.__ `{tr}setdog DEEPAI_API <api>` __from https://deepai.org/__.",
            link_preview=False,
        )
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to any image or non animated sticker !`", 5)
    dogevent = await eor(event, "`Downloading the file to check...`")
    media = await event.client.download_media(reply)
    if not media.endswith(("png", "jpg", "webp")):
        return await edl(event, "`Reply to any image or non animated sticker !`", 5)
    dogevent = await eor(event, "`Detecting NSFW limit...`")
    r = post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            "image": open(media, "rb"),
        },
        headers={"api-key": DEEPAI_API},
    )
    remove(media)
    if "status" in r.json():
        return await edl(dogevent, r.json()["status"])
    r_json = r.json()["output"]
    pic_id = r.json()["id"]
    percentage = r_json["nsfw_score"] * 100
    detections = r_json["detections"]
    link = f"https://api.deepai.org/job-view-file/{pic_id}/inputs/image.jpg"
    result = f"<b>Detected Nudity:</b>\n<a href='{link}'>>>></a> <code>{percentage:.3f}%</code>\n\n"
    if detections:
        for parts in detections:
            name = parts["name"]
            confidence = int(float(parts["confidence"]) * 100)
            result += f"<b>• {name}:</b>\n   <code>{confidence} %</code>\n"
    await eor(
        dogevent,
        result,
        link_preview=False,
        parse_mode="HTML",
    )
