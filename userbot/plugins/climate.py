# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from io import BytesIO
from json import loads

from aiohttp import ClientSession
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz
from requests import get

from . import _format, doge, eor, gvar, logging, reply_id, sgvar

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


# Get time zone of the given country. Credits: @aragon12 and @zakaryan2004.
async def get_tz(con):
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


def fahrenheit(f):
    temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
    return temp[0]


def celsius(c):
    temp = str((c - 273.15)).split(".")
    return temp[0]


def sun(unix, ctimezone):
    return datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")


@doge.bot_cmd(
    pattern="climate(?:\s|$)([\s\S]*)",
    command=("climate", plugin_category),
    info={
        "h": "Bir şehrin hava durumu raporunu alır.",
        "d": "Size bir şehrin hava raporunu gösterir. Varsayılan olarak İstanbul'dur, {tr}setcity komutu ile değiştirebilirsiniz.",
        "note": "Bu eklentinin çalışması için WEATHER_API değişkenini ayarlamanız gerekir, https://openweathermap.org/ adresinden değer alabilirsiniz.",
        "u": [
            "{tr}climate",
            "{tr}climate <Şehir İsmi>",
        ],
    },
)
async def get_weather(event):  # sourcery no-metrics
    "Bir şehrin hava durumu raporunu alır."
    # if WEATHER_API is None:
    # await eor(event, "`Get an API key from` https://openweathermap.org/ ``")
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    CITY = (gvar("WEATHER_CITY") or "Istanbul") if not input_str else input_str
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = f"{newcity[0].strip()},{newcity[1].strip()}"
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                return await eor(event, "`Geçersiz Ülke`")
            CITY = f"{newcity[0].strip()},{countrycode.strip()}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={(gvar('WEATHER_API') or '6fded1e1c5ef3f394283e3013a597879')}"
    async with ClientSession() as _session:
        async with _session.get(url) as request:
            requeststatus = request.status
            requesttext = await request.text()
    result = loads(requesttext)
    if requeststatus != 200:
        return await eor(event, "`Geçersiz Ülke.`")
    cityname = result["name"]
    curtemp = result["main"]["temp"]
    humidity = result["main"]["humidity"]
    min_temp = result["main"]["temp_min"]
    max_temp = result["main"]["temp_max"]
    pressure = result["main"]["pressure"]
    feel = result["main"]["feels_like"]
    desc = result["weather"][0]
    desc = desc["main"]
    country = result["sys"]["country"]
    sunrise = result["sys"]["sunrise"]
    sunset = result["sys"]["sunset"]
    wind = result["wind"]["speed"]
    winddir = result["wind"]["deg"]
    cloud = result["clouds"]["all"]
    ctimezone = tz(c_tz[country][0])
    time = datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    div = 360 / len(dirs)
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")
    await eor(
        event,
        f"🌡**Sıcaklık:** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        + f"🥰**Hissedilen** `{celsius(feel)}°C | {fahrenheit(feel)}°F`\n"
        + f"🥶**En Düşük Sıcaklık:** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        + f"🥵**En Yüksek Sıcaklık:** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"☁️**Nem:** `{humidity}%`\n"
        + f"🧧**Basınç** `{pressure} hPa`\n"
        + f"🌬**Rüzgar:** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
        + f"⛈**Bulut Oranı:** `{cloud} %`\n"
        + f"🌄**Gün Doğumu:** `{sun(sunrise,ctimezone)}`\n"
        + f"🌅**Gün Batımı:** `{sun(sunset,ctimezone)}`\n\n\n"
        + f"**{desc}**\n"
        + f"`{cityname}, {fullc_n}`\n"
        + f"`{time}`\n",
    )


@doge.bot_cmd(
    pattern="setcity(?:\s|$)([\s\S]*)",
    command=("setcity", plugin_category),
    info={
        "h": "Climate komutu için varsayılan şehri ayarlar.",
        "d": "Varsayılan şehrinizi ayarlar, böylece her seferinde şehir adını yazmanıza gerek kalmadan .weather veya .climate'ı istediğiniz zaman kullanabilirsiniz.",
        "note": "Bu eklentinin çalışması için WEATHER_API değişkenini ayarlamanız gerekir, https://openweathermap.org/ adresinden değer alabilirsiniz.",
        "u": [
            "{tr}climate",
            "{tr}climate <Şehir İsmi>",
        ],
    },
)
async def set_default_city(event):
    "Climate komutu için varsayılan şehri ayarlar."
    # if WEATHER_API is None:
    # await eor(event, "`Get an API key from` https://openweathermap.org/ ``")
    input_str = event.pattern_match.group(1)
    CITY = (gvar("WEATHER_CITY") or "Istanbul") if not input_str else input_str
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = f"{newcity[0].strip()},{newcity[1].strip()}"
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                return await eor(event, "`Geçersiz Ülke`")
            CITY = f"{newcity[0].strip()},{countrycode.strip()}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={(gvar('WEATHER_API') or '6fded1e1c5ef3f394283e3013a597879')}"
    request = get(url)
    result = loads(request.text)
    if request.status_code != 200:
        return await eor(event, "`Geçersiz Ülke.`")
    sgvar("WEATHER_CITY", CITY)
    cityname = result["name"]
    country = result["sys"]["country"]
    fullc_n = c_n[f"{country}"]
    await eor(event, f"`Varsayılan olay {cityname}, {fullc_n} olarak ayarlandı.`")


@doge.bot_cmd(
    pattern="weather(?:\s|$)([\s\S]*)",
    command=("weather", plugin_category),
    info={
        "h": "Bir şehrin hava durumu raporunu alır.",
        "d": "Size bir şehrin hava durumunu gösterir. Varsayılan olarak İstanbul'dur, {tr}setcity komutu ile değiştirebilirsiniz.",
        "u": [
            "{tr}weather",
            "{tr}weather <Şehir İsmi>",
        ],
    },
)
async def _(event):
    "'wttr.in'den bugün için hava durumu raporu"
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = gvar("WEATHER_CITY") or "Istanbul"
    output = get(f"https://wttr.in/{input_str}?mnTC0&lang=en").text
    await eor(event, output, parse_mode=_format.parse_pre)


@doge.bot_cmd(
    pattern="wttr(?:\s|$)([\s\S]*)",
    command=("wttr", plugin_category),
    info={
        "h": "Bir şehrin hava durumu raporunu alır.",
        "d": "Önümüzdeki 3 gün için bir şehrin hava durumunu gösterir. Varsayılan olarak İstanbul'dur, {tr}setcity komutu ile bunu değiştirebilirsiniz.",
        "u": [
            "{tr}wttr",
            "{tr}wttr <Şehir İsmi>",
        ],
    },
)
async def _(event):
    "'wttr.in'den sonraki 3 gün için hava durumu raporu"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = gvar("WEATHER_CITY") or "Istanbul"
    async with ClientSession() as session:
        sample_url = "https://wttr.in/{}.png"
        response_api_zero = await session.get(sample_url.format(input_str))
        response_api = await response_api_zero.read()
        with BytesIO(response_api) as out_file:
            await event.reply(
                f"**Şehir:** `{input_str}`", file=out_file, reply_to=reply_to_id
            )
    try:
        await event.delete()
    except Exception as e:
        LOGS.error(f"🚨 {str(e)}")
