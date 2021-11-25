# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from random import choice

SLAP_TEMPLATES = [
    "{u} {h} {v} with a {i}.",
    "{u} {h} {v} in the face with a {i}.",
    "{u} {h} {v} around a bit with a {i}.",
    "{u} {t} a {i} at {v}.",
    "{u} grabs a {i} and {t} it at {v}'s face.",
    "{u} {h} a {i} at {v}.",
    "{t} a few {i} at {v}.",
    "{u} put {v} in the friendzone.",
    "{u} slaps {v} with a DMCA takedown request!",
    "{u} sits on {v}'s face while slamming a {i} {w}.",
    "{u} starts slapping {v} silly with a {i}.",
    "{u} pins {v} down and repeatedly {h} them with a {i}.",
    "{u} RSA-encrypted {v} and deleted the private key.",
    "put {v} in check-mate.",
    "{u} hit {v} with a small, interstellar spaceship.",
    "{u} quickscoped {v}.",
    "{u} picks up a {i} and {h} {v} with it.",
    "made {v} a knuckle sandwich.",
    "{u} {h} {v} {w} with a {i}.",
    "{u} slapped {v} with pure nothing.",
    "{u} gave a friendly push to help {v} learn to swim in lava.",
    "sent {v} down the memory hole.",
    "threw {v} off a building.",
    "{u} spammed {v}'s email.",
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    lan("sitem3"),
    lan("sitem4"),
    lan("sitem5"),
    lan("sitem6"),
    lan("sitem7"),
    lan("sitem8"),
    lan("sitem9"),
    lan("sitem10"),
    lan("sitem11"),
    lan("sitem12"),
    lan("sitem13"),
    lan("sitem14"),
    lan("sitem15"),
    lan("sitem16"),
    lan("sitem17"),
    lan("sitem18"),
    lan("sitem19"),
    lan("sitem20"),
    lan("sitem21"),
    lan("sitem22"),
    lan("sitem23"),
    lan("sitem24"),
    lan("sitem25"),
    lan("sitem26"),
    lan("sitem27"),
    lan("sitem28"),
    lan("sitem29"),
    lan("sitem30"),
    lan("sitem31"),
    lan("sitem32"),
    lan("sitem33"),
    lan("sitem34"),
    lan("sitem35"),
    lan("sitem36"),
]

THROW = [
    lan("sthrow1"),
    lan("sthrow2"),
    lan("sthrow3"),
    lan("sthrow4"),
]

HIT = [
    lan("shit1"),
    lan("shit2"),
    lan("shit3"),
    lan("shit4"),
    lan("shit5"),
    lan("shit6"),
]

WHERE = [
    lan("swhere1"),
    lan("swhere2"),
    lan("swhere3"),
    lan("swhere4"),
]


async def slap(replied_user, event, DEFAULTUSER):
    """Construct a funny slap sentence!"""
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username
    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"
    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)
    where = choice(WHERE)
    return temp.format(
        u=DEFAULTUSER,
        v=slapped,
        i=item,
        h=hit,
        t=throw,
        w=where,
    )


UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]


SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "ლ(ﾟдﾟლ)",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "ლ｜＾Д＾ლ｜",
    "ლ（╹ε╹ლ）",
    "ლ(ಠ益ಠ)ლ",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "乁༼☯‿☯✿༽ㄏ",
    "ʅ（´◔౪◔）ʃ",
    "ლ(•ω •ლ)",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    "乁ʕ •̀ ۝ •́ ʔㄏ",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]


CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]


