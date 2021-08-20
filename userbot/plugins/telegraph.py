from datetime import datetime
from os import remove
from random import choice
from string import ascii_lowercase, ascii_uppercase

from PIL.Image import open as Imopen
from telegraph import Telegraph, upload_file
from telegraph.exceptions import TelegraphException
from telethon.events import NewMessage
from telethon.utils import get_display_name

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    Config,
    doge,
    edl,
    eor,
    fsmessage,
    lan,
    logging,
    mention,
)

plugin_category = "tool"
LOGS = logging.getLogger(__name__)

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Imopen(image)
    im.save(image, "PNG")


@doge.bot_cmd(
    pattern="(t(ele)?g(raph)?) ?(m|t|media|text)(?:\s|$)([\s\S]*)",
    command=("telegraph", plugin_category),
    info={
        "header": "To get telegraph link.",
        "description": "Reply to text message to paste that text on telegraph you can also pass input along with command \
            So that to customize title of that telegraph and reply to media file to get sharable link of that media(atmost 5mb is supported)",
        "options": {
            "m or media": "To get telegraph link of replied sticker/image/video/gif.",
            "t or text": "To get telegraph link of replied text you can use custom title.",
        },
        "usage": [
            "{tr}tgm",
            "{tr}tgt <title(optional)>",
            "{tr}telegraph media",
            "{tr}telegraph text <title(optional)>",
        ],
    },
)  # sourcery no-metrics
async def _(event):
    "To get telegraph link."
    dogevent = await eor(event, lan("processing"))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Created New Telegraph account {auth_url} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**",
        )
    optional_title = event.pattern_match.group(5)
    if not event.reply_to_msg_id:
        return await dogevent.edit(
            "`Reply to a message to get a permanent telegra.ph link.`",
        )

    start = datetime.now()
    r_message = await event.get_reply_message()
    input_str = (event.pattern_match.group(4)).strip()
    if input_str in ["media", "m"]:
        downloaded_file_name = await event.client.download_media(
            r_message, Config.TEMP_DIR
        )
        await dogevent.edit(f"`Downloaded to {downloaded_file_name}`")
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
        try:
            media_urls = upload_file(downloaded_file_name)
        except TelegraphException as exc:
            await dogevent.edit(f"**Error: **\n`{exc}`")
            remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms = (end - start).seconds
            remove(downloaded_file_name)
            await dogevent.edit(
                f"**➥ Uploaded to: **[telegraph](https://telegra.ph{media_urls[0]})\
                 \n**➥ Uploaded in {ms} seconds.**\
                 \n**➥ Uploaded by:** {mention}",
                link_preview=True,
            )
    elif input_str in ["text", "t"]:
        user_object = await event.client.get_entity(r_message.sender_id)
        title_of_page = get_display_name(user_object)
        # apparently, all Users do not have last_name field
        if optional_title:
            title_of_page = optional_title
        page_content = r_message.message
        if r_message.media:
            if page_content != "":
                title_of_page = page_content
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TEMP_DIR
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            for m in m_list:
                page_content += m.decode("UTF-8") + "\n"
            remove(downloaded_file_name)
        page_content = page_content.replace("\n", "<br>")
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
        except Exception as e:
            LOGS.info(e)
            title_of_page = "".join(
                choice(list(ascii_lowercase + ascii_uppercase)) for _ in range(16)
            )
            response = telegraph.create_page(title_of_page, html_content=page_content)
        end = datetime.now()
        ms = (end - start).seconds
        dog = f"https://telegra.ph/{response['path']}"
        await dogevent.edit(
            f"**➥ Uploaded to:** [telegraph]({dog})\
                 \n**➥ Uploaded in {ms} seconds.**\
                 \n**➥ Uploaded by:** {mention}",
            link_preview=True,
        )


@doge.bot_cmd(
    pattern="tgl(?:\s|$)([\s\S]*)",
    command=("tgl", plugin_category),
    info={
        "header": "Reply or write link convert to Telegraph page.",
        "usage": ["{tr}tgl <reply link>", "{tr}tgl <link>"],
    },
)
async def _(event):
    "To get link preview"
    input_str = event.pattern_match.group(1)
    if not input_str:
        reply_message = await event.get_reply_message()
        input_str = reply_message.text
    if not input_str:
        return await edl(event, "Give me a link.")
    chat = "@ChotamReaderBot"
    dogevent = await eor(event, lan("processing"))
    async with event.client.conversation(chat) as conv:
        response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
        await fsmessage(event, input_str, forward=True, chat=chat)
        response = await response
        await event.client.send_read_acknowledge(conv.chat_id)
        if response.text.startswith(""):
            await dogevent.edit("Am I Dumb Or Am I Dumb?")
        else:
            await dogevent.delete()
            await event.client.send_message(event.chat_id, response.message)
        await conv.mark_read()
        await conv.cancel_all()
