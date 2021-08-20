from io import BytesIO
from os import path, remove
from random import choice, randint, uniform
from string import hexdigits
from textwrap import wrap

from colour import Color
from numpy import array, asarray, mean, sum
from PIL import Image
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
    filename = filename or path.join("./temp/", "temp.jpg")
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filename, "jpeg")
    remove(image)
    return filename


def convert_tosticker(response, filename=None):
    filename = filename or path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    remove(response)
    return filename


# http://effbot.org/imagingbook/imageops.html
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
    out.name = "out.png"
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
    colorRange = list(Color(color1).range_to(Color(color2), nbins))
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
    # Crush image to hell and back
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
    # Generate colour overlay
    overlay = img.split()[0]
    overlay = Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = colorize(overlay, colours[0], colours[1])
    # Overlay red and yellow onto main image and sharpen the hell out of it
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


async def dogemmfhelper(image_path, dogeinput, CNG_FONTS):
    img = Image.open(image_path)
    remove(image_path)
    i_width, i_height = img.size
    text = dogeinput
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = Draw(img)
    m_font = truetype(CNG_FONTS, int((70 / 640) * i_width))
    current_h, pad = 10, 5
    if upper_text:
        for u_text in wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 1,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 1,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((80 / 640) * i_width)) - 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((80 / 640) * i_width)) + 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((80 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    imag = "@DogeUserBot.webp"
    img.save(imag, "WebP")
    return imag


async def dogemmshelper(image_path, dogeinput, CNG_FONTS):
    img = Image.open(image_path)
    remove(image_path)
    i_width, i_height = img.size
    text = dogeinput
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = Draw(img)
    m_font = truetype(CNG_FONTS, int((70 / 640) * i_width))
    current_h, pad = 10, 5
    if upper_text:
        for u_text in wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    pics = "@DogeUserBot.png"
    img.save(pics, "png")
    return pics


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
        path.join("./temp", "textart.webp")
        if dogemedia
        else path.join("./temp", "textart.jpg")
    )
    wc.to_file(outputfile)
    return outputfile
