# @DogeUserBot - < https://t.me/DogeUserBot > 
# Copyright (C) 2021 - DOG-E 
# Tüm hakları saklıdır. 
# 
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır. 
# Lütfen GNU Affero Genel Kamu Lisansını okuyun; 
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ > 
# ================================================================ 
from json import loads 
from re import findall 
 
from bs4 import BeautifulSoup 
from requests import get 
 
from . import doge, edl, eor, tr 
 
plugin_category = "tool" 
 
 
@doge.bot_cmd( 
    pattern="magisk$", 
    command=("magisk", plugin_category), 
    info={ 
        "h": "En son Magisk sürümlerini alın", 
        "u": "{tr}magisk", 
    }, 
) 
async def kakashi(event): 
    "En son Magisk sürümlerini alın" 
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/" 
    magisk_dict = { 
        "⦁ Stabil": magisk_repo + "master/stable.json", 
        "⦁ Beta": magisk_repo + "master/beta.json", 
        "⦁ Canary": magisk_repo + "master/canary.json", 
    } 
    releases = "**En son magisk sürümleri**\n\n" 
    for name, release_url in magisk_dict.items(): 
        data = get(release_url).json() 
        releases += ( 
            f'{name}: [APK v{data["magisk"]["versiyon"]}]({data["magisk"]["link"]}) | ' 
            f'[Değişiklikler]({data["magisk"]["note"]})\n' 
        ) 
    await eor(event, releases) 
 
 
@doge.bot_cmd( 
    pattern="device(?: |$)(\S*)", 
    command=("device", plugin_category), 
    info={ 
        "h": "Android cihaz adını/modelini kod_adı'ndan almak için Doge eklentisi", 
        "u": "{tr}device <kod_adı>", 
        "e": "{tr}device whyred", 
    }, 
) 
async def device_info(event): 
    "Kod adından Android cihaz adını al" 
    textx = await event.get_reply_message() 
    codename = event.pattern_match.group(1) 
    if not codename: 
        if textx: 
            codename = textx.text 
        else: 
            return await edl(event, f"Kullanım: {tr}device <kod_adı> veya <model>") 
    data = loads( 
        get( 
            "https://raw.githubusercontent.com/androidtrackers/" 
            "certified-android-devices/master/by_device.json" 
        ).text 
    ) 
    results = data.get(codename) 
    if results: 
        reply = f"**{codename} için arama sonucu:**\n\n" 
        for item in results: 
            reply += ( 
                f"**Marka:** {item['brand']}\n" 
                f"**Ad:** {item['name']}\n" 
                f"**Model:** {item['model']}\n\n" 
            ) 
    else: 
        reply = f"{codename} hakkında bilgi yok!\n" 
    await eor(event, reply) 
 
 
@doge.bot_cmd( 
    pattern="dcname(?: |)([\S]*)(?: |)([\s\S]*)", 
    command=("dcname", plugin_category), 
    info={ 
        "h": "To Search for android device codename", 
        "u": "{tr}dcname <brand> <device>", 
        "e": "{tr}dcname Xiaomi Redmi Note 5 Pro", 
    }, 
)
async def codename_info(event): 
    textx = await event.get_reply_message() 
    brand = event.pattern_match.group(1).lower() 
    device = event.pattern_match.group(2).lower() 
 
    if brand and device: 
        pass 
    elif textx: 
        brand = textx.text.split(" ")[0] 
        device = " ".join(textx.text.split(" ")[1:]) 
    else: 
        return await edl(event, f"Usage: {tr}dcname <marka> <cihaz>") 
 
    data = loads( 
        get( 
            "https://raw.githubusercontent.com/androidtrackers/" 
            "certified-android-devices/master/by_brand.json" 
        ).text 
    ) 
    devices_lower = {k.lower(): v for k, v in data.items()} 
    devices = devices_lower.get(brand) 
    if not devices: 
        return await eor(event, f"__I couldn't find {brand}.__") 
    results = [ 
        i 
        for i in devices 
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower() 
    ] 
    if results: 
        reply = f"**{brand} {device} için arama sonucu:**\n\n" 
        if len(results) > 8: 
            results = results[:8] 
        for item in results: 
            reply += ( 
                f"**Cihaz:** {item['device']}\n" 
                f"**Ad:** {item['name']}\n" 
                f"**Model:** {item['model']}\n\n" 
            ) 
    else: 
        reply = f"{device} için kod adı bulunamadı!\n" 
    await eor(event, reply) 
 
 
