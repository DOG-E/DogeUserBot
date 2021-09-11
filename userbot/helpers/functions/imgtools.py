# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from io import BytesIO
from os import getcwd, remove
from os.path import join
from random import choice, randint, uniform
from string import hexdigits
from textwrap import wrap

from colour import Color as colour
from numpy import array, asarray, mean, sum
from PIL import Image
from PIL.ImageColor import getcolor
from PIL.ImageDraw import Draw
from PIL.ImageEnhance import Brightness, Contrast, Sharpness
from PIL.ImageFilter import GaussianBlur
from PIL.ImageFont import load_default, truetype
from PIL.ImageOps import colorize
from PIL.ImageOps import crop as IOcrop
from PIL.ImageOps import expand, flip
from PIL.ImageOps import grayscale as IOgrayscale
from PIL.ImageOps import invert, mirror, posterize
from PIL.ImageOps import solarize as IOsolarize
from scipy.ndimage import gaussian_gradient_magnitude
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image as wandimage
from wordcloud import ImageColorGenerator, WordCloud


def get_warp_length(width):
    return int((20.0 / 1024.0) * (width + 0.0))


def random_color():
    number_of_colors = 2
    return [
        "#" + "".join(choice("0123456789ABCDEF") for j in range(6))
        for i in range(number_of_colors)
    ]


def convert_toimage(image, filename=None):
    filename = filename or join("./temp/", "temp.jpg")
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filename, "jpeg")
    remove(image)
    return filename


def convert_tosticker(response, filename=None):
    filename = filename or join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    remove(response)
    return filename


# https://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging/38378828
async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = invert(image)
    inverted_image.save(endname)


async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = flip(image)
    inverted_image.save(endname)


async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = IOgrayscale(image)
    inverted_image.save(endname)


async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = mirror(image)
    inverted_image.save(endname)


async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = IOsolarize(image, threshold=128)
    inverted_image.save(endname)


async def add_frame(imagefile, endname, x, color):
    image = Image.open(imagefile)
    inverted_image = expand(image, border=x, fill=color)
    inverted_image.save(endname)


async def crop(imagefile, endname, x):
    image = Image.open(imagefile)
    inverted_image = IOcrop(image, border=x)
    inverted_image.save(endname)


async def crop_and_divide(img):
    (width, height) = img.size
    rows = 5
    columns = 5
    scale_width = width // columns
    scale_height = height // rows
    if (scale_width * columns, scale_height * rows) != (width, height):
        img = img.resize((scale_width * columns, scale_height * rows))
    (new_width, new_height) = (0, 0)
    media = []
    for _ in range(1, rows + 1):
        for o in range(1, columns + 1):
            mimg = img.crop(
                (
                    new_width,
                    new_height,
                    new_width + scale_width,
                    new_height + scale_height,
                )
            )
            mimg = mimg.resize((512, 512))
            image = BytesIO()
            image.name = "DogeUserBot.png"
            mimg.save(image, "PNG")
            media.append(image.getvalue())
            new_width += scale_width
        new_width = 0
        new_height += scale_height
    return media


def cirsle(im, x, y, r, fill):
    x += r // 2
    y += r // 2
    draw = Draw(im)
    draw.ellipse((x - r, y - r, x + r, y + r), fill)
    return im


