# by @mrconfused (@sandy1709)
from asyncio import create_subprocess_exec, get_event_loop
from asyncio.subprocess import PIPE
from base64 import b64decode
from datetime import datetime
from io import BytesIO
from io import open as iopen
from os import makedirs
from os import path as osp
from os import remove, rename
from shutil import copyfile
from time import time

from fitz import open as fitzopen
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pymediainfo.MediaInfo import parse as MediaInfoparse
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.types import (
    DocumentAttributeVideo,
    InputMediaUploadedDocument,
    InputMediaUploadedPhoto,
)
from telethon.utils import get_attributes

from . import (
    Config,
    _dogetools,
    _dogeutils,
    _format,
    convert_toimage,
    convert_tosticker,
    doge,
    edl,
    eor,
    invert_frames,
    l_frames,
    logging,
    make_gif,
    media_type,
    parse_pre,
    progress,
    r_frames,
    reply_id,
    spin_frames,
    thumb_from_audio,
    ud_frames,
    vid_to_gif,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)


if not osp.isdir("./temp"):
    makedirs("./temp")


PATH = osp.join("./temp", "temp_vid.mp4")
thumb_loc = osp.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@doge.bot_cmd(
    pattern="spin(?: |$)((.)?(s)?)$",
    command=("spin", plugin_category),
    info={
        "header": "To convert replied image or sticker to spining round video.",
        "flags": {
            ".s": "to save in saved gifs.",
        },
        "usage": [
            "{tr}spin <flag>",
        ],
        "examples": ["{tr}spin", "{tr}spin .s"],
    },
)
async def pic_gifcmd(event):  # sourcery no-metrics
    "To convert replied image or sticker to spining round video."
    args = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "`Reply to supported Media...`")
    media_type(reply)
    dogevent = await eor(event, "__Making round spin video wait a sec.....__")
    output = await _dogetools.media_to_pic(event, reply, noedits=True)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    image = Image.open(meme_file)
    w, h = image.size
    outframes = []
    try:
        outframes = await spin_frames(image, w, h, outframes)
    except Exception as e:
        return await edl(output[0], f"**Error**\n__{e}__")
    output = BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=1)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = osp.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        return await edl(dogevent, "__Unable to make spin gif.__")
    media_info = MediaInfoparse(final)
    aspect_ratio = 1
    for track in media_info.tracks:
        if track.track_type == "Video":
            aspect_ratio = track.display_aspect_ratio
            height = track.height
            width = track.width
    PATH = osp.join(Config.TEMP_DIR, "round.gif")
    if aspect_ratio != 1:
        crop_by = min(height, width)
        await _dogeutils.runcmd(
            f'ffmpeg -i {final} -vf "crop={crop_by}:{crop_by}" {PATH}'
        )
    else:
        copyfile(final, PATH)
    time()
    ul = iopen(PATH, "rb")
    uploaded = await event.client.fast_upload_file(
        file=ul,
    )
    ul.close()
    media = InputMediaUploadedDocument(
        file=uploaded,
        mime_type="video/mp4",
        attributes=[
            DocumentAttributeVideo(
                duration=0,
                w=1,
                h=1,
                round_message=True,
                supports_streaming=True,
            )
        ],
        force_file=False,
        thumb=await event.client.upload_file(meme_file),
    )
    teledoge = await event.client.send_file(
        event.chat_id,
        media,
        reply_to=reply,
        video_note=True,
        supports_streaming=True,
    )
    if not args:
        await _dogeutils.unsavegif(event, teledoge)
    await dogevent.delete()
    for i in [final, "Output.gif", meme_file, PATH, final]:
        if osp.exists(i):
            remove(i)


