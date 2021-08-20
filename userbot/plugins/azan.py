# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py
from json import loads

from requests import get

from . import doge, edl, eor, gvarstatus

plugin_category = "tool"


@doge.bot_cmd(
    pattern="[ae]zan(?:\s|$)([\s\S]*)",
    command=("ezan", plugin_category),
    info={
        "header": "Shows you the Islamic prayer times of the given city name.",
        "note": "You can set default city by using `{tr}setcity` command.",
        "usage": ["{tr}azan <city name>", "{tr}ezan <city name>",],
        "examples": ["{tr}azan hyderabad", "{tr}ezan istanbul",],
    },
)
async def get_adzan(adzan):
    "Shows you the Islamic prayer times of the given city name"
    input_str = adzan.pattern_match.group(1)
    LOKASI = gvarstatus("DEFCITY") or "Istanbul" if not input_str else input_str
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = get(url)
    if request.status_code != 200:
        return await edl(adzan, f"`Couldn't fetch any data about the city {LOKASI}`")
    result = loads(request.text)
    dogresult = f"<b>Islamic prayer times </b>\
            \n\
            \n<b>City         : </b><i>{result['query']}</i>\
            \n<b>Country: </b><i>{result['country']}</i>\
            \n<b>Date       : </b><i>{result['items'][0]['date_for']}</i>\
            \n<b>Fajr         : </b><i>{result['items'][0]['fajr']}</i>\
            \n<b>Shurooq: </b><i>{result['items'][0]['shurooq']}</i>\
            \n<b>Dhuhr    : </b><i>{result['items'][0]['dhuhr']}</i>\
            \n<b>Asr           : </b><i>{result['items'][0]['asr']}</i>\
            \n<b>Maghrib: </b><i>{result['items'][0]['maghrib']}</i>\
            \n<b>Isha         : </b><i>{result['items'][0]['isha']}</i>\
    "
    await eor(adzan, dogresult, "html")
