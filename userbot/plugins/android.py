# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from json import loads
from re import findall

from bs4 import BeautifulSoup
from requests import get

from . import doge, edl, eor, tr

plugin_category = "tool"


@doge.bot_cmd(
    pattern="magisk$",
    command=("magisk", plugin_category),
    info={
        "header": lan("magisk1"),
        "usage": "{tr}magisk",
    },
)
async def kakashi(event):
    lan("magisk2")
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/"
    magisk_dict = {
        f"⦁ **{lan('magisk3')}**": magisk_repo + "master/stable.json",
        f"⦁ **{lan('magisk4')}**": magisk_repo + "master/beta.json",
        f"⦁ **{lan('magisk5')}**": magisk_repo + "master/canary.json",
    }
    releases = f"{lan('magisk6')}\n\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[{lan("magisk7")}]({data["magisk"]["note"]})\n'
        )
    await eor(event, releases)


@doge.bot_cmd(
    pattern="device(?: |$)(\S*)",
    command=("device", plugin_category),
    info={
        "header": lan("device1"),
        "usage": f"{tr}device {lan('device2')}",
        "examples": f"{tr}device {lan('device3')}",
    },
)
async def device_info(event):
    lan("device4")
    textx = await event.get_reply_message()
    codename = event.pattern_match.group(1)
    if not codename:
        if textx:
            codename = textx.text
        else:
            return await edl(event, f"**{lan('usage')}:** {tr}device {lan('device5')}`")
    data = loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = lan("device6").format(codename)
        for item in results:
            reply += (
                f"**{lan('device7')}** {item['brand']}\n"
                f"**{lan('device8')}** {item['name']}\n"
                f"**{lan('device9')}** {item['model']}\n\n"
            )
    else:
        reply = lan("device10").format(codename)
    await eor(event, reply)


@doge.bot_cmd(
    pattern="dcname(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("dcname", plugin_category),
    info={
        "header": lan("dcname1"),
        "usage": f"{tr}dcname {lan('dcname2')}",
        "examples": "{tr}dcname Xiaomi Redmi Note 5 Pro",
    },
)
async def codename_info(event):
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edl(event, f"**{lan('usage')}**: `{tr}dcname {lan('dcname2')}`")

    data = loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        return await eor(event, lan("dcname").format(brand))
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = lan("dcname4").format(brand, device)
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**{lan('dcname5')}:** {item['device']}\n"
                f"**{lan('device8')}:** {item['name']}\n"
                f"**{lan('device9')}:** {item['model']}\n\n"
            )
    else:
        reply = lan("dcname6").format(device)
    await eor(event, reply)


@doge.bot_cmd(
    pattern="specs(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("specs", plugin_category),
    info={
        "header": lan("specs1"),
        "usage": "{tr}specs",
        "examples": "{tr}specs Xiaomi Redmi Note 5 Pro",
    },
)
async def devices_specifications(event):
    lan("specs2")
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edl(event, f"**{lan('usage')}** `{tr}specs` {lan('specs3')}")
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        return await edl(event, lan("specs4").format(brand))
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        return await edl(event, lan("specs5").format(device))
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}:** {data}\n"
    await eor(event, reply)


@doge.bot_cmd(
    pattern="twrp(?: |$)(\S*)",
    command=("twrp", plugin_category),
    info={
        "header": lan("twrp1"),
        "usage": f"{tr}twrp {lan('twrp2')}",
        "examples": f"{tr}twrp {lan('device3')}",
    },
)
async def twrp(event):
    lan("twrp3")
    textx = await event.get_reply_message()
    device = event.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await edl(event, f"**{lan('usage')}:** `{tr}twrp {lan('twrp2')}`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = lan("twrp4").format(device)
        return await edl(event, reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f'{lan("twrp5").forma(device)}'
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**{lan('twrp6')}** __{date}__\n"
    )
    await eor(event, reply)


# Lang By Aylak - @atayist
# Copyright (C) 2021 - DOG-E
