# Credits to AsenaDev
# https://github.com/yusufusta/AsenaUserBot/blob/master/userbot/modules/covid19.py#L24

from requests import get
from pytz import country_names
from flag import flag

from . import doge, edl, eor, lan

plugin_category = "tool"


@doge.bot_cmd(
    pattern="covid(?:\s|$)([\s\S]*)",
    command=("covid", plugin_category),
    info={
        "header": "To get latest information about Covid-19.",
        "description": "Get information about Covid-19 data in the given country.",
        "usage": "{tr}covid <country_code>",
        "examples": [ "{tr}covid tr", "{tr}covid az"],
        "note": "If you don't write any country code, it will give Turkey statistics by default."
    },
)
async def corona(event):
    "To get latest information about Covid-19."
    try:
        if event.pattern_match.group(1) == '':
            country = 'TR'
        else: 
            country = event.pattern_match.group(1)
        dogevent = await eor(event, lan("processing"))
        fl = flag(country)
        worldData = get('https://coronavirus-19-api.herokuapp.com/all').json()
        countryData = get('https://coronavirus-19-api.herokuapp.com/countries/' + country_names[country]).json()
    except:
        return await edl(dogevent, 'An error has occurred.')

    case=worldData['cases']
    death=worldData['deaths']
    recover=worldData['recovered']
    cname=country_names[country]
    ccase=countryData['cases']
    ctcase=countryData['todayCases']
    cactive=countryData['active']
    cdeath=countryData['deaths']
    ctdeath=countryData['todayDeaths']
    crecover=countryData['recovered']
    cttest=countryData['totalTests']

    covidresult = (
    f"**CᴏʀᴏɴᴀVɪʀᴜs Dᴀᴛᴀ**\n\
        \n**World**\n\
        **🌎 Case:** `{case}`\n\
        **🌎 Death:** `{death}`\n\
        **🌎 Heal:** `{recover}`\n\
        \n**{cname}**\n\
        **{fl} Case (total):** `{ccase}`\n\
        **{fl} Case (today):** `{ctcase}`\n\
        **{fl} Case (active):** `{cactive}`\n\
        **{fl} Death (total):** `{cdeath}`\n\
        **{fl} Death (today):** `{ctdeath}`\n\
        **{fl} Heal:** `{crecover}`\n\
        **{fl} Test (total):** `{cttest}`"
    )

    await eor(dogevent, covidresult)
