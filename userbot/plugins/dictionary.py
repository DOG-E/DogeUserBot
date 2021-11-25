# Credits: @mrconfused
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary
from requests import get

from . import AioHttp, _format, doge, edl, eor, getSimilarWords, logging

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


@doge.bot_cmd(
    pattern="ud ([\s\S]*)",
    command=("ud", plugin_category),
    info={
        "header": "To fetch meaning of the given word from Urban dictionary.",
        "usage": "{tr}ud <word>",
    },
)
async def ud(event):
    "To fetch meaning of the given word from urban dictionary."
    word = event.pattern_match.group(1)
    try:
        response = await AioHttp().get_json(
            f"http://api.urbandictionary.com/v0/define?term={word}",
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        result = "**Text: {}**\n**Meaning:**\n`{}`\n\n**Example:**\n`{}`".format(
            _format.replacetext(word),
            _format.replacetext(definition),
            _format.replacetext(example),
        )
        await eor(event, result)
    except Exception as e:
        await edl(
            event,
            text="`The Urban Dictionary API could not be reached`",
        )
        LOGS.info(e)


@doge.bot_cmd(
    pattern="meaning ([\s\S]*)",
    command=("meaning", plugin_category),
    info={
        "header": "To fetch meaning of the given word from dictionary.",
        "usage": "{tr}meaning <word>",
    },
)
async def meaning(event):
    "To fetch meaning of the given word from dictionary."
    word = event.pattern_match.group(1)
    dictionary = PyDictionary()
    dog = dictionary.meaning(word)
    output = f"**Word:** __{word}__\n\n"
    try:
        for a, b in dog.items():
            output += f"**{a}**\n"
            for i in b:
                output += f"☞__{i}__\n"
        await eor(event, output)
    except Exception:
        await eor(event, f"Couldn't fetch meaning of {word}")


# TDK & Tureng coded @By_Azade ported from Asena - github.com/yusufusta/asenauserbot
@doge.bot_cmd(
    pattern="tdk ?([\s\S]*)",
    command=("tdk", plugin_category),
    info={
        "header": "To fetch meaning of the given word from Turkish dictionary. Only Turkish.",
        "usage": "{tr}tdk <word>",
    },
)
async def tdk(event):
    inp = event.pattern_match.group(1)
    dogevent = await eor(event, "__Searching...__")
    response = get(f"https://sozluk.gov.tr/gts?ara={inp}").json()
    if "error" in response:
        await edl(dogevent, f"**I couldn't find ({inp}) in Turkish dictionary.**")
        words = getSimilarWords(inp)
        if not words == "":
            return await edl(
                dogevent,
                f"__I couldn't find ({inp}) in Turkish dictionary.__\n\n**Similar Words:** {words}",
                30,
            )
    else:
        meaningsStr = ""
        for mean in response[0]["anlamlarListe"]:
            meaningsStr += f"\n**{mean['anlam_sira']}.**"
            if ("ozelliklerListe" in mean) and (
                (not mean["ozelliklerListe"][0]["tam_adi"] is None)
                or (not mean["ozelliklerListe"][0]["tam_adi"] == "")
            ):
                meaningsStr += f"__({mean['ozelliklerListe'][0]['tam_adi']})__"
            meaningsStr += f' ```{mean["anlam"]}```'

            if response[0]["cogul_mu"] == "0":
                cogul = "❌"
            else:
                cogul = "✅"

            if response[0]["ozel_mi"] == "0":
                ozel = "❌"
            else:
                ozel = "✅"

        await eor(
            dogevent,
            f"**Word:** `{inp}`\n\n**Is the plural?:** {cogul}\n**Is the word a proper noun?:** {ozel}\n\n**Meanings:** {meaningsStr}",
        )
        words = getSimilarWords(inp)
        if not words == "":
            return dogevent.edit(
                f"**Word:** `{inp}`\n\n**Is the plural?:** `{cogul}`\n**Is the word a proper noun?:** {ozel}\n\n**Meanings:** {meaningsStr}\n\n**Similar Words:** {words}",
            )


@doge.bot_cmd(
    pattern="tureng ?([\s\S]*)",
    command=("tureng", plugin_category),
    info={
        "header": "To fetch meaning of the given word from Tureng dictionary. Only Turkish.",
        "usage": "{tr}tureng <word>",
    },
)
async def tureng(event):
    word = event.pattern_match.group(1)
    url = "https://tureng.com/tr/turkce-ingilizce/" + word
    try:
        answer = get(url)
    except BaseException:
        return await edl(event, "No connection")
    soup = BeautifulSoup(answer.content, "html.parser")
    trlated = "The meaning of the word {}:\n\n".format(word)
    try:
        table = soup.find("table")
        td = table.find_all("td", attrs={"lang": "en"})
        for val in td[0:5]:
            trlated = "{} 👉 {}\n".format(trlated, val.text)
        await eor(event, trlated)
    except BaseException:
        await edl(event, "I couldn't find the result")
