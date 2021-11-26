# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from random import choice

# BASIS:
MONTHS = {
    "Jan": "Ocak",
    "Feb": "Şubat",
    "Mar": "Mart",
    "Apr": "Nisan",
    "May": "Mayıs",
    "Jun": "Haziran",
    "Jul": "Temmuz",
    "Aug": "Ağustos",
    "Sep": "Eylül",
    "Oct": "Ekim",
    "Nov": "Kasım",
    "Dec": "Aralık",
}


# AFK:
DEF_AFKS = [
    "🪐 I have a rush job right now,\
    \ncan you send message later?\
    \n🙃 Don't worry, I will come again...",
    "📴 The person you're calling cannot answer the phone at the moment.\
    \n🔈 After the signal tone, you can leave your message on your own tariff.\
    \n💸 The message fee is 69¢.\
    \n🔉 beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep!",
    "✨ I'll be back in a few minutes.\
    💨 If I don't come, you read this message again.",
    "🎈 Sometimes the best things in life are worth waiting for...\
    \n💫 I'll be right back.",
    "🪐 I'm far from 7 seas & 7 countries,\
    \n🏝 7 waters & 7 continents,\
    \n⛰ 7 mountains & 7 hills,\
    \n🏕 7 plains & 7 mounds,\
    \n🌊 7 pools & 7 lakes,\
    \n🌿 7 springs & 7 meadows,\
    \n🏙 7 cities & 7 neighborhoods,\
    \n🏘 7 blocks & 7 houses...\n\
    \n📵 A place where even messages can't reach me!",
    "⌨️ I'm away from the keyboard right now,\
    \nbut if you shout loud enough at the screen,\
    \n👂 I can hear you.",
    "🔮 If I were here,\
    \nI'd tell you where I am.\n\
    \n🍁 But I'm not the one who wrote this message,\
    \nAsk me when I get back...",
    "⛅ I'm far away!\
    \n☁ I don't know when I'll be back!\
    \n🌬 Hopefully in a few minutes!",
    "☄ You don't know if I'm good or bad,\
    \n🌠 but I can tell that I'm away from the keyboard.",
    "🧑‍💻 🪐 Busy learning HTML to hack NASA.",
    "🕳 I went to the void.",
    "😪 I'm not in the mood to be alive.",
    "🗺 Busy proving the flat earth theory.",
]
DOGEAFK = f"{str(choice(DEF_AFKS))}"


# ALIVE:
ALIVETEMP = "{msg}\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅoɢᴇ oғ - {mention}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅoɢᴇ ᴠᴇʀꜱɪoɴ - {dv}\n\
┃ ᴀʟɪᴠᴇ ꜱɪɴᴄᴇ - {uptime}\n\
┃ ꜱᴛᴀᴛᴜꜱ - {db}\n\
┃ ᴛᴇʟᴇᴛʜoɴ ᴠᴇʀꜱɪoɴ - {tv}\n\
┃ ᴘʏᴛʜoɴ ᴠᴇʀꜱɪoɴ - {pv}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴘɪɴɢ - {ping} ms\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛"


IALIVETEMP = "{msg}\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅoɢᴇ oғ - {mention}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛\n\
\n\
┏━━━━━━✦❘༻༺❘✦━━━━━━┓\n\
┃ ᴅoɢᴇ ᴠᴇʀꜱɪoɴ - {dv}\n\
┃ ᴀʟɪᴠᴇ ꜱɪɴᴄᴇ - {uptime}\n\
┃ ꜱᴛᴀᴛᴜꜱ - {db}\n\
┃ ᴛᴇʟᴇᴛʜoɴ ᴠᴇʀꜱɪoɴ - {tv}\n\
┃ ᴘʏᴛʜoɴ ᴠᴇʀꜱɪoɴ - {pv}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛"


# GROUP:
DEF_KICKMES = [
    "👋🏻 Bye bye I'm leaving from here!",
    "You'll notice that I'm not in the group the day I left unannounced...\
    \nThat's why I'm leaving this message.",
    "🪐 I'm far from 7 seas & 7 countries,\
    \n🏝 7 waters & 7 continents,\
    \n⛰ 7 mountains & 7 hills,\
    \n🏕 7 plains & 7 mounds,\
    \n🌊 7 pools & 7 lakes,\
    \n🌿 7 springs & 7 meadows,\
    \n🏙 7 cities & 7 neighborhoods,\
    \n🏘 7 blocks & 7 houses...\n\
    \n🤡 In short, to the furthest place from this group..!",
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


# HMM:
hm_st_rd_v = "**🐕‍🦺 Sorry dude.\
    \n🐾 Don't ask me to do this!\
    \n🐾 I won't do this to my developer.**"

m_st_rd_v = "\n\n<b>🧡 This user is my developer!</b>"


b_ng_y = "\n\n<b>🤡 This user has been banned from using Doge.</b>"

c_nf_rm_dg_y = "**🏳️‍🌈 I'M OBVIOUSLY A #CONFIRMEDGAY!**\n\n"

cc_nf_rm_dg_y = (
    f"{c_nf_rm_dg_y}**💨 BECAUSE I WAS TRYING TO ADD USERS HERE TO MY CONTACTS.**"
)

pc_nf_rm_dg_y = (
    f"{c_nf_rm_dg_y}**💨 BECAUSE I WAS TRYING TO ADD USERS HERE WATCH P*RN.**"
)

sc_nf_rm_dg_y = f"{c_nf_rm_dg_y}**💨 BECAUSE I WAS TRYING TO STEAL MEMBERS HERE.**"

sndmsgg_ys = "**🦮 SORRY DUDE!\
    \n💔 I won't work with you.\
    \n🐶 My admins have banned you from using @DogeUserBot!\n\
    \n💡 To find out why,\
    \n🤡 Check out @DogeGays\n\
    \n🌪 To appeal,\
    \n💬 You can write to my @DogeSup group.**"
