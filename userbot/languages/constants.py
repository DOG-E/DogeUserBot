from random import choice

from .languages import lan
from .. import tr


#BASIS:
STARTINGDOGE=lan('startingdoge')
STARTUPDOGE=lan('startupdoge')
STARTEDUPDOGE=(
    f"\
    ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
    🐶 {lan('wowialive')}\n\
    🐾 {lan('dogeisready')}\n\
    ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
    {lan('writealivetc')}\n\
    {lan('writedogelc')}\n\
    ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
    {lan('visitoursup')}: t.me/DogeSup\n\
    ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖".format(tr)
)

MONTHS = {
    "Jan": lan("jan"),
    "Feb": lan("feb"),
    "Mar": lan("mar"),
    "Apr": lan("apr"),
    "May": lan("may"),
    "Jun": lan("jun"),
    "Jul": lan("jul"),
    "Aug": lan("aug"),
    "Sep": lan("sep"),
    "Oct": lan("oct"),
    "Nov": lan("nov"),
    "Dec": lan("dec"),
}

# ADMIN:
S_NOPERM = lan("noperm")

# AFK:
DEF_AFKS = [
    "🪐 I have a rush job right now,\n\
        can you send message later?\n\
        🙃 Don't worry, I will come again...",
    "📴 The person you are calling cannot answer the phone at the moment.\n\
        🔈 After the signal tone, you can leave your message on your own tariff.\n\
        💸 The message fee is 69¢.\n\
        🔉 beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep!",
    "✨ I'll be back in a few minutes.\n\
        💨 If I don't come, you read this message again.",
    "🎈 Sometimes the best things in life are worth waiting for...\n\
        💫 I'll be right back.",
    "🪐 I'm far from 7 seas & 7 countries,\n\
        🏝 7 waters & 7 continents,\n\
        ⛰ 7 mountains & 7 hills,\n\
        🏕 7 plains & 7 mounds,\n\
        🌊 7 pools & 7 lakes,\n\
        🌿 7 springs & 7 meadows,\n\
        🏙 7 cities & 7 neighborhoods,\n\
        🏘 7 blocks & 7 houses...\n\
        \n\
        📵 A place where even messages can't reach me!",
    "⌨ I'm away from the keyboard right now,\n\
        but if you shout loud enough at the screen,\n\
        I can hear you.",
    "🔮 If I were here,\n\
        I'd tell you where I am.\n\
        🍁 But I'm not the one who wrote this message,\n\
        Ask me when I get back...",
    "⛅ I'm far away!\n\
        ☁ I don't know when I'll be back!\n\
        🌬 Hopefully in a few minutes!",
    "☄ You don't know if I'm good or bad,\n\
        🌠 but I can tell that I'm away from the keyboard.",
    "🧑‍💻 🪐 Busy learning HTML to hack NASA.",
    "🕳 I went to the void.",
    "😪 I'm not in the mood to be alive.",
    "🗺 Busy proving the flat earth theory.",
]
DOGEAFK = f"{str(choice(DEF_AFKS))}"

# FILTERS:
FMSGTEXT = lan("fmsgtext")

# GROUP:
DEF_KICKMES = [
    "👋🏻 Bye bye I'm leaving!",
    "You'll notice that I'm not in the group the day I left unannounced...\n\
        That's why I'm leaving this message.",
    "🪐 I'm far from 7 seas & 7 countries,\n\
        🏝 7 waters & 7 continents,\n\
        ⛰ 7 mountains & 7 hills,\n\
        🏕 7 plains & 7 mounds,\n\
        🌊 7 pools & 7 lakes,\n\
        🌿 7 springs & 7 meadows,\n\
        🏙 7 cities & 7 neighborhoods,\n\
        🏘 7 blocks & 7 houses...\n\
        \n\
        🤡 In short, to the furthest place from this group..!",
]
DOGEKICKME = f"{str(choice(DEF_KICKMES))}"

# STICKERS:
DEF_KANGS = [
    "🤪 I'm stealing your sticker...",
    "😈 Long live theft..!",
    "🎫 I'm inviting this sticker to my own pack...",
    "🐾 I have to steal this..!",
    "💫 I'm imprisoning your sticker..!",
    "🪐 Why not this nice sticker in my package?",
    "👁‍🗨 Why shouldn't I have this nice sticker on my package as well?",
    "👀 Mr.Steal your sticker is stealing this sticker...",
    "🔮 I'm using witchery to kang this sticker...",

]
DOGEKANG = f"{str(choice(DEF_KANGS))}"

# OTHERS:
CMSGTEXT = lan("cmsgtext")
MMSGTEXT = lan("mmsgtext")
PMSGTEXT = lan("pmsgtext")
