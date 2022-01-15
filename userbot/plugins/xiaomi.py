# Credits: @eve_enryu
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import doge, eor, xiaomeme

plugin_category = "tool"


@doge.bot_cmd(
    pattern="firmware ([\s\S]*)",
    command=("firmware", plugin_category),
    info={
        "h": "En son Firmware'i alır.",
        "d": "Yalnızca Xiaomi cihazları için çalışır.",
        "u": "{tr}firmware <kod adı>",
        "e": "{tr}firmware whyred",
    },
)
async def _(event):
    "En son Firmware'i alır."
    link = event.pattern_match.group(1)
    msg = f"/firmware {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="vendor ([\s\S]*)",
    command=("vendor", plugin_category),
    info={
        "h": "En son Vendoru alır.",
        "d": "Yalnızca Xiaomi cohazları için çalışır.",
        "u": "{tr}vendor <kod adı>",
        "e": "{tr}vendor whyred",
    },
)
async def _(event):
    "En son Vendor'u alır."
    link = event.pattern_match.group(1)
    msg = f"/vendor {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="xspecs ([\s\S]*)",
    command=("xspecs", plugin_category),
    info={
        "h": "Cihaz özellikleri hakkında bilgi alır.",
        "d": "Yalnızca Xiaomi cihazlarında çalışır.",
        "u": "{tr}xspecs <kod adı>",
        "e": "{tr}xspecs whyred",
    },
)
async def _(event):
    "Cihaz özellikleri hakkında bilgi alır."
    link = event.pattern_match.group(1)
    msg = f"/specs {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="fastboot ([\s\S]*)",
    command=("fastboot", plugin_category),
    info={
        "h": "En son fastboot MIUI'yı alır.",
        "d": "Yalnızca Xiaomi cihazlarında çalışır.",
        "u": "{tr}fastboot <kod adı>",
        "e": "{tr}fastboot whyred",
    },
)
async def _(event):
    "En son fastboot MIUI'yı alır."
    link = event.pattern_match.group(1)
    msg = f"/fastboot {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="recovery ([\s\S]*)",
    command=("recovery", plugin_category),
    info={
        "h": "En son recovery MIUI'yı alır.",
        "d": "Yalnızca Xiaomi cihazlarında çalışır.",
        "u": "{tr}recovery <kod adı>",
        "e": "{tr}recovery whyred",
    },
)
async def _(event):
    "En son recovery MIUI'yı alır."
    link = event.pattern_match.group(1)
    msg = f"/recovery {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="pb ([\s\S]*)",
    command=("pb", plugin_category),
    info={
        "h": "En son PitchBlack Recovery'i alır.",
        "d": "Yalnızca Xiaomi cihazlarlnda çalışır.",
        "u": "{tr}pb <kod adı>",
        "e": "{tr}pb whyred",
    },
)
async def _(event):
    "En son PitchBlack Recovery'i alır."
    link = event.pattern_match.group(1)
    msg = f"/pb {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)


@doge.bot_cmd(
    pattern="of ([\s\S]*)",
    command=("of", plugin_category),
    info={
        "h": "En son OrangeFox Recovery'yi alır.",
        "d": "Yalnızca Xiaomi cihazlarında çalışır.",
        "u": "{tr}of <kod adı>",
        "e": "{tr}of whyred",
    },
)
async def _(event):
    "En son OrangeFox Recovery'yi alır."
    link = event.pattern_match.group(1)
    msg = f"/of {link}"
    dogevent = await eor(event, "**⏳ İşleniyor...**")
    await xiaomeme(event, msg, dogevent)
