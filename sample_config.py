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
import os
from typing import Set

from telethon.tl.types import ChatBannedRights




class Config(object):
    LOGGER = True

    # MUST NEEDED VARS
    # Set this value with your name
    ALIVE_NAME = os.environ.get("ALIVE_NAME", None)
    # Get the values for following 2 from https://my.telegram.org/apps
    APP_ID = int(os.environ.get("APP_ID", 6))
    API_HASH = os.environ.get("API_HASH") or None
    # Database url Heroku sets it automatically else get this from ElephantSQL
    DB_URI = os.environ.get("DATABASE_URL", None)
    # Get this value by running https://bit.do/DogessRepl
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    # Telegram Bot Token and Bot Username from @BotFather ( https://t.me/BotFather )
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    BOT_USERNAME = None
    # Set this with required Doge repository link
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "DOGE-TR")

    # BASIC & MAIN CONFIG VARS
    # Set this value with group ID of private group(can be found this value by .id)
    PRIVATE_GROUP_BOT_API_ID = int(os.environ.get("PRIVATE_GROUP_BOT_API_ID") or 0)
    # For Heroku plugin you can get this value from https://dashboard.heroku.com/account
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    # Set this with same app name you given for Heroku
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)

    # CUSTOM VARS
    # Set this with group ID so it keeps notifying about your tagged messages or PMs
    PM_LOGGER_GROUP_ID = int(os.environ.get("PM_LOGGER_GROUP_ID") or 0)
    PMLOGGER = os.environ.get("PMLOGGER", False)
    # Set this will channel ID of your custom plugins
    PLUGIN_CHANNEL = int(os.environ.get("PLUGIN_CHANNEL") or 0)
    PLUGINS = os.environ.get("PLUGINS", True)
    DOGEPLUGIN = os.environ.get("DOGEPLUGIN", False)
    DOGEHUB = os.environ.get("DOGEHUB", False)
    # Specify NO_LOAD with plugin names for not loading in userbot
    NO_LOAD = list(os.environ.get("NO_LOAD", "").split())
    # Specify command handler that should be used for the plugins
    # This should be a valid "regex" pattern
    CMDSET = os.environ.get("CMDSET", r".")
    SUDO_CMDSET = os.environ.get("SUDO_CMDSET", r".")
    # Set this with required folder path to act as download folder
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "downloads")
    # Set this with required folder path to act as temparary folder
    TEMP_DIR = os.environ.get("TEMP_DIR", "./temp/")
    # Is dual logging needed? Write; True or False
    DUAL_LOG = os.environ.get("DUAL_LOG", False)
    # Progress bar progress
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "▰")
    UNFINISHED_PROGRESS_STR = os.environ.get("UNFINISHED_PROGRESS_STR", "▱")

    # DON'T EDIT BELOW THIS LINE IF YOU DON'T KNOW WHAT YOU ARE DOING
    # TG API limit. A message can have maximum 4096 characters!
    MAX_MESSAGE_SIZE_LIMIT = 4095
    # Specify LOAD and NO_LOAD
    LOAD = []
    # Warn mode for anti flood
    ANTI_FLOOD_WARN_MODE = ChatBannedRights(
        until_date=None, view_messages=None, send_messages=True
    )
    CHROME_BIN = os.environ.get("CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
    CHROME_DRIVER = os.environ.get(
        "CHROME_DRIVER", "/app/.chromedriver/bin/chromedriver"
    )
    # For sed plugin
    GROUP_REG_SED_EX_BOT_S = os.environ.get(
        "GROUP_REG_SED_EX_BOT_S", r"(regex|moku|BananaButler_|rgx|l4mR)bot"
    )
    # Get this value from http://www.timezoneconverter.com/cgi-bin/findzone.tzc
    COUNTRY = str(os.environ.get("COUNTRY", ""))
    TZ = os.environ.get("TZ", "Europe/Istanbul")
    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))
    # For updater plugin
    UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "DOGE-TR")
    # DON'T TOUCH THIS AT ALL
    SUDO_USERS: Set[int] = set()
    DOGELOGO = None
    BOTLOG = False
    BOTLOG_CHATID = 0



class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
