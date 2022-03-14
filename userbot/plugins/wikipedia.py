# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from . import doge, edl, eor

plugin_category = "misc"


@doge.bot_cmd(
    pattern="wiki ([\s\S]*)",
    command=("wiki", plugin_category),
    info={
        "h": "Wikipedia'dan içerik getirir.",
        "u": "{tr}wiki <sorgu>",
    },
)
async def wiki(event):
    "Wikipedia'dan içerik getirir."
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
        return await eor(event, f"**Benzer sayfa bulundu:**\n\n{result}")
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
            return await eor(event, f"**Benzer sayfa bulundu:**\n\n{result}")
        except PageError:
            return await edl(
                event, f"**Üzgünüm!\n\n`{match}` için herhangi bir şey bulamadım.**"
            )
    await eor(event, "**Arama:**\n`" + match + "`\n\n**Sonuç:**\n" + f"__{result}__")
