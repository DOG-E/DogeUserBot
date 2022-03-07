# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import calcc, doge, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="calc ([\s\S]*)",
    command=("calc", plugin_category),
    info={
        "h": "Basit hesaplama işlemlerini yapar.",
        "d": "Hesaplama işlemlerinizi çözün.",
        "u": ["{tr}calc", "{tr}calc 2+2÷2"],
    },
)
async def calculator(event):
    "Basit hesaplama işlemlerini yapar."
    cmd = event.text.split(" ", maxsplit=1)[1]
    event = await eor(event, "Hesaplanıyor...")
    out = await calcc(cmd, event, "Maalesef verilen denklem için sonuç bulamıyorum.")
    final_output = "**DENKLEM:** `{}` \n\n **ÇÖZÜM:** \n`{}` \n".format(cmd, out)
    await event.edit(final_output)
