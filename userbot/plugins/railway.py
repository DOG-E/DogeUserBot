from . import BOTLOG_CHATID, doge, edl, eor, tr
from ..sql_helper.globals import delr_var, getr_var, setr_var

plugin_category = "bot"


@doge.bot_cmd(
    pattern="([Ss]et|[Gg]et|[Dd]el)[ Rr]w ([\s\S]*)",
    command=("rw", plugin_category),
    info={
        "header": "To manage railway variables.",
        "flags": {
            "set": "To set a new variable or modify an old one.",
            "get": "To get the value of a variable.",
            "del": "To delete a variable"
        },
        "usage": [
            "{tr}set rw <var name> <var value>",
            "{tr}get rw <var name>",
            "{tr}del rw <var name"
        ],
        "examples": [
            "{tr}get rw ALIVE_NAME",
            "{tr}set rw ALIVE_NAME Mutlu"
        ]
    }
)
async def railway_variable(event):
    "To play with Railway variables"
    exe = event.pattern_match.group(1)
    if exe == "set":
        key = event.pattern_match.group(2)
        value = event.pattern_match.group(3)
        if not key or not value:
            return await eor(
                event,
                f"__Try typing__ `{tr}doge rw` __before proceeding further .__\n"
                "__If you still don't get it, then you should try using this 🔫 on yourself.__"
            )

        if not await setr_var(key, value):
            return await edl(
                event,
                "__You have already set this var with the same value.__"
            )

        await setr_var(key, value)
        await edl(event, f"`{key}` **successfully set to  ->  **`value`")
        return await event.client.send_message(
            BOTLOG_CHATID,
            "#RAILWAY_VARIABLE\n\n"
            "**Variable has been set!!**\n"
            f"Variable Name: {key}\n"
            f"Variable Value: {value}"
        )

    if exe == "get":
        key = event.pattern_match.group(2)
        if not key:
            return await eor(
                event,
                f"__Try typing__ `{tr}doge rw` __before proceeding further .__\n"
                "__If you stil don't get it, then you should try using this 🔫 on yourself.__"
            )

        if not await getr_var(key):
            return await edl(
                event,
                f"__I couldn't find `{key}` __variable. I guess you haven't set that yet.__"
            )

        value = await getr_var(key)
        return await eor(
            event,
            "**Config Vars:**"
            f"\n\n`{key}` = `{value}`\n"
        )

    if exe == "del":
        key = event.pattern_match.group(2)
        if not key:
            return await eor(
                event,
                f"__Try typing__ `{tr}doge rw` __before proceeding further .__\n"
                "__If you stil don't get it, then you should try using this 🔫 on yourself.__"
            )

        if await delr_var(key) == "Click Clack!":
            return await eor(
                event,
                f"**Error:**\n __I can't delete__ `{key}` __variable. Please delete it manually from__ railway.app"
            )

        if not await delr_var(key):
            return await eor(event, f"__First set the variable by__ `{tr}set railway var {key} <some value>`")

        value = await getr_var(key)
        await delr_var(key)
        await edl(event, "Successfully deleted the variable " + key)
        return await event.client.send_message(
            BOTLOG_CHATID,
            "#RAILWAY_VARIABLE\n\n"
            "**Variable has been deleted!!**\n"
            f"Variable Name: {key}\n"
            f"Variable Value: {value}"
        )