@doge.bot_cmd(
    pattern="circle ?((-)?s)?$",
    command=("circle", plugin_category),
    info={
        "header": "To make circular video note/sticker.",
        "description": "crcular video note supports atmost 60 sec so give appropariate video.",
        "usage": "{tr}circle <reply to video/sticker/image>",
    },
)
async def video_dogfile(event):  # sourcery no-metrics
    "To make circular video note."
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    dogid = await reply_id(event)
    if not reply or not reply.media:
        return await edl(event, "`Reply to supported media`")
    mediatype = media_type(reply)
    if mediatype == "Round Video":
        return await edl(
            event,
            "__Do you think I am a dumb person😏? The replied media is already in round format,recheck._",
        )
    if mediatype not in ["Photo", "Audio", "Voice", "Gif", "Sticker", "Video"]:
        return await edl(event, "```Supported Media not found...```")
    flag = True
    dogevent = await eor(event, "`Converting to round format..........`")
    dogfile = await reply.download_media(file="./temp/")
    if mediatype in ["Gif", "Video", "Sticker"]:
        if not dogfile.endswith((".webp")):
            if dogfile.endswith((".tgs")):
                hmm = await make_gif(dogevent, dogfile)
                rename(hmm, "./temp/circle.mp4")
                dogfile = "./temp/circle.mp4"
            media_info = MediaInfoparse(dogfile)
            aspect_ratio = 1
            for track in media_info.tracks:
                if track.track_type == "Video":
                    aspect_ratio = track.display_aspect_ratio
                    height = track.height
                    width = track.width
            if aspect_ratio != 1:
                crop_by = min(height, width)
                await _dogeutils.runcmd(
                    f'ffmpeg -i {dogfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
                )
            else:
                copyfile(dogfile, PATH)
            if str(dogfile) != str(PATH):
                remove(dogfile)
            try:
                dogthumb = await reply.download_media(thumb=-1)
            except Exception as e:
                LOGS.error(f"circle - {e}")
    elif mediatype in ["Voice", "Audio"]:
        dogthumb = None
        try:
            dogthumb = await reply.download_media(thumb=-1)
        except Exception:
            dogthumb = osp.join("./temp", "thumb.jpg")
            await thumb_from_audio(dogfile, dogthumb)
        if dogthumb is not None and not osp.exists(dogthumb):
            dogthumb = osp.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, dogthumb)
        if dogthumb is not None and not osp.exists(dogthumb) and osp.exists(thumb_loc):
            flag = False
            dogthumb = osp.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, dogthumb)
        if dogthumb is not None and osp.exists(dogthumb):
            await _dogeutils.runcmd(
                f"""ffmpeg -loop 1 -i {dogthumb} -i {dogfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale=\'iw-mod (iw,2)\':\'ih-mod(ih,2)\',format=yuv420p\" -shortest -movflags +faststart {PATH}"""
            )
            remove(dogfile)
        else:
            remove(dogfile)
            return await edl(dogevent, "`No thumb found to make it video note`", 5)
    if (
        mediatype
        in [
            "Voice",
            "Audio",
            "Gif",
            "Video",
            "Sticker",
        ]
        and not dogfile.endswith((".webp"))
    ):
        if osp.exists(PATH):
            c_time = time()
            attributes, mime_type = get_attributes(PATH)
            ul = iopen(PATH, "rb")
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, dogevent, c_time, "Uploading....")
                ),
            )
            ul.close()
            media = InputMediaUploadedDocument(
                file=uploaded,
                mime_type="video/mp4",
                attributes=[
                    DocumentAttributeVideo(
                        duration=0,
                        w=1,
                        h=1,
                        round_message=True,
                        supports_streaming=True,
                    )
                ],
                force_file=False,
                thumb=await event.client.upload_file(dogthumb) if dogthumb else None,
            )
            teledoge = await event.client.send_file(
                event.chat_id,
                media,
                reply_to=dogid,
                video_note=True,
                supports_streaming=True,
            )

            if not args:
                await _dogeutils.unsavegif(event, teledoge)
            remove(PATH)
            if flag:
                remove(dogthumb)
        await dogevent.delete()
        return
    data = reply.photo or reply.media.document
    img = BytesIO()
    await event.client.download_file(data, img)
    im = Image.open(img)
    w, h = im.size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(im, (0, 0))
    m = min(w, h)
    img = img.crop(((w - m) // 2, (h - m) // 2, (w + m) // 2, (h + m) // 2))
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, w - 10, h - 10), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    img = ImageOps.fit(img, (w, h))
    img.putalpha(mask)
    im = BytesIO()
    im.name = "dog.webp"
    img.save(im)
    im.seek(0)
    await event.client.send_file(event.chat_id, im, reply_to=dogid)
    await dogevent.delete()


@doge.bot_cmd(
    pattern="sti$",
    command=("sti", plugin_category),
    info={
        "header": "Reply this command to a sticker to get image.",
        "description": "This also converts every media to image. that is if video then extracts image from that video.if audio then extracts thumb.",
        "usage": "{tr}sti",
    },
)
async def _(event):
    "Sticker to image Conversion."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "Reply to any sticker/media to convert it to image.__")
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_toimage(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()


@doge.bot_cmd(
    pattern="its$",
    command=("its", plugin_category),
    info={
        "header": "Reply this command to image to get sticker.",
        "description": "This also converts every media to sticker. that is if video then extracts image from that video. if audio then extracts thumb.",
        "usage": "{tr}its",
    },
)
async def _(event):
    "Image to Sticker Conversion."
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if not reply:
        return await edl(event, "Reply to any image/media to convert it to sticker.__")
    output = await _dogetools.media_to_pic(event, reply)
    if output[1] is None:
        return await edl(
            output[0], "__Unable to extract image from the replied message.__"
        )
    meme_file = convert_tosticker(output[1])
    await event.client.send_file(
        event.chat_id, meme_file, reply_to=reply_to_id, force_document=False
    )
    await output[0].delete()


@doge.bot_cmd(
    pattern="ttf ([\s\S]*)",
    command=("ttf", plugin_category),
    info={
        "header": "Text to file.",
        "description": "Reply this command to a text message to convert it into file with given name.",
        "usage": "{tr}ttf <file name>",
    },
)
async def get(event):
    "text to file conversion"
    name = event.text[5:]
    if name is None:
        await eor(event, "reply to text message as `.ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        remove(name)
    else:
        await eor(event, "reply to text message as `.ttf <file name>`")


@doge.bot_cmd(
    pattern="ftt$",
    command=("ftt", plugin_category),
    info={
        "header": "File to text.",
        "description": "Reply this command to a file to print text in that file to text message.",
        "support types": "txt, py, pdf and many more files in text format",
        "usage": "{tr}ftt <reply to document>",
    },
)
async def get(event):
    "File to text message conversion."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if mediatype != "Document":
        return await edl(
            event, "__It seems this is not writable file. Reply to writable file.__"
        )
    file_loc = await reply.download_media()
    file_content = ""
    try:
        with open(file_loc) as f:
            file_content = f.read().rstrip("\n")
    except UnicodeDecodeError:
        pass
    except Exception as e:
        LOGS.info(e)
    if file_content == "":
        try:
            with fitzopen(file_loc) as doc:
                for page in doc:
                    file_content += page.getText()
        except Exception as e:
            if osp.exists(file_loc):
                remove(file_loc)
            return await edl(event, f"**Error:**\n__{e}__")
    await eor(
        event,
        file_content,
        parse_mode=parse_pre,
        aslink=True,
        noformat=True,
        linktext="**Telegram allows only 4096 charcters in a single message. But replied file has much more. So pasting it to pastebin\nlink :**",
    )
    if osp.exists(file_loc):
        remove(file_loc)


@doge.bot_cmd(
    pattern="ftoi$",
    command=("ftoi", plugin_category),
    info={
        "header": "Reply this command to a image file to convert it to image",
        "usage": "{tr}ftoi",
    },
)
async def on_file_to_photo(event):
    "image file(png) to streamable image."
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return await edl(event, "`This isn't an image`")
    if not image.mime_type.startswith("image/"):
        return await edl(event, "`This isn't an image`")
    if image.mime_type == "image/webp":
        return await edl(event, "`For sticker to image use stoi command`")
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    dogt = await eor(event, "`Converting...`")
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await dogt.delete()


@doge.bot_cmd(
    pattern="gif(?:\s|$)([\s\S]*)",
    command=("gif", plugin_category),
    info={
        "header": "Converts Given animated sticker to gif.",
        "usage": "{tr}gif quality ; fps(frames per second)",
    },
)
async def _(event):  # sourcery no-metrics
    "Converts Given animated sticker to gif"
    input_str = event.pattern_match.group(1)
    if not input_str:
        quality = None
        fps = None
    else:
        loc = input_str.split(";")
        if len(loc) > 2:
            return await edl(
                event,
                "wrong syntax . syntax is `.gif quality ; fps(frames per second)`",
            )
        if len(loc) == 2:
            try:
                loc[0] = int(loc[0])
                loc[1] = int(loc[1])
            except ValueError:
                return await edl(
                    event,
                    "wrong syntax . syntax is `.gif quality ; fps(frames per second)`",
                )
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edl(event, "Use quality of range 0 to 721")
            if 0 < loc[1] < 20:
                quality = loc[1].strip()
            else:
                return await edl(event, "Use quality of range 0 to 20")
        if len(loc) == 1:
            try:
                loc[0] = int(loc[0])
            except ValueError:
                return await edl(
                    event,
                    "wrong syntax . syntax is `.gif quality ; fps(frames per second)`",
                )
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edl(event, "Use quality of range 0 to 721")
    dogreply = await event.get_reply_message()
    doge_event = b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not dogreply or not dogreply.media or not dogreply.media.document:
        return await eor(event, "`Stupid!, This is not animated sticker.`")
    if dogreply.media.document.mime_type != "application/x-tgsticker":
        return await eor(event, "`Stupid!, This is not animated sticker.`")
    dogevent = await eor(
        event,
        "Converting this Sticker to GiF...\n This may takes upto few mins..",
        parse_mode=_format.parse_pre,
    )
    try:
        doge_event = Get(doge_event)
        await event.client(doge_event)
    except BaseException:
        pass
    reply_to_id = await reply_id(event)
    dogfile = await event.client.download_media(dogreply)
    doggif = await make_gif(event, dogfile, quality, fps)
    teledoge = await event.client.send_file(
        event.chat_id,
        doggif,
        support_streaming=True,
        force_document=False,
        reply_to=reply_to_id,
    )
    await _dogeutils.unsavegif(event, teledoge)
    await dogevent.delete()
    for files in (doggif, dogfile):
        if files and osp.exists(files):
            remove(files)


@doge.bot_cmd(
    pattern="nfc (mp3|voice)",
    command=("nfc", plugin_category),
    info={
        "header": "Converts the required media file to voice or mp3 file.",
        "usage": [
            "{tr}nfc mp3",
            "{tr}nfc voice",
        ],
    },
)
async def _(event):
    "Converts the required media file to voice or mp3 file."
    if not event.reply_to_msg_id:
        await eor(event, "```Reply to any media file.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eor(event, "reply to media file")
        return
    input_str = event.pattern_match.group(1)
    event = await eor(event, "`Converting...`")
    try:
        start = datetime.now()
        c_time = time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + str(round(time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + str(round(time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            remove(downloaded_file_name)
            return
        process = await create_subprocess_exec(
            *command_to_run,
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        remove(downloaded_file_name)
        if osp.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            remove(new_required_file_name)
            await event.delete()


@doge.bot_cmd(
    pattern="itog(?: |$)((-)?(r|l|u|d|s|i)?)$",
    command=("itog", plugin_category),
    info={
        "header": "To convert replied image or sticker to gif",
        "description": "Bt deafualt will use -i as flag",
        "flags": {
            "-r": "Right rotate gif.",
            "-l": "Left rotate gif.",
            "-u": "Rotates upward gif.",
            "-d": "Rotates downward gif.",
            "-s": "spin the image gif.",
            "-i": "invert colurs gif.",
        },
        "usage": [
            "{tr}itog <flag>",
        ],
        "examples": ["{tr}itog s", "{tr}itog -s"],
    },
)
async def pic_gifcmd(event):  # sourcery no-metrics
    "To convert replied image or sticker to gif"
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edl(event, "__Reply to photo or sticker to make it gif.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/i-tgsticker":
        return await edl(
            event,
            "__Reply to photo or sticker to make it gif. Animated sticker is not supported__",
        )
    args = event.pattern_match.group(1)
    args = "i" if not args else args.replace("-", "")
    dogevent = await eor(event, "__🎞 Making Gif from the relied media...__")
    imag = await _dogetools.media_to_pic(event, reply, noedits=True)
    if imag[1] is None:
        return await edl(
            imag[0], "__Unable to extract image from the replied message.__"
        )
    image = Image.open(imag[1])
    w, h = image.size
    outframes = []
    try:
        if args == "r":
            outframes = await r_frames(image, w, h, outframes)
        elif args == "l":
            outframes = await l_frames(image, w, h, outframes)
        elif args == "u":
            outframes = await ud_frames(image, w, h, outframes)
        elif args == "d":
            outframes = await ud_frames(image, w, h, outframes, flip=True)
        elif args == "s":
            outframes = await spin_frames(image, w, h, outframes)
        elif args == "i":
            outframes = await invert_frames(image, w, h, outframes)
    except Exception as e:
        return await edl(dogevent, f"**Error**\n__{e}__")
    output = BytesIO()
    output.name = "Output.gif"
    outframes[0].save(output, save_all=True, append_images=outframes[1:], duration=0.7)
    output.seek(0)
    with open("Output.gif", "wb") as outfile:
        outfile.write(output.getbuffer())
    final = osp.join(Config.TEMP_DIR, "output.gif")
    output = await vid_to_gif("Output.gif", final)
    if output is None:
        await edl(
            dogevent, "__There was some error in the media. I can't format it to gif.__"
        )
        for i in [final, "Output.gif", imag[1]]:
            if osp.exists(i):
                remove(i)
        return
    teledoge = await event.client.send_file(event.chat_id, output, reply_to=reply)
    await _dogeutils.unsavegif(event, teledoge)
    await dogevent.delete()
    for i in [final, "Output.gif", imag[1]]:
        if osp.exists(i):
            remove(i)


@doge.bot_cmd(
    pattern="vtog ?([0-9.]+)?$",
    command=("vtog", plugin_category),
    info={
        "header": "Reply this command to a video to convert it to gif.",
        "description": "By default speed will be 1x",
        "usage": "{tr}vtog <speed>",
    },
)
async def _(event):
    "Reply this command to a video to convert it to gif."
    reply = await event.get_reply_message()
    mediatype = media_type(event)
    if mediatype and mediatype != "video":
        return await edl(event, "__Reply to video to convert it to gif__")
    args = event.pattern_match.group(1)
    if not args:
        args = 2.0
    else:
        try:
            args = float(args)
        except ValueError:
            args = 2.0
    dogevent = await eor(event, "__🎞Converting into Gif..__")
    inputfile = await reply.download_media()
    outputfile = osp.join(Config.TEMP_DIR, "vidtogif.gif")
    result = await vid_to_gif(inputfile, outputfile, speed=args)
    if result is None:
        return await edl(event, "__I couldn't convert it to gif.__")
    teledoge = await event.client.send_file(event.chat_id, result, reply_to=reply)
    await _dogeutils.unsavegif(event, teledoge)
    await dogevent.delete()
    for i in [inputfile, outputfile]:
        if osp.exists(i):
            remove(i)
