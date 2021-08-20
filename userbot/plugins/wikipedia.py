from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from . import doge, edl, eor

plugin_category = "misc"


@doge.bot_cmd(
    pattern="wiki ([\s\S]*)",
    command=("wiki", plugin_category),
    info={
        "header": "To get wikipedia data about query.",
        "usage": "{tr}wiki <query>",
    },
)
async def wiki(event):
    "To fetch content from Wikipedia."
    match = event.pattern_match.group(1)
    result = None
    try:
        result = summary(match, auto_suggest=False)
    except DisambiguationError as error:
        error = str(error).split("\n")
        result = "".join(
            f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
            for lineno, i in enumerate(error, start=1)
        )
        return await eor(event, f"**Disambiguated page found.**\n\n{result}")
    except PageError:
        pass
    if not result:
        try:
            result = summary(match, auto_suggest=True)
        except DisambiguationError as error:
            error = str(error).split("\n")
            result = "".join(
                f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
                for lineno, i in enumerate(error, start=1)
            )
            return await eor(event, f"**Disambiguated page found.**\n\n{result}")
        except PageError:
            return await edl(event, f"**Sorry i Can't find any results for **`{match}`")
    await eor(event, "**Search:**\n`" + match + "`\n\n**Result:**\n" + f"__{result}__")
