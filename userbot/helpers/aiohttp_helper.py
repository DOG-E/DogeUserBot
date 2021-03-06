# Credits: Pokurt - github.com/pokurt
# Ported from: https://github.com/pokurt/Nana-Remix/blob/5ec27fcc124e7438b2816731c07ea4a129dc9a4d/nana/utils/aiohttp_helper.py#L4
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from aiohttp import ClientSession


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

    @staticmethod
    async def get_status(link):
        async with ClientSession() as session:
            async with session.get(link) as resp:
                return resp.status
