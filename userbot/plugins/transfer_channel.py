from telethon.password import compute_check
from telethon.tl.functions.account import GetPasswordRequest
from telethon.tl.functions.channels import EditCreatorRequest

from . import Config, doge

plugin_category = "tool"


@doge.bot_cmd(
    pattern="otransfer ([\s\S]*)",
    command=("otransfer", plugin_category),
    info={
        "header": "To transfer channel ownership.",
        "description": "Transfers ownership to the given username for this set this var `TG_2STEP_VERIFICATION_CODE` in heroku with your 2-step verification code.",
        "usage": "{tr}otransfer <username to whom you want to transfer>",
    },
)
async def _(event):
    "To transfer channel ownership"
    user_name = event.pattern_match.group(1)
    try:
        pwd = await event.client(GetPasswordRequest())
        my_srp_password = compute_check(pwd, Config.TG_2STEP_VERIFICATION_CODE)
        await event.client(
            EditCreatorRequest(
                channel=event.chat_id, user_id=user_name, password=my_srp_password
            )
        )
    except Exception as e:
        await event.edit(f"**Error:**\n`{e}`")
    else:
        await event.edit("Transferred 🌚")
