#    Credts @Mrconfused
from geopy.geocoders import Nominatim
from telethon.tl.types import InputGeoPoint, InputMediaGeoPoint

from . import doge, eor, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="gps ([\s\S]*)",
    command=("gps", plugin_category),
    info={
        "header": "To send the map of the given location.",
        "usage": "{tr}gps <place>",
        "examples": "{tr}gps Hyderabad",
    },
)
async def gps(event):
    "Map of the given location."
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    dogevent = await eor(event, "`Finding...`")
    geolocator = Nominatim(user_agent="DogeUserBot")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=InputMediaGeoPoint(InputGeoPoint(lat, lon)),
            caption=f"**Location: **`{input_str}`",
            reply_to=reply_to_id,
        )
        await dogevent.delete()
    else:
        await dogevent.edit("`I coudn't find it`")
