from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

from ..utils.tools import create_supergroup
from . import Config, doge, edl, eor, tr

plugin_category = "tool"


@doge.bot_cmd(
    pattern="create (b|g|c) ([\s\S]*)",
    command=("create", plugin_category),
    info={
        "header": "To create a private group/channel with userbot.",
        "description": "Use this cmd to create super group , normal group or channel.",
        "flags": {
            "b": "to create a private super group",
            "g": "To create a private basic group.",
            "c": "to create a private channel",
        },
        "usage": "{tr}create (b|g|c) <name of group/channel>",
        "examples": "{tr}create b DogeUserBot",
    },
)
async def _(event):
    "To create a private group/channel with userbot"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "c":
        descript = "This is a Test Channel created using DogeUserBot\n\
            @DogeUserBot"
    else:
        descript = "This is a Test Group created using DogeUserBot\n\
            @DogeUserBot"
    if type_of_group == "g":
        try:
            result = await event.client(
                CreateChatRequest(
                    users=[Config.BOT_USERNAME],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await eor(
                event, f"Group `{group_name}` created successfully. Join {result.link}"
            )
        except Exception as e:
            await edl(event, f"**Error:**\n{str(e)}")
    elif type_of_group == "c":
        try:
            r = await event.client(
                CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )
            created_chat_id = r.chats[0].id
            result = await event.client(
                ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await eor(
                event,
                f"Channel `{group_name}` created successfully. Join {result.link}",
            )
        except Exception as e:
            await edl(event, f"**Error:**\n{e}")
    elif type_of_group == "b":
        answer = await create_supergroup(
            group_name, event.client, Config.BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await eor(
                event,
                f"Mega group `{group_name}` created successfully. Join {answer[0].link}",
            )
        else:
            await edl(event, f"**Error:**\n{answer[1]}")
    else:
        await edl(event, f"Read `{tr}doge create` to know how to use me")