@doge.bot_cmd( 
    pattern="specs(?: |)([\S]*)(?: |)([\s\S]*)", 
    command=("specs", plugin_category), 
    info={ 
        "h": "Android cihazı hakkında bilgi almak için.", 
        "u": "{tr}specs", 
        "e": "{tr}specs Xiaomi Redmi Note 5 Pro", 
    }, 
) 
async def devices_specifications(event): 
    "Mobil cihaz özellikleri" 
    textx = await event.get_reply_message() 
    brand = event.pattern_match.group(1).lower() 
    device = event.pattern_match.group(2).lower() 
    if brand and device: 
        pass 
    elif textx: 
        brand = textx.text.split(" ")[0] 
        device = " ".join(textx.text.split(" ")[1:]) 
    else: 
        return await edl(event, f"Usage: {tr}specs <marka> <cihaz>") 
    all_brands = ( 
        BeautifulSoup( 
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml" 
        ) 
        .find("div", {"class": "brand-listing-container-news"}) 
        .findAll("a") 
    ) 
    brand_page_url = None 
    try: 
        brand_page_url = [ 
            i["href"] for i in all_brands if brand == i.text.strip().lower() 
        ][0] 
    except IndexError: 
        return await edl(event, f"{brand} bilinmeyen bir marka!") 
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll( 
        "div", {"class": "model-listing-container-80"} 
    ) 
    device_page_url = None 
    try: 
        device_page_url = [ 
            i.a["href"] 
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3") 
            if device in i.text.strip().lower() 
        ] 
    except IndexError: 
        return await edl(event, f"{device} bulunamadı!") 
    if len(device_page_url) > 2: 
        device_page_url = device_page_url[:2] 
    reply = "" 
    for url in device_page_url: 
        info = BeautifulSoup(get(url).content, "lxml") 
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n" 
        info = info.find("div", {"id": "model-brief-specifications"}) 
        specifications = findall(r"<b>.*?<br/>", str(info)) 
        for item in specifications:
            title = findall(r"<b>(.*?)</b>", item)[0].strip()
            data = ( 
                findall(r"</b>: (.*?)<br/>", item)[0] 
                .replace("<b>", "") 
                .replace("</b>", "") 
                .strip() 
            ) 
            reply += f"**{title}:** {data}\n"
    await eor(event, reply)


@doge.bot_cmd( 
    pattern="twrp(?: |$)(\S*)", 
    command=("twrp", plugin_category), 
    info={ 
        "h": "Android cihaz için en son twrp indirme bağlantılarını almak için.", 
        "u": "{tr}twrp <cihaz> <kod adı>", 
        "e": "{tr}twrp whyred", 
    }, 
) 
async def twrp(event): 
    "get android device twrp" 
    textx = await event.get_reply_message() 
    device = event.pattern_match.group(1) 
    if device: 
        pass 
    elif textx: 
        device = textx.text.split(" ")[0] 
    else: 
        return await edl(event, f"Kullanım: {tr}twrp <cihaz> <kod adı>") 
    url = get(f"https://dl.twrp.me/{device}/") 
    if url.status_code == 404: 
        reply = f"{device} için twrp indirmeleri bulunamadı!\n" 
        return await edl(event, reply) 
    page = BeautifulSoup(url.content, "lxml") 
    download = page.find("table").find("tr").find("a") 
    dl_link = f"https://dl.twrp.me{download['href']}" 
    dl_file = download.text 
    size = page.find("span", {"class": "filesize"}).text 
    date = page.find("em").text.strip() 
    reply = ( 
        f"**{device} için en son TWRP**\n" 
        f"[{dl_file}]({dl_link}) - {size}\n" 
        f"**Güncellendi:** {date}\n" 
    ) 
    await eor(event, reply)
