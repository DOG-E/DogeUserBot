# ported from uniborg by @spechide
from asyncio import create_subprocess_exec, get_event_loop
from asyncio.subprocess import PIPE
from datetime import datetime
from io import FileIO
from os import path as osp
from os import remove
from time import time

from . import Config, _dogetools, doge, edl, eor, media_type, progress, reply_id, tr

plugin_category = "tool"

FF_MPEG_DOWN_LOAD_MEDIA_PATH = osp.join(
    Config.TMP_DOWNLOAD_DIRECTORY, "DogeUserBot.media.ffmpeg"
)


# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26
async def cult_small_video(
    video_file, output_directory, start_time, end_time, out_put_file_name=None
):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = out_put_file_name or osp.join(
        output_directory, f"{round(time())}.mp4"
    )
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name,
    ]
    process = await create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=PIPE,
        stderr=PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    if osp.lexists(out_put_file_name):
        return out_put_file_name
    return None


@doge.bot_cmd(
    pattern="ffmpegsave$",
    command=("ffmpegsave", plugin_category),
    info={
        "header": "Saves the media file in bot to trim mutliple times",
        "description": "Will download the replied media into the bot so that you an trim it as your needs.",
        "usage": "{tr}ffmpegsave <reply>",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Saves the media file in bot to trim mutliple times"
    if not osp.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        reply_message = await event.get_reply_message()
        if reply_message:
            start = datetime.now()
            media = media_type(reply_message)
            if media not in ["Video", "Audio", "Voice", "Round Video", "Gif"]:
                return await edl(event, "`Only media files are supported`", 5)
            dogevent = await eor(event, "`Saving the file...`")
            try:
                c_time = time()
                dl = FileIO(FF_MPEG_DOWN_LOAD_MEDIA_PATH, "a")
                await event.client.fast_download_file(
                    location=reply_message.document,
                    out=dl,
                    progress_callback=lambda d, t: get_event_loop().create_task(
                        progress(d, t, dogevent, c_time, "trying to download")
                    ),
                )
                dl.close()
            except Exception as e:
                await dogevent.edit(f"**Error:**\n`{e}`")
            else:
                end = datetime.now()
                ms = (end - start).seconds
                await dogevent.edit(
                    f"Saved file to `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}` in `{ms}` seconds."
                )
        else:
            await edl(event, "`Reply to a any media file`")
    else:
        await edl(
            event,
            f"A media file already exists in path. Please remove the media and try again!\n`{tr}ffmpegclear`",
        )


@doge.bot_cmd(
    pattern="vtrim(?:\s|$)([\s\S]*)",
    command=("vtrim", plugin_category),
    info={
        "header": "Trims the saved media with specific given time internval and outputs as video if it is video",
        "description": "Will trim the saved media with given given time interval.",
        "note": "if you haven't mentioned time interval and just time then will send screenshot at that location.",
        "usage": "{tr}vtrim <time interval>",
        "examples": "{tr}vtrim 00:00 00:10",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Trims the saved media with specific given time internval and outputs as video if it is video"
    if not osp.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        return await edl(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
    reply_to_id = await reply_id(event)
    dogevent = await eor(event, "`Triming the media......`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
        )
        if o is None:
            return await edl(dogevent, f"**Error : **`Can't complete the process`")
        try:
            c_time = time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, dogevent, c_time, "trying to upload")
                ),
            )
            remove(o)
        except Exception as e:
            return await edl(dogevent, f"**Error: **`{e}`")
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await _dogetools.take_screen_shot(FF_MPEG_DOWN_LOAD_MEDIA_PATH, start_time)
        if o is None:
            return await edl(dogevent, "**Error: **`Can't complete the process`")
        try:
            c_time = time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, dogevent, c_time, "trying to upload")
                ),
            )
            remove(o)
        except Exception as e:
            return await edl(dogevent, f"**Error : **`{e}`")
    else:
        await edl(dogevent, "RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await edl(dogevent, f"`Completed Process in {ms} seconds`", 3)


@doge.bot_cmd(
    pattern="atrim(?:\s|$)([\s\S]*)",
    command=("atrim", plugin_category),
    info={
        "header": "Trims the saved media with specific given time internval and outputs as audio",
        "description": "Will trim the saved media with given given time interval. and output only audio part",
        "usage": "{tr}atrim <time interval>",
        "examples": "{tr}atrim 00:00 00:10",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Trims the saved media with specific given time internval and outputs as audio"
    if not osp.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        return await edl(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
    reply_to_id = await reply_id(event)
    dogevent = await eor(event, "`Triming the media...........`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    out_put_file_name = osp.join(Config.TMP_DOWNLOAD_DIRECTORY, f"{round(time())}.mp3")
    if len(cmt) == 3:
        # output should be audio
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
            out_put_file_name,
        )
        if o is None:
            return await edl(dogevent, "**Error: **`Can't complete the process`")
        try:
            c_time = time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: get_event_loop().create_task(
                    progress(d, t, dogevent, c_time, "trying to upload")
                ),
            )
            remove(o)
        except Exception as e:
            return await edl(dogevent, f"**Error: **`{e}`")
    else:
        await edl(dogevent, "RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await edl(dogevent, f"`Completed Process in {ms} seconds`", 3)


@doge.bot_cmd(
    pattern="ffmpegclear$",
    command=("ffmpegclear", plugin_category),
    info={
        "header": "Deletes the saved media so you can save new one",
        "description": "Only after deleting the old saved file you can add new file",
        "usage": "{tr}ffmpegclear",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Deletes the saved media so you can save new one"
    if not osp.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await edl(event, "`There is no media saved in bot for triming`")
    else:
        remove(FF_MPEG_DOWN_LOAD_MEDIA_PATH)
        await edl(
            event,
            "`The media saved in bot for triming is deleted now . you can save now new one `",
        )
