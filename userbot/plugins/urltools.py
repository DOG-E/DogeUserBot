# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from requests import get
from validators.url import url

from . import doge, edl, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="dns(?:\s|$)([\s\S]*)",
    command=("dns", plugin_category),
    info={
        "h": "Verilen bağlantının Alan Adı Sistemini (dns) alır.",
        "u": "{tr}dns <url/yanıtlanan url>",
        "e": "{tr}dns google.com",
    },
)
async def _(event):
    "Verilen bağlantının Alan Adı Sistemini (dns) alır"
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "`Veri almak için bağlantıya yanıt verin veya girdi olarak bağlantı verin.`", 5
        )
    check = url(input_str)
    if not check:
        dogstr = "http://" + input_str
        check = url(dogstr)
    if not check:
        return await edl(event, "`Bu link desteklenmiyor.`", 5)
    sample_url = f"https://da.gd/dns/{input_str}"
    response_api = get(sample_url).text
    if response_api:
        await eor(event, f"DNS records of {input_str} are \n{response_api}")
    else:
        await eor(event, f"__I can't seem to find `{input_str}` on the internet__")


@doge.bot_cmd(
    pattern="short(?:\s|$)([\s\S]*)",
    command=("short", plugin_category),
    info={
        "h": "Verilen URL'yi kısaltır.",
        "u": "{tr}short <url/yanıtlanan url>",
        "e": "{tr}short https://github.com/DOG-E/DogeUserBot",
    },
)
async def _(event):
    "Verilen URL'yi kısaltır."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "`Veri almak için bağlantıya yanıt verin veya girdi olarak bağlantı verin.`", 5
        )
    check = url(input_str)
    if not check:
        dogstr = f"http://" + input_str
        check = url(dogstr)
    if not check:
        return await edl(event, "`verilen bağlantı desteklenmiyor.`", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    sample_url = f"https://da.gd/s?url={input_str}"
    response_api = get(sample_url).text
    if response_api:
        await eor(
            event, f"`{input_str}` bağlantısı kısaltıldı.\nYeni bağlantı: `{response_api}`", link_preview=False
        )
    else:
        await eor(event, "`Bir sorun var, lütfen daha sonra tekrar deneyin.`")


@doge.bot_cmd(
    pattern="unshort(?:\s|$)([\s\S]*)",
    command=("unshort", plugin_category),
    info={
        "h": "Verilen DagB kısaltılmış URL'sini alır.",
        "u": "{tr}unshort <url/yanıtlayarak url>",
        "e": "{tr}unshort https://da.gd/Doge",
    },
)
async def _(event):
    "Verilen DagB kısaltılmış URL'sini alır."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "`Veri almak için bağlantıya yanıt verin veya girdi olarak bağlantı verin.`", 5
        )
    check = url(input_str)
    if not check:
        dogstr = "http://" + input_str
        check = url(dogstr)
    if not check:
        return await edl(event, "`bu link desteklenmiyor.`", 5)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await eor(
            event,
            f"Giriş URL: `{input_str}`\nOrijinal URL: `{r.headers['Location']}`",
            link_preview=False,
        )
    else:
        await eor(
            event,
            "Giriş URL'si {}, durum_kodu {} ile iptal edildi".format(input_str, r.status_code),
        )


# By Priyam Kalra
@doge.bot_cmd(
    pattern="hl(?:\s|$)([\s\S]*)",
    command=("hl", plugin_category),
    info={
        "h": "URL'yi köprü kullanarak boşluklarla gizler.",
        "u": "{tr}hl <url/yanıtlayarak url>",
        "e": "{tr}hl https://da.gd/Doge",
    },
)
async def _(event):
    "URL'yi köprü kullanarak boşluklarla gizler."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edl(
            event, "`Veri almak için bağlantıya yanıt verin veya girdi olarak bağlantı verin`", 5
        )
    check = url(input_str)
    if not check:
        dogstr = "http://" + input_str
        check = url(dogstr)
    if not check:
        return await edl(event, "`link desteklenmiyor.`", 5)
    await eor(event, "[ㅤㅤㅤㅤㅤㅤㅤ](" + input_str + ")")
