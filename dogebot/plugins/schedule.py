# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from asyncio import sleep

from dogebot import doge

plugin_category = "utils"


@doge.ub(
    pattern="schd (\d*) ([\s\S]*)",
    command=("schd", plugin_category),
    info={
        "header": "To schedule a message after given time(in seconds).",
        "usage": "{tr}schd <time_in_seconds>  <message to send>",
        "examples": "{tr}schd 120 hello",
    },
)
async def _(event):
    "To schedule a message after given time"
    dog = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = dog[1]
    ttl = int(dog[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
