# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from random import getrandbits

from telethon.errors.rpcbaseerrors import ForbiddenError
from telethon.errors.rpcerrorlist import PollOptionInvalidError
from telethon.tl.types import InputMediaPoll, Poll

from . import Build_Poll, doge, eor, reply_id

plugin_category = "tool"


@doge.bot_cmd(
    pattern="poll(?:\s|$)([\s\S]*)",
    command=("poll", plugin_category),
    info={
        "header": "To create a poll.",
        "description": "If you doesnt give any input it sends a default poll",
        "usage": ["{tr}poll", "{tr}poll question ; option 1; option2"],
        "examples": "{tr}poll Are you an early bird or a night owl ;Early bird ; Night owl",
    },
)
async def pollcreator(dogpoll):
    "To create a poll"
    reply_to_id = await reply_id(dogpoll)
    string = "".join(dogpoll.text.split(maxsplit=1)[1:])
    if not string:
        options = Build_Poll(["Yah sure 😊✌️", "Nah 😏😕", "Whatever die sur 🥱🙄"])
        try:
            await dogpoll.client.send_message(
                dogpoll.chat_id,
                file=InputMediaPoll(
                    poll=Poll(
                        id=getrandbits(32),
                        question="👆👆So do you guys agree with this?",
                        answers=options,
                    )
                ),
                reply_to=reply_to_id,
            )
            await dogpoll.delete()
        except PollOptionInvalidError:
            await eor(
                dogpoll, "`A poll option used invalid data (the data may be too long).`"
            )
        except ForbiddenError:
            await eor(dogpoll, "`This chat has forbidden the polls`")
        except Exception as e:
            await eor(dogpoll, str(e))
    else:
        doginput = string.split(";")
        if len(doginput) > 2 and len(doginput) < 12:
            options = Build_Poll(doginput[1:])
            try:
                await dogpoll.client.send_message(
                    dogpoll.chat_id,
                    file=InputMediaPoll(
                        poll=Poll(
                            id=getrandbits(32),
                            question=doginput[0],
                            answers=options,
                        )
                    ),
                    reply_to=reply_to_id,
                )
                await dogpoll.delete()
            except PollOptionInvalidError:
                await eor(
                    dogpoll,
                    "`A poll option used invalid data (the data may be too long).`",
                )
            except ForbiddenError:
                await eor(dogpoll, "`This chat has forbidden the polls`")
            except Exception as e:
                await eor(dogpoll, str(e))
        else:
            await eor(
                dogpoll,
                "Make sure that you used Correct syntax `.poll question ; option1 ; option2`",
            )
