# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from . import fonts
from . import memeshelper as dogememes
from .aiohttp_helper import AioHttp
from .resources.constants import *
from .utils import *

flag = True
check = 0
while flag:
    try:
        from . import nsfw as hub
        from .functions import *
        from .progress import *
        from .qhelper import process
        from .tools import *
        from .utils import _dogetools, _dogeutils, _format

        break
    except ModuleNotFoundError as e:
        install_pip(e.name)
        check += 1
        if check > 5:
            break
