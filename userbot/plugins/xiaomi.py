# Credits: @eve_enryu
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, eor, xiaomeme

plugin_category = "tool"


@doge.bot_cmd(
    pattern="firmware ([\s\S]*)",
    command=("firmware", plugin_category),
    info={
        "h": "To get lastest Firmware.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}firmware <codename>",
        "e": "{tr}firmware whyred",
    },
)
async def _(event):
    "To get lastest Firmware."
    link = event.pattern_match.group(1)
    msg = f"/firmware {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="vendor ([\s\S]*)",
    command=("vendor", plugin_category),
    info={
        "h": "To get lastest Vendor.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}vendor <codename>",
        "e": "{tr}vendor whyred",
    },
)
async def _(event):
    "To get lastest Vendor."
    link = event.pattern_match.group(1)
    msg = f"/vendor {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="xspecs ([\s\S]*)",
    command=("xspecs", plugin_category),
    info={
        "h": "To get quick spec information about device",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}xspecs <codename>",
        "e": "{tr}xspecs whyred",
    },
)
async def _(event):
    "To get quick spec information about device"
    link = event.pattern_match.group(1)
    msg = f"/specs {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="fastboot ([\s\S]*)",
    command=("fastboot", plugin_category),
    info={
        "h": "To get latest fastboot MIUI.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}fastboot <codename>",
        "e": "{tr}fastboot whyred",
    },
)
async def _(event):
    "To get latest fastboot MIUI."
    link = event.pattern_match.group(1)
    msg = f"/fastboot {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="recovery ([\s\S]*)",
    command=("recovery", plugin_category),
    info={
        "h": "To get latest recovery MIUI.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}recovery <codename>",
        "e": "{tr}recovery whyred",
    },
)
async def _(event):
    "To get latest recovery MIUI."
    link = event.pattern_match.group(1)
    msg = f"/recovery {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="pb ([\s\S]*)",
    command=("pb", plugin_category),
    info={
        "h": "To get latest PBRP.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}pb <codename>",
        "e": "{tr}pb whyred",
    },
)
async def _(event):
    "To get latest PBRP."
    link = event.pattern_match.group(1)
    msg = f"/pb {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="of ([\s\S]*)",
    command=("of", plugin_category),
    info={
        "h": "To get latest OrangeFox Recovery.",
        "d": "Works for Xiaomi devices only",
        "u": "{tr}of <codename>",
        "e": "{tr}of whyred",
    },
)
async def _(event):
    "To get latest OrangeFox Recovery."
    link = event.pattern_match.group(1)
    msg = f"/of {link}"
    dogevent = await eor(event, "**⏳ Processing...**")
    await xiaomeme(event, msg, dogevent)
