# Credits: @amnd33p
# Modified: @mrconfused
#
# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from datetime import datetime
from io import BytesIO
from traceback import format_exc

from requests import get
from selenium.webdriver import Chrome, ChromeOptions
from validators.url import url

from . import SS_API, Config, doge, eor, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="(ss|gis) ([\s\S]*)",
    command=("ss", plugin_category),
    info={
        "h": "To Take a screenshot of a website.",
        "u": "{tr}ss <link>",
        "e": "{tr}ss https://github.com/DOG-E/DogeUserBot",
    },
)
async def _(event):
    "To Take a screenshot of a website."
    if Config.CHROME_BIN is None:
        return await eor(event, "Need to install Google Chrome. Module Stopping.")
    dogevent = await eor(event, "**⏳ Processing...**")
    start = datetime.now()
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        # https://stackoverflow.com/a/53073789/4723940
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.CHROME_BIN
        await event.edit("`Starting Google Chrome BIN`")
        driver = Chrome(chrome_options=chrome_options)
        cmd = event.pattern_match.group(1)
        input_str = event.pattern_match.group(2)
        inputstr = input_str
        if cmd == "ss":
            dogurl = url(inputstr)
            if not dogurl:
                inputstr = "http://" + input_str
                dogurl = url(inputstr)
            if not dogurl:
                return await dogevent.edit("`The given input is not supported url`")
        if cmd == "gis":
            inputstr = "https://www.google.com/search?q=" + input_str
        driver.get(inputstr)
        await dogevent.edit("`Calculating Page Dimensions`")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        # Add some pixels on top of the calculated dimensions
        # for good measure to make the scroll bars disappear
        im_png = driver.get_screenshot_as_png()
        # saves screenshot of entire page
        await dogevent.edit("`Stoppping Chrome Bin`")
        driver.close()
        message_id = await reply_id(event)
        end = datetime.now()
        ms = (end - start).seconds
        hmm = f"**url:** {input_str} \n**Time:** `{ms} seconds`"
        await dogevent.delete()
        with BytesIO(im_png) as out_file:
            out_file.name = input_str + ".PNG"
            await event.client.send_file(
                event.chat_id,
                out_file,
                caption=hmm,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
    except Exception:
        await dogevent.edit(f"`{format_exc()}`")


@doge.bot_cmd(
    pattern="scapture ([\s\S]*)",
    command=("scapture", plugin_category),
    info={
        "h": "To Take a screenshot of a website.",
        "d": "For functioning of this command you need to set SS_API var",
        "u": "{tr}scapture <link>",
        "e": "{tr}scapture https://github.com/DOG-E/DogeUserBot",
    },
)
async def _(event):
    "To Take a screenshot of a website."
    start = datetime.now()
    message_id = await reply_id(event)
    if SS_API is None:
        return await eor(
            event,
            "`Need to get an API key from https://screenshotlayer.com/product and need to set it SS_API !`",
        )
    dogevent = await eor(event, "**⏳ Processing...**")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
    input_str = event.pattern_match.group(1)
    inputstr = input_str
    dogurl = url(inputstr)
    if not dogurl:
        inputstr = "http://" + input_str
        dogurl = url(inputstr)
    if not dogurl:
        return await dogevent.edit("`The given input is not supported url`")
    response_api = get(
        sample_url.format(SS_API, inputstr, "1", "2560x1440", "PNG", "1")
    )
    # https://stackoverflow.com/a/23718458/4723940
    contentType = response_api.headers["content-type"]
    end = datetime.now()
    ms = (end - start).seconds
    hmm = f"**url:** {input_str} \n**Time:** `{ms} seconds`"
    if "image" in contentType:
        with BytesIO(response_api.content) as screenshot_image:
            screenshot_image.name = "screencapture.png"
            try:
                await event.client.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=hmm,
                    force_document=True,
                    reply_to=message_id,
                )
                await dogevent.delete()
            except Exception as e:
                await dogevent.edit(str(e))
    else:
        await dogevent.edit(f"`{response_api.text}`")
