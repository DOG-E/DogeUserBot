# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from calendar import month
from datetime import datetime as dt
from os import makedirs, path, remove

from PIL.Image import new
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from . import TEMP_DIR, Config, doge, edl, eor, reply_id, tr

plugin_category = "tool"

FONT_FILE_TO_USE = "userbot/helpers/resources/fonts/spacemono_regular.ttf"


async def get_tz(con):
    """Get time zone of the given country."""
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Western)", "(western)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Minor Outlying Islands", "minor outlying islands")
    if "Nl" in con:
        con = con.replace("Nl", "NL")
    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return


@doge.bot_cmd(
    pattern="ctime(?:\s|$)([\s\S]*)(?<![0-9])(?: |$)([0-9]+)?",
    command=("ctime", plugin_category),
    info={
        "h": "To get current time of a paticular country",
        "note": "For country names check [this link](https://telegra.ph/country-names-10-24)",  # TODO
        "u": "{tr}ctime <country name/code> <timezone number>",
        "e": "{tr}ctime Brazil 2",
    },
)
async def time_func(tdata):
    """To get current time of a paticular country"""
    con = tdata.pattern_match.group(1).title()
    tz_num = tdata.pattern_match.group(2)
    t_form = "%H:%M"
    d_form = "%d/%m/%y - %A"
    c_name = ""
    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif Config.COUNTRY:
        c_name = Config.COUNTRY
        tz_num = Config.TZ_NUMBER
        timezones = await get_tz(Config.COUNTRY)
    else:
        return await eor(
            tdata,
            f"`It's`  **{dt.now().strftime(t_form)}**` on `**{dt.now().strftime(d_form)}** `here.`",
        )

    if not timezones:
        return await eor(tdata, "`Invaild country.`")

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n\n"
            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"
            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"`Example: {tr}ctime {c_name} 2`"
            return await eor(tdata, return_str)

    dtnow1 = dt.now(tz(time_zone)).strftime(t_form)
    dtnow2 = dt.now(tz(time_zone)).strftime(d_form)
    if c_name != Config.COUNTRY:
        await eor(
            tdata,
            f"`It's`  **{dtnow1}**` on `**{dtnow2}**  `in {c_name} ({time_zone} timezone).`",
        )
    if Config.COUNTRY:
        await eor(
            tdata,
            f"`It's`  **{dtnow1}**` on `**{dtnow2}**  `here, in {Config.COUNTRY}"
            f"({time_zone} timezone).`",
        )


@doge.bot_cmd(
    pattern="time(?:\s|$)([\s\S]*)",
    command=("time", plugin_category),
    info={
        "h": "To show current time.",
        "d": "shows current default time you can change by changing TZ in heroku vars.",
        "u": "{tr}time",
    },
)
async def _(event):
    "To show current time"
    reply_msg_id = await reply_id(event)
    current_time = dt.now().strftime(
        f"⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n⚡USERBOT TIMEZONE⚡\n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n   {path.basename(Config.TZ)}\n  Time: %H:%M:%S \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
    )
    input_str = event.pattern_match.group(1)
    if input_str:
        current_time = input_str
    if not path.isdir(TEMP_DIR):
        makedirs(TEMP_DIR)
    required_file_name = TEMP_DIR + " " + str(dt.now()) + ".webp"
    img = new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = truetype(FONT_FILE_TO_USE, 30)
    drawn_text = Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await event.client.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
    )
    remove(required_file_name)
    await event.delete()


@doge.bot_cmd(
    pattern="calendar ([\s\S]*)",
    command=("calendar", plugin_category),
    info={
        "h": "To get calendar of given month and year.",
        "u": "{tr}calendar year ; month",
        "e": "{tr}calendar 2021 ; 5",
    },
)
async def _(event):
    "To get calendar of given month and year."
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(";")
    if len(input_sgra) != 2:
        return await edl(event, "**Syntax:** `.calendar year ; month`", 5)

    yyyy = input_sgra[0]
    mm = input_sgra[1]
    try:
        output_result = month(int(yyyy.strip()), int(mm.strip()))
        await eor(event, f"```{output_result}```")
    except Exception as e:
        await edl(event, f"**Error:**\n`{e}`", 5)
