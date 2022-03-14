# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
#
# LÜTFEN DUR!
# BU DOSYAYI DÜZENLEMEYİN YA DA SİLMEYİN!
# Aynı dizinde yeni bir config.py dosyası oluşturun ve içe aktarın,
# Sonra bu "class"ı kullanın.
#
# ================================================================
from os import environ
from typing import Set

from telethon.tl.types import ChatBannedRights


class Config(object):
    LOGGER = True

    # MUST NEEDED VARS
    # Set this value with your name
    ALIVE_NAME = environ.get("ALIVE_NAME", None)
    # Get the values for following 2 from https://my.telegram.org/apps
    APP_ID = int(environ.get("APP_ID", 6))
    API_HASH = environ.get("API_HASH", None)
    # Database url Heroku sets it automatically else get this from ElephantSQL
    DB_URI = environ.get("DATABASE_URL", None)
    # Get this value by running https://bit.do/DogessRepl
    STRING_SESSION = environ.get("STRING_SESSION", None)
    # Telegram Bot Token and Bot Username from @BotFather ( https://t.me/BotFather )
    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    # Set this with required Doge repository link
    UPSTREAM_REPO = environ.get("UPSTREAM_REPO", "https://github.com/DOG-E/DogeStarter")

    # BASIC & MAIN CONFIG VARS
    # Set this value with group ID of private group(can be found this value by .id)
    PRIVATE_GROUP_BOT_API_ID = int(environ.get("PRIVATE_GROUP_BOT_API_ID") or 0)
    # For Heroku plugin you can get this value from https://dashboard.heroku.com/account
    HEROKU_API_KEY = environ.get("HEROKU_API_KEY", None)
    # Set this with same app name you given for Heroku
    HEROKU_APP_NAME = environ.get("HEROKU_APP_NAME", None)

    # CUSTOM VARS
    # Set this with group ID so it keeps notifying about your tagged messages or PMs
    PM_LOGGER_GROUP_ID = int(environ.get("PM_LOGGER_GROUP_ID") or 0)
    PMLOGGER = environ.get("PMLOGGER", False)
    # Set this will channel ID of your custom plugins
    PLUGIN_CHANNEL = int(environ.get("PLUGIN_CHANNEL") or 0)
    PLUGINS = environ.get("PLUGINS", True)
    DOGEPLUGIN = environ.get("DOGEPLUGIN", False)
    DOGEHUB = environ.get("DOGEHUB", False)
    # Specify NO_LOAD with plugin names for not loading in userbot
    NO_LOAD = list(environ.get("NO_LOAD", "").split())
    # Specify command handler that should be used for the plugins
    # This should be a valid "regex" pattern
    CMDSET = environ.get("CMDSET", r".")
    SUDO_CMDSET = environ.get("SUDO_CMDSET", r".")
    # Set this with required folder path to act as download folder
    TMP_DOWNLOAD_DIRECTORY = environ.get("TMP_DOWNLOAD_DIRECTORY", "downloads")
    # Set this with required folder path to act as temparary folder
    TEMP_DIR = environ.get("TEMP_DIR", "./temp/")
    # Is dual logging needed? Write; True or False
    DUAL_LOG = environ.get("DUAL_LOG", False)
    # Progress bar progress
    FINISHED_PROGRESS_STR = environ.get("FINISHED_PROGRESS_STR", "▰")
    UNFINISHED_PROGRESS_STR = environ.get("UNFINISHED_PROGRESS_STR", "▱")

    # DON'T EDIT BELOW THIS LINE IF YOU DON'T KNOW WHAT YOU ARE DOING
    # TG API limit. A message can have maximum 4096 characters!
    MAX_MESSAGE_SIZE_LIMIT = 4095
    # Specify LOAD and NO_LOAD
    LOAD = []
    # Warn mode for anti flood
    ANTI_FLOOD_WARN_MODE = ChatBannedRights(
        until_date=None, view_messages=None, send_messages=True
    )
    CHROME_BIN = environ.get("CHROME_BIN", "/usr/bin/chromium-browser")
    CHROME_DRIVER = environ.get("CHROME_DRIVER", "/usr/bin/chromedriver")
    # For sed plugin
    GROUP_REG_SED_EX_BOT_S = environ.get(
        "GROUP_REG_SED_EX_BOT_S", r"(regex|moku|BananaButler_|rgx|l4mR)bot"
    )
    # Get this value from http://www.timezoneconverter.com/cgi-bin/findzone.tzc
    COUNTRY = str(environ.get("COUNTRY", "Turkey"))
    TZ = environ.get("TZ", "Europe/Istanbul")
    TZ_NUMBER = int(environ.get("TZ_NUMBER", 1))
    # For updater plugin
    UPSTREAM_REPO_BRANCH = environ.get("UPSTREAM_REPO_BRANCH", "DOGE-TR")
    # DON'T TOUCH THIS AT ALL
    SUDO_USERS: Set[int] = set()
    DOGELOGO = None
    BOTLOG = False
    BOTLOG_CHATID = 0


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
