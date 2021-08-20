from PIL.Image import open as Imopen
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype as Imftruetype
from requests import get
from telegraph import upload_file
from validators.url import url


async def fakegs(search, result):
    imgurl = "https://i.imgur.com/wNFr5X2.jpg"
    with open("./temp/temp.jpg", "wb") as f:
        f.write(get(imgurl).content)
    img = Imopen("./temp/temp.jpg")
    drawing = Draw(img)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    font1 = Imftruetype(
        "userbot/helpers/resources/fonts/productsans_bolditalic.ttf", 20
    )
    font2 = Imftruetype("userbot/helpers/resources/fonts/productsans_light.ttf", 23)
    drawing.text((450, 258), result, fill=blue, font=font1)
    drawing.text((270, 37), search, fill=black, font=font2)
    img.save("./temp/temp.jpg")
    return "./temp/temp.jpg"


async def trumptweet(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def changemymind(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def kannagen(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def tweets(text1, text2):
    r = get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.webp", "webp")
    return "temp.webp"


async def iphonex(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def baguette(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def threats(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def lolice(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def awooify(text):
    r = get(f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phcomment(text1, text2, text3):
    r = get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}"
    ).json()
    teledoge = r.get("message")
    dogurl = url(teledoge)
    if not dogurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(get(teledoge).content)
    img = Imopen("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def magik(photo):
    Photo = await photo.download_media()
    uphoto = upload_file(Photo)
    r = get(
        f"https://nekobot.xyz/api/imagegen?type=magik&image=https://telegra.ph{uphoto[0]}"
    ).json()
    teledoge = r["message"]
    return teledoge
