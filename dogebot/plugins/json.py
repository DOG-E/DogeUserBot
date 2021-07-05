# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from dogebot import doge

from ..core.managers import edit_or_reply
from ..helpers.utils import _format

plugin_category = "tools"

# yaml_format is ported from uniborg
@doge.ub(
    pattern="json$",
    command=("json", plugin_category),
    info={
        "header": "To get details of that message in json format.",
        "usage": "{tr}json reply to message",
    },
)
async def _(event):
    "To get details of that message in json format."
    dogevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = dogevent.stringify()
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)


@doge.ub(
    pattern="yaml$",
    command=("yaml", plugin_category),
    info={
        "header": "To get details of that message in yaml format.",
        "usage": "{tr}yaml reply to message",
    },
)
async def _(event):
    "To get details of that message in yaml format."
    dogevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = _format.yaml_format(dogevent)
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)