async def dotify(image, pix, mode):
    count = 24
    im_ = Image.open(image)
    if im_.mode == "RGBA":
        temp = Image.new("RGB", im_.size, "#000")
        temp.paste(im_, (0, 0), im_)
        im_ = temp
    im = im_.convert("L")
    im_ = im if mode else im_
    w, h = im.size
    img = Image.new(im_.mode, (w * count + (count // 2), h * count + (count // 2)), 0)
    Draw(img)
    _x = _y = count // 2
    for x in range(w):
        for y in range(h):
            r = im.getpixel((x, y))
            fill = im_.getpixel((x, y))
            cirsle(img, _x, _y, r // count, fill)
            _y += count
        _x += count
        _y = count // 2
    out = BytesIO()
    out.name = "DogeUserBot.png"
    img.save(out)
    out.seek(0)
    return out


def asciiart(in_f, SC, GCF, out_f, color1, color2, bgcolor="black"):
    chars = asarray(list(" .,:irs?@9B&#"))
    font = load_default()
    letter_width = font.getsize("x")[0]
    letter_height = font.getsize("x")[1]
    WCF = letter_height / letter_width
    img = Image.open(in_f)
    widthByLetter = round(img.size[0] * SC * WCF)
    heightByLetter = round(img.size[1] * SC)
    S = (widthByLetter, heightByLetter)
    img = img.resize(S)
    img = sum(asarray(img), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)
    lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")
    nbins = len(lines)
    colorRange = list(colour(color1).range_to(colour(color2), nbins))
    newImg_width = letter_width * widthByLetter
    newImg_height = letter_height * heightByLetter
    newImg = Image.new("RGBA", (newImg_width, newImg_height), bgcolor)
    draw = Draw(newImg)
    leftpadding = 0
    y = 0
    for lineIdx, line in enumerate(lines):
        color = colorRange[lineIdx]
        draw.text((leftpadding, y), line, color.hex, font=font)
        y += letter_height
    if newImg.mode != "RGB":
        newImg = newImg.convert("RGB")
    newImg.save(out_f)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )
    img = img.copy().convert("RGB")
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = posterize(img, randint(3, 7))
    overlay = img.split()[0]
    overlay = Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = colorize(overlay, colours[0], colours[1])
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = Sharpness(img).enhance(randint(5, 300))
    return img


async def pframehelper(image):
    wid, hgt = image.size
    img = Image.new("RGBA", (wid, hgt))
    scale = min(wid // 100, hgt // 100)
    temp = Image.new("RGBA", (wid + scale * 40, hgt + scale * 40), "#fff")
    if image.mode == "RGBA":
        img.paste(image, (0, 0), image)
        newimg = Image.new("RGBA", (wid, hgt))
        for N in range(wid):
            for O in range(hgt):
                if img.getpixel((N, O)) != (0, 0, 0, 0):
                    newimg.putpixel((N, O), (0, 0, 0))
    else:
        img.paste(image, (0, 0))
        newimg = Image.new("RGBA", (wid, hgt), "black")
    newimg = newimg.resize((wid + scale * 5, hgt + scale * 5))
    temp.paste(
        newimg,
        ((temp.width - newimg.width) // 2, (temp.height - newimg.height) // 2),
        newimg,
    )
    temp = temp.filter(GaussianBlur(scale * 5))
    temp.paste(
        img, ((temp.width - img.width) // 2, (temp.height - img.height) // 2), img
    )
    output = BytesIO()
    output.name = (
        "-".join(
            "".join(choice(hexdigits) for img in range(event))
            for event in [5, 4, 3, 2, 1]
        )
        + ".png"
    )
    temp.save(output, "PNG")
    output.seek(0)
    return output


async def dogememify_helper(CNG_FONTS, topString, bottomString, filename, endname):
    img = Image.open(filename)
    imageSize = img.size
    fontSize = int(imageSize[1] / 5)
    font = truetype(CNG_FONTS, fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize -= 1
        font = truetype(CNG_FONTS, fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = Draw(img)
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text(
                (topTextPosition[0] + x, topTextPosition[1] + y),
                topString,
                (0, 0, 0),
                font=font,
            )
            draw.text(
                (bottomTextPosition[0] + x, bottomTextPosition[1] + y),
                bottomString,
                (0, 0, 0),
                font=font,
            )
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save(endname)


async def dogememifyhelper(upper_text, lower_text, CNG_FONTS, picture_name, endname):
    main_image = wandimage(filename=picture_name)
    main_image.resize(
        1024, int(((main_image.height * 1.0) / (main_image.width * 1.0)) * 1024.0)
    )
    upper_text = "\n".join(wrap(upper_text, get_warp_length(main_image.width))).upper()
    lower_text = "\n".join(wrap(lower_text, get_warp_length(main_image.width))).upper()
    MARGINS = [50, 150, 250, 350, 450]
    lower_margin = MARGINS[lower_text.count("\n")]
    text_draw = Drawing()
    text_draw.font = join(getcwd(), CNG_FONTS)
    text_draw.font_size = 100
    text_draw.text_alignment = "center"
    text_draw.stroke_color = Color("black")
    text_draw.stroke_width = 3
    text_draw.fill_color = Color("white")
    if upper_text:
        text_draw.text((main_image.width) // 2, 80, upper_text)
    if lower_text:
        text_draw.text(
            (main_image.width) // 2, main_image.height - lower_margin, lower_text
        )
    text_draw(main_image)
    main_image.save(filename=endname)


def higlighted_text(
    input_img,
    text,
    output_img,
    background="black",
    foreground="white",
    transparency=255,
    align="center",
    direction=None,
    text_wrap=2,
    font_name=None,
    font_size=60,
    linespace="+2",
    rad=20,
    position=(0, 0),
):
    templait = Image.open(input_img)
    source_img = templait.convert("RGBA").resize((1024, 1024))
    w, h = source_img.size
    if font_name is None:
        font_name = "userbot/helpers/resources/fonts/impact.ttf"
    font = truetype(font_name, font_size)
    ew, eh = position
    tw, th = font.getsize(text)
    width = 50 + ew
    hight = 30 + eh
    mask_size = int((w / text_wrap) + 50)
    input_text = "\n".join(wrap(text, int((40.0 / w) * mask_size)))
    list_text = input_text.splitlines()
    if direction == "upwards":
        list_text.reverse()
        operator = "-"
        hight = h - (th + int(th / 1.2)) + eh
    else:
        operator = "+"
    for i, items in enumerate(list_text):
        x, y = (font.getsize(list_text[i])[0] + 50, int(th * 2 - (th / 2)))
        if align == "center":
            width_align = "((mask_size-x)/2)"
        elif align == "left":
            width_align = "0"
        elif align == "right":
            width_align = "(mask_size-x)"
        clr = getcolor(background, "RGBA")
        if transparency == 0:
            mask_img = Image.new("RGBA", (x, y), (clr[0], clr[1], clr[2], 0))
            mask_draw = Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
        else:
            mask_img = Image.new("RGBA", (x, y), (clr[0], clr[1], clr[2], transparency))
            mask_draw = Draw(mask_img)
            mask_draw.text((25, 8), list_text[i], foreground, font=font)
            # remove corner (source - https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi)
            circle = Image.new("L", (rad * 2, rad * 2), 0)
            draw = Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), transparency)
            alpha = Image.new("L", mask_img.size, transparency)
            mw, mh = mask_img.size
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, mh - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (mw - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (mw - rad, mh - rad))
            mask_img.putalpha(alpha)
        trans = Image.new("RGBA", source_img.size)
        trans.paste(
            mask_img,
            (
                (int(width) + int(eval(f"{width_align}"))),
                (eval(f"{hight} {operator}({y*i}+({int(linespace)*i}))")),
            ),
        )
        source_img = Image.alpha_composite(source_img, trans)
    source_img.save(output_img, "png")


def mediatoarttext(dogemedia, output):
    text = open("userbot/helpers/resources/story.txt", encoding="utf-8").read()
    image_color = array(Image.open(output[1]))
    image_color = image_color[::1, ::1]
    image_mask = image_color.copy()
    image_mask[image_mask.sum(axis=2) == 0] = 255
    edges = mean(
        [
            gaussian_gradient_magnitude(image_color[:, :, i] / 255.0, 2)
            for i in range(3)
        ],
        axis=0,
    )
    image_mask[edges > 0.08] = 255
    wc = WordCloud(
        max_words=2000,
        mask=image_mask,
        max_font_size=40,
        random_state=42,
        relative_scaling=0,
    )
    wc.generate(text)
    image_colors = ImageColorGenerator(image_color)
    wc.recolor(color_func=image_colors)
    outputfile = (
        join("./temp", "DogeUserBot.webp")
        if dogemedia
        else join("./temp", "DogeUserBot.png")
    )
    wc.to_file(outputfile)
    return outputfile
