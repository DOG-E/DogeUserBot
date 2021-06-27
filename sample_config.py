# PLEASE STOP!
# DO NOT EDIT THIS FILE OR DELETE THIS FILE!
# Create a new config.py file in same directory and import, then extend this class.

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
    # Get this value by running ### or https://
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    # Telegram Bot Token and Bot Username from @BotFather(https://T.me/BotFather)
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN") or os.environ.get(
        "TG_BOT_TOKEN_BF_HER", None
    )
    TG_BOT_USERNAME = None
    # Get this value from http://www.timezoneconverter.com/cgi-bin/findzone.tzc
    TZ = os.environ.get("TZ", "Europe/Istanbul")
    # Set this with required Doge repository link
    UPSTREAM_REPO = os.environ.get(
        "UPSTREAM_REPO", "https://github.com/DOG-E/DogeUserBot.git"
    )
    # Set Doge language
    DOGELANG = os.environ.get('DOGELANG', 'en')

    # BASIC & MAIN CONFIG VARS
    # For profile default name
    AUTONAME = os.environ.get("AUTONAME", None)
    # Set this value with group ID of private group(can be found this value by .id)
    PRIVATE_GROUP_BOT_API_ID = int(os.environ.get("PRIVATE_GROUP_BOT_API_ID") or 0)
    # Set this value same as PRIVATE_GROUP_BOT_API_ID if you need PMGUARD
    PRIVATE_GROUP_ID = int(os.environ.get("PRIVATE_GROUP_ID") or 0)
    # Set this value with channel ID of private channel use full for .frwd cmd
    PRIVATE_CHANNEL_BOT_API_ID = int(os.environ.get("PRIVATE_CHANNEL_BOT_API_ID") or 0)
    # For Heroku plugin you can get this value from https://dashboard.heroku.com/account
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    # Set this with same app name you given for Heroku
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    # Owner ID to show profile link of given ID as owner
    OWNER_ID = int(os.environ.get("OWNER_ID") or 0)
    # Set this with group ID so it keeps notifying about your tagged messages or PMs
    PM_LOGGER_GROUP_ID = int(
        os.environ.get("PM_LOGGER_GROUP_ID")
        or os.environ.get("PM_LOGGR_BOT_API_ID")
        or 0
    )

    # Custom vars for userbot
    # Set this will channel ID of your custom plugins
    PLUGIN_CHANNEL = int(os.environ.get("PLUGIN_CHANNEL") or 0)
    # Set this value with your required name for Telegraph plugin
    TELEGRAPH_SHORT_NAME = os.environ.get("TELEGRAPH_SHORT_NAME", "dogeuserbot")
    # For custom thumb image set this with your required thumb Telegraph link
    THUMB_IMAGE = os.environ.get(
        "THUMB_IMAGE", "https://telegra.ph/file/30772e5649e947279315f.jpg"
    )
    # Specify NO_LOAD with plugin names for not loading in userbot
    NO_LOAD = [x for x in os.environ.get("NO_LOAD", "").split()]
    # For custom pic for .digitalpfp
    DIGITAL_PIC = os.environ.get("DIGITAL_PIC", None)
    # Your default pic Telegraph link
    DEFAULT_PIC = os.environ.get("DEFAULT_PIC", None)
    # Set this with your default bio
    DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)
    # Set this with your deafult name
    DEFAULT_NAME = os.environ.get("DEFAULT_NAME", None)
    # Specify command handler that should be used for the plugins
    # This should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", r".")
    SUDO_COMMAND_HAND_LER = os.environ.get("SUDO_COMMAND_HAND_LER", r".")
    # Set this with required folder path to act as download folder
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "downloads")
    # Set this with required folder path to act as temparary folder
    TEMP_DIR = os.environ.get("TEMP_DIR", "./temp/")
    # Time to update autoprofile cmds
    CHANGE_TIME = int(os.environ.get("CHANGE_TIME", 60))
    # SpamWatch, CAS, SpamProtection ban needed or not
    ANTISPAMBOT_BAN = os.environ.get("ANTISPAMBOT_BAN", False)
    # Is dual logging needed or not true or false
    DUAL_LOG = os.environ.get("DUAL_LOG", False)
    # Progress bar progress
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "▰")
    UNFINISHED_PROGRESS_STR = os.environ.get("UNFINISHED_PROGRESS_STR", "▱")

    # API VARS FOR USERBOT
    # Get your own ACCESS_KEY from http://api.screenshotlayer.com/api/capture for screen shot
    SCREEN_SHOT_LAYER_ACCESS_KEY = os.environ.get("SCREEN_SHOT_LAYER_ACCESS_KEY", None)
    # Get your own APPID from https://api.openweathermap.org/data/2.5/weather
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    # This is required for the speech to text plugin. Get your USERNAME from
    # https://console.bluemix.net/docs/services/speech-to-text/getting-started.html
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    # Get a Free API Key from OCR.Space
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)
    # Genius lyrics get this value from https://genius.com/developers both has
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", None)
    # Get your own API key from https://www.remove.bg/
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    # Get this value from https://free.currencyconverterapi.com/
    CURRENCY_API = os.environ.get("CURRENCY_API", None)
    # Google Drive plugin for info: https://
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID", None)
    G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA", None)
    G_DRIVE_INDEX_LINK = os.environ.get("G_DRIVE_INDEX_LINK", None)
    # For transfer channel 2 step verification code of Telegram
    TG_2STEP_VERIFICATION_CODE = os.environ.get("TG_2STEP_VERIFICATION_CODE", None)
    # JustWatch Country for watch plugin
    WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "IN")
    # Last.fm plugin for info: https://
    BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
    LASTFM_API = os.environ.get("LASTFM_API", None)
    LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
    LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
    LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
    # SpamWatch API you can get it from get api from http://t.me/SpamWatchBot?start=token
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    # Can get from https://coffeehouse.intellivoid.net/
    RANDOM_STUFF_API_KEY = os.environ.get("RANDOM_STUFF_API_KEY", None)
    # GitHub vars https://github.com/
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)
    GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
    # DeepAI value can get from https://deepai.org/
    DEEP_AI = os.environ.get("DEEP_AI", None)

    # DO NOT EDIT BELOW THIS LINE IF YOU DO NOT KNOW WHAT YOU ARE DOING
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
    # time.py
    COUNTRY = str(os.environ.get("COUNTRY", ""))
    TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))
    # For updater plugin
    UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "DOGE")
    # DON'T TOUCH THIS AT ALL
    SUDO_USERS: Set[int] = set()
    DOGEBOTLOGO = None
    BOTLOG = False
    BOTLOG_CHATID = 0


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