FACEREACTS = [
    [
        "( ͡° ͜ʖ ͡°)",
        "(ʘ‿ʘ)",
        "(✿´‿`)",
        "=͟͟͞͞٩(๑☉ᴗ☉)੭ु⁾⁾",
        "(*⌒▽⌒*)θ～♪",
        "°˖✧◝(⁰▿⁰)◜✧˖°",
        "✌(-‿-)✌",
        "⌒°(❛ᴗ❛)°⌒",
        "(ﾟ<|＼(･ω･)／|>ﾟ)",
        "ヾ(o✪‿✪o)ｼ",
    ],
    [
        "(҂⌣̀_⌣́)",
        "（；¬＿¬)",
        "(-｡-;",
        "┌[ O ʖ̯ O ]┐",
        "〳 ͡° Ĺ̯ ͡° 〵",
    ],
    [
        "(ノ^∇^)",
        "(;-_-)/",
        "@(o・ェ・)@ノ",
        "ヾ(＾-＾)ノ",
        "ヾ(◍’౪`◍)ﾉﾞ♡",
        "(ό‿ὸ)ﾉ",
        "(ヾ(´・ω・｀)",
    ],
    [
        "༎ຶ‿༎ຶ",
        "(‿ˠ‿)",
        "╰U╯☜(◉ɷ◉ )",
        "(;´༎ຶ益༎ຶ`)♡",
        "╭∩╮(︶ε︶*)chu",
        "( ＾◡＾)っ (‿|‿)",
    ],
    [
        "乂❤‿❤乂",
        "(｡♥‿♥｡)",
        "( ͡~ ͜ʖ ͡°)",
        "໒( ♥ ◡ ♥ )७",
        "༼♥ل͜♥༽",
    ],
    [
        "(・_・ヾ",
        "｢(ﾟﾍﾟ)",
        "﴾͡๏̯͡๏﴿",
        "(￣■￣;)!?",
        "▐ ˵ ͠° (oo) °͠ ˵ ▐",
        "(-_-)ゞ゛",
    ],
    [
        "(✖╭╮✖)",
        "✖‿✖",
        "(+_+)",
        "(✖﹏✖)",
        "∑(✘Д✘๑)",
    ],
    [
        "(＠´＿｀＠)",
        "⊙︿⊙",
        "(▰˘︹˘▰)",
        "●︿●",
        "(　´_ﾉ` )",
        "彡(-_-;)彡",
    ],
    [
        "-ᄒᴥᄒ-",
        "◖⚆ᴥ⚆◗",
    ],
    [
        "( ͡° ͜ʖ ͡°)",
        r"¯\_(ツ)_/¯",
        "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
        "ʕ•ᴥ•ʔ",
        "(▀̿Ĺ̯▀̿ ̿)",
        "(ง ͠° ͟ل͜ ͡°)ง",
        "༼ つ ◕_◕ ༽つ",
        "ಠ_ಠ",
        "(☞ ͡° ͜ʖ ͡°)☞",
        r"¯\_༼ ି ~ ି ༽_/¯",
        "c༼ ͡° ͜ʖ ͡° ༽⊃",
        "ʘ‿ʘ",
        "ヾ(-_- )ゞ",
        "(っ˘ڡ˘ς)",
        "(´ж｀ς)",
        "( ಠ ʖ̯ ಠ)",
        "(° ͜ʖ͡°)╭∩╮",
        "(ᵟຶ︵ ᵟຶ)",
        "(งツ)ว",
        "ʚ(•｀",
        "(っ▀¯▀)つ",
        "(◠﹏◠)",
        "( ͡ಠ ʖ̯ ͡ಠ)",
        "( ఠ ͟ʖ ఠ)",
        "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
        "(⊃｡•́‿•̀｡)⊃",
        "(._.)",
        "{•̃_•̃}",
        "(ᵔᴥᵔ)",
        "♨_♨",
        "⥀.⥀",
        "ح˚௰˚づ ",
        "(҂◡_◡)",
        "ƪ(ړײ)‎ƪ​​",
        "(っ•́｡•́)♪♬",
        "◖ᵔᴥᵔ◗ ♪ ♫ ",
        "(☞ﾟヮﾟ)☞",
        "[¬º-°]¬",
        "(Ծ‸ Ծ)",
        "(•̀ᴗ•́)و ̑̑",
        "ヾ(´〇`)ﾉ♪♪♪",
        "(ง'̀-'́)ง",
        "ლ(•́•́ლ)",
        "ʕ •́؈•̀ ₎",
        "♪♪ ヽ(ˇ∀ˇ )ゞ",
        "щ（ﾟДﾟщ）",
        "( ˇ෴ˇ )",
        "눈_눈",
        "(๑•́ ₃ •̀๑) ",
        "( ˘ ³˘)♥ ",
        "ԅ(≖‿≖ԅ)",
        "♥‿♥",
        "◔_◔",
        "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
        "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
        "( ఠൠఠ )ﾉ",
        "٩(๏_๏)۶",
        "┌(ㆆ㉨ㆆ)ʃ",
        "ఠ_ఠ",
        "(づ｡◕‿‿◕｡)づ",
        "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
        "“ヽ(´▽｀)ノ”",
        "༼ ༎ຶ ෴ ༎ຶ༽",
        "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
        "(づ￣ ³￣)づ",
        "(⊙.☉)7",
        "ᕕ( ᐛ )ᕗ",
        "t(-_-t)",
        "(ಥ⌣ಥ)",
        "ヽ༼ ಠ益ಠ ༽ﾉ",
        "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
        "ミ●﹏☉ミ",
        "(⊙_◎)",
        "¿ⓧ_ⓧﮌ",
        "ಠ_ಠ",
        "(´･_･`)",
        "ᕦ(ò_óˇ)ᕤ",
        "⊙﹏⊙",
        "(╯°□°）╯︵ ┻━┻",
        r"¯\_(⊙︿⊙)_/¯",
        "٩◔̯◔۶",
        "°‿‿°",
        "ᕙ(⇀‸↼‶)ᕗ",
        "⊂(◉‿◉)つ",
        "V•ᴥ•V",
        "q(❂‿❂)p",
        "ಥ_ಥ",
        "ฅ^•ﻌ•^ฅ",
        "ಥ﹏ಥ",
        "（ ^_^）o自自o（^_^ ）",
        "ಠ‿ಠ",
        "ヽ(´▽`)/",
        "ᵒᴥᵒ#",
        "( ͡° ͜ʖ ͡°)",
        "┬─┬﻿ ノ( ゜-゜ノ)",
        "ヽ(´ー｀)ノ",
        "☜(⌒▽⌒)☞",
        "ε=ε=ε=┌(;*´Д`)ﾉ",
        "(╬ ಠ益ಠ)",
        "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
        "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
        r"¯\_(ツ)_/¯",
        "ʕᵔᴥᵔʔ",
        "(`･ω･´)",
        "ʕ•ᴥ•ʔ",
        "ლ(｀ー´ლ)",
        "ʕʘ̅͜ʘ̅ʔ",
        "（　ﾟДﾟ）",
        r"¯\(°_o)/¯",
        "(｡◕‿◕｡)",
    ],
]
