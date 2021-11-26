# Credits: FridayUserBot
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from countryinfo import CountryInfo
from flag import flag

from . import doge, edl, eor

plugin_category = "misc"


@doge.bot_cmd(
    pattern="country ?([\s\S]*)",
    command=("country", plugin_category),
    info={
        "h": "Get information about any country",
        "u": "{tr}country <country name>",
        "e": "{tr}country Turkey",
    },
)
async def country_(message):
    await eor(message, "`Searching For Country.....`")
    lol = message.pattern_match.group(1)
    if not lol:
        return await edl(message, "`Please Give Input!`")

    country = CountryInfo(lol)
    try:
        a = country.info()
    except BaseException:
        return await edl(
            message, "`Country not found. Maybe you need to learn geography!`"
        )

    name = a.get("name")
    bb = a.get("altSpellings")
    hu = ""
    for p in bb:
        hu += p + ",  "
    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
        borders += fk + ",  "
    call = ""
    WhAt = a.get("callingCodes")
    for what in WhAt:
        call += what + "  "
    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
        currencies += FKer + ",  "
    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR = PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for zort in iSo:
        po = iSo.get(zort)
        iso += po + ",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag(nox)
    languages = a.get("languages")
    lMAO = ""
    for lmao in languages:
        lMAO += lmao + ",  "
    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom = ""
    for jerry in tik:
        tom += jerry + ",   "
    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
        lanester += targaryen + ",   "
    wiki = a.get("wiki")
    caption = f"""{okie} <b><u>Information of {name}</b></u>
<b>
Country Name: {name} {okie}
Alternative Spellings: {hu}
Country Area: {area} km²
Borders: {borders}
Calling Codes: {call}
Country's Capital: {capital}
Country's Currency: {currencies}
Demonym: {HmM}
Country Type: {EsCoBaR}
ISO Names: {iso}
Languages: {lMAO}
Native Name: {nonive}
Population: {waste}
Region: {reg}
Sub Region: {sub}
Time Zones: {tom}
Top Level Domain: {lanester}

Wikipedia:</b> <code>{wiki}</code>

🐶 <u><b>Information gathered by Doge</b></u>
"""
    await eor(message, caption, parse_mode="html")
