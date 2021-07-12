import asyncio

from userbot import doge

from ..core.managers import edl, eor
from ..helpers.utils import reply_id

plugin_category = "fun"

game_code = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
button = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
game_name = [
    "Tic-Tac-Toe",
    "Tic-Tac-Four",
    "Elephant XO",
    "Connect Four",
    "Rock-Paper-Scissors",
    "Rock-Paper-Scissors-Lizard-Spock",
    "Russian Roulette",
    "Checkers",
    "Pool Checkers",
]
game_list = "`1` :- Tic-Tac-Toe\n`2` :- Tic-Tac-Four\n`3` :- Elephant XO\n`4` :- Connect Four\n`5` :- Rock-Paper-Scissors\n`6` :- Rock-Paper-Scissors-Lizard-Spock\n`7` :- Russian Roulette\n`8` :- Checkers\n`9` :- Pool Checkers"


@doge.bot_cmd(
    pattern="game(?:\s|$)([\s\S]*)",
    command=("game", plugin_category),
    info={
        "header": "Play inline games",
        "description": "Start an inline game by inlinegamebot",
        "Game code & Name": {
            "1": "Tic-Tac-Toe",
            "2": "Tic-Tac-Four",
            "3": "Elephant XO",
            "4": "Connect Four",
            "5": "Rock-Paper-Scissors",
            "6": "Rock-Paper-Scissors-Lizard-Spock",
            "7": "Russian Roulette",
            "8": "Checkers",
            "9": "Pool Checkers",
        },
        "usage": "{tr}game <game code>",
        "examples": "{tr}game 3 ",
    },
)
async def igame(event):
    "Fun game by inline"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    data = dict(zip(game_code, button))
    name = dict(zip(game_code, game_name))
    if not input_str:
        await edl(
            event, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
        return
    if input_str not in game_code:
        dogevent = await eor(event, "`Give me a correct game code...`")
        await asyncio.sleep(1)
        await edl(
            dogevent, f"**Available Game Codes & Names :-**\n\n{game_list}", time=60
        )
    else:
        game = data[input_str]
        gname = name[input_str]
        await eor(
            event, f"**Game code `{input_str}` is selected for game:-** __{gname}__"
        )
        await asyncio.sleep(1)
        bot = "@inlinegamesbot"
        results = await event.client.inline_query(bot, gname)
        await results[int(game)].click(event.chat_id, reply_to=reply_to_id)
        await event.delete()
