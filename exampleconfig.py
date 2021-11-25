# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from sample_config import Config


class Development(Config):
    # Get this values from the https://my.telegram.org/apps
    APP_ID = 6
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
    # The name to display in your alive message
    ALIVE_NAME = "Your name"
    # Create any PostgreSQL database (recommend to use ElephantSQL) and paste that link here
    DB_URI = "Your DB url"
    # Get this value by running https://bit.do/DogessRepl
    STRING_SESSION = "Your value"
    # Create a new bot in @BotFather ( https://t.me/BotFather ) and fill the following vales with Bot TokenAPI
    BOT_TOKEN = "Your value"
    # Create a private group and a @MissRose_bot to it and type /id and paste that Chat ID here (replace that -100 with that group ID)
    PRIVATE_GROUP_BOT_API_ID = -100
    # Command handler
    CMDSET = "."
    # Command hanler for sudo
    SUDO_CMDSET = "."