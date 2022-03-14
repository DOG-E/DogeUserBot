# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from time import time

from emoji import get_emoji_regexp
from telethon.tl.types import Channel, PollAnswer


async def get_message_link(channelid, msgid):
    if str(channelid).startswith("-"):
        channelid = str(channelid)[1:]
    if channelid.startswith("100"):
        channelid = channelid[3:]
    return f"https://t.me/c/{channelid}/{msgid}"


def utc_to_local(utc_datetime):
    now_timestamp = time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["sn", "dk", "s", "gün"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


async def admin_groups(hav):
    doggroups = []
    async for dialog in hav.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            doggroups.append(entity.id)
    return doggroups


# Credits: Pokurt - https://github.com/pokurt/LyndaRobot/blob/7556ca0efafd357008131fa88401a8bb8057006f/lynda/modules/helper_funcs/string_handling.py#L238
async def extract_time(dog, time_val):
    if any(time_val.endswith(unit) for unit in ("sn", "d", "s", "g", "h")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await dog.edit("🚨 Geçersiz zaman değeri belirtildi.")
            return None
        if unit == "sn":
            bantime = int(time() + int(time_num) * 1)
        elif unit == "d":
            bantime = int(time() + int(time_num) * 60)
        elif unit == "s":
            bantime = int(time() + int(time_num) * 60 * 60)
        elif unit == "g":
            bantime = int(time() + int(time_num) * 24 * 60 * 60)
        elif unit == "h":
            bantime = int(time() + int(time_num) * 7 * 24 * 60 * 60)
        else:
            await dog.edit(
                f"`🚨 Geçersiz zaman değeri belirtildi..\n⏰ Beklenen sn, d, s, g ya da h iken olan değer:` `{time_val[-1]}`"
            )
            return None
        return bantime
    await dog.edit(
        f"`🚨 Geçersiz zaman değeri belirtildi..\n⏰ Beklenen sn, d, s, g ya da h iken olan değer:` `{time_val[-1]}`"
    )
    return None


def Build_Poll(options):
    return [PollAnswer(option, bytes(i)) for i, option in enumerate(options, start=1)]


def deEmojify(inputString: str) -> str:
    return get_emoji_regexp().sub("", inputString)
