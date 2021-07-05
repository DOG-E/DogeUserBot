# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import random

from telethon.errors.rpcbaseerrors import ForbiddenError
from telethon.errors.rpcerrorlist import PollOptionInvalidError
from telethon.tl.types import InputMediaPoll, Poll

from dogebot import doge

from ..core.managers import edit_or_reply
from . import Build_Poll, reply_id

plugin_category = "extra"


@doge.doge_cmd(
    pattern="poll(?:\s|$)([\s\S]*)",
    command=("poll", plugin_category),
    info={
        "header": "To create a poll.",
        "description": "If you doesnt give any input it sends a default poll",
        "usage": ["{tr}poll", "{tr}poll question ; option 1; option2"],
        "examples": "{tr}poll Are you an early bird or a night owl ;Early bird ; Night owl",
    },
)
async def pollcreator(dogepoll):
    "To create a poll"
    reply_to_id = await reply_id(dogepoll)
    string = "".join(dogepoll.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure 😊✌️", "Nah 😏😕", "Whatever die sur 🥱🙄"])
        try:
            await dogepoll.client.send_message(
                dogepoll.chat_id,
                file=InputMediaPoll(
                    poll=Poll(
                        id=random.getrandbits(32),
                        question="👆👆So do you guys agree with this?",
                        answers=options,
                    )
                ),
                reply_to=reply_to_id,
            )
            await dogepoll.delete()
        except PollOptionInvalidError:
            await edit_or_reply(
                dogepoll,
                "`A poll option used invalid data (the data may be too long).`",
            )
        except ForbiddenError:
            await edit_or_reply(dogepoll, "`This chat has forbidden the polls`")
        except exception as e:
            await edit_or_reply(dogepoll, str(e))
    else:
        dogeinput = string.split(";")
        if len(dogeinput) > 2 and len(dogeinput) < 12:
            options = Build_Poll(dogeinput[1:])
            try:
                await dogepoll.client.send_message(
                    dogepoll.chat_id,
                    file=InputMediaPoll(
                        poll=Poll(
                            id=random.getrandbits(32),
                            question=dogeinput[0],
                            answers=options,
                        )
                    ),
                    reply_to=reply_to_id,
                )
                await dogepoll.delete()
            except PollOptionInvalidError:
                await edit_or_reply(
                    dogepoll,
                    "`A poll option used invalid data (the data may be too long).`",
                )
            except ForbiddenError:
                await edit_or_reply(dogepoll, "`This chat has forbidden the polls`")
            except Exception as e:
                await edit_or_reply(dogepoll, str(e))
        else:
            await edit_or_reply(
                dogepoll,
                "Make sure that you used Correct syntax `.poll question ; option1 ; option2`",
            )
