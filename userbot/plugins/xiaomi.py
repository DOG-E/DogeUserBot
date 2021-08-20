# created by @eve_enryu
# edited & fix by @Jisan7509

from . import doge, eor, lan, xiaomeme

plugin_category = "tool"


@doge.bot_cmd(
    pattern="firmware ([\s\S]*)",
    command=("firmware", plugin_category),
    info={
        "header": "To get lastest Firmware.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}firmware <codename>",
        "examples": "{tr}firmware whyred",
    },
)
async def _(event):
    "To get lastest Firmware."
    link = event.pattern_match.group(1)
    msg = f"/firmware {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="vendor ([\s\S]*)",
    command=("vendor", plugin_category),
    info={
        "header": "To get lastest Vendor.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}vendor <codename>",
        "examples": "{tr}vendor whyred",
    },
)
async def _(event):
    "To get lastest Vendor."
    link = event.pattern_match.group(1)
    msg = f"/vendor {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="xspecs ([\s\S]*)",
    command=("xspecs", plugin_category),
    info={
        "header": "To get quick spec information about device",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}xspecs <codename>",
        "examples": "{tr}xspecs whyred",
    },
)
async def _(event):
    "To get quick spec information about device"
    link = event.pattern_match.group(1)
    msg = f"/specs {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="fastboot ([\s\S]*)",
    command=("fastboot", plugin_category),
    info={
        "header": "To get latest fastboot MIUI.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}fastboot <codename>",
        "examples": "{tr}fastboot whyred",
    },
)
async def _(event):
    "To get latest fastboot MIUI."
    link = event.pattern_match.group(1)
    msg = f"/fastboot {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="recovery ([\s\S]*)",
    command=("recovery", plugin_category),
    info={
        "header": "To get latest recovery MIUI.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}recovery <codename>",
        "examples": "{tr}recovery whyred",
    },
)
async def _(event):
    "To get latest recovery MIUI."
    link = event.pattern_match.group(1)
    msg = f"/recovery {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="pb ([\s\S]*)",
    command=("pb", plugin_category),
    info={
        "header": "To get latest PBRP.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}pb <codename>",
        "examples": "{tr}pb whyred",
    },
)
async def _(event):
    "To get latest PBRP."
    link = event.pattern_match.group(1)
    msg = f"/pb {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="of ([\s\S]*)",
    command=("of", plugin_category),
    info={
        "header": "To get latest OrangeFox Recovery.",
        "description": "Works for Xiaomi devices only",
        "usage": "{tr}of <codename>",
        "examples": "{tr}of whyred",
    },
)
async def _(event):
    "To get latest OrangeFox Recovery."
    link = event.pattern_match.group(1)
    msg = f"/of {link}"
    dogevent = await eor(event, lan("processing"))
    await xiaomeme(event, msg, dogevent)
