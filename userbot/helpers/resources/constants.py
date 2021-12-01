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
    "🪐 Şu anda acele bir işim var,\
    \nmesajınızı daha sonra gönderebilir misiniz?\
    \n🙃 Endişelenmeyin, size döneceğim...",
    "📴 Aradığınız kişi şu anda telefona cevap verememektedir.\
    \n🔈 Sinyal tonundan sonra, mesajınızı tarifeniz üzerinden bırakabilirsiniz.\
    \n💸 Mesaj ücreti ₺0.69'dir.\
    \n🔉 biiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiip!",
    "✨ Birkaç dakika içinde döneceğim.\
    💨 Eğer gelmezsem, bu mesajı tekrar oku.",
    "🎈 Bazen hayattaki en iyi şeyler beklemeye değer...\
    \n💫 Hemen döneceğim.",
    "🪐 7 deniz ve 7 ülkeden uzakta,\
    \n🏝 7 su ve 7 kıtadan,\
    \n⛰ 7 dağ ve 7 kayadan,\
    \n🏕 7 ova ve 7 höyükten,\
    \n🌊 7 havuz ve 7 gölden,\
    \n🌿 7 bahar ve 7 çayırdan,\
    \n🏙 7 şehir ve 7 mahalleden,\
    \n🏘 7 blok ve 7 evden...\n\
    \n📵 Kısaca, mesajların bile bana ulaşamayacağı bir yerdeyim!",
    "⌨️ Şu an Telegram'dan uzaktayım,\
    \nama ekrana yeterince yüksek sesle bağırırsan,\
    \n👂 Seni çok iyi duyabilirim.",
    "🔮 Burada olsaydım,\
    \nsana nerede olduğumu söylerdim.\n\
    \n🍁 ama bu mesajı yazan ben değilim.\
    \nGeri döndüğümde bunu bana sor.",
    "⛅ Uzaklardayım!\
    \n☁ Ne zaman döneceğimi bilmiyorum.\
    \n🌬 Belki de birkaç dakika içinde!",
    "☄ İyi ya da kötü olduğumu bilmiyorsun,\
    \n🌠 ama şu an Telegram'da olmadığımı söyleyebilirim.",
    "🧑‍💻 🪐 NASA'yı hack'lemek için HTML'yi öğrenmekle meşgul.",
    "🕳 Kara delikteyim.",
    "😪 Telegram'da olmak için havamda değilim.",
    "🗺 Düz Dünya teorisini kanıtlamakla meşgul.",
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
┃ ᴅoɢᴇ süʀüᴍü - {dv}\n\
┃ çᴀʟışᴍᴀ süʀᴇsɪ - {up}\n\
┃ ᴛᴇʟᴇᴛʜoɴ süʀüᴍü - {tv}\n\
┃ ᴘʏᴛʜoɴ süʀüᴍü - {pv}\n\
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
┃ ᴅoɢᴇ süʀüᴍü - {dv}\n\
┃ çᴀʟışᴍᴀ süʀᴇsɪ - {up}\n\
┃ ᴛᴇʟᴇᴛʜoɴ süʀüᴍü - {tv}\n\
┃ ᴘʏᴛʜoɴ süʀüᴍü - {pv}\n\
┗━━━━━━✦❘༻༺❘✦━━━━━━┛"


# GROUP:
DEF_KICKMES = [
    "👋🏻 Güle güle güle gittim buradan ayrılıyorum!",
    "Sizi habersiz bıraktığım gün grupta olamadığımı fark edeceksiniz ki ...\
    \nBu yüzden bu mesajı buraya bırakıyorum. ",
    "🪐 Buradan uzakta;\
    \n🗺️ 7 deniz ve 7 ülkeden uzakta,\
    \n🏝 7 su ve 7 kıtadan,\
    \n⛰ 7 dağ ve 7 kayadan,\
    \n🏕 7 ova ve 7 höyükten,\
    \n🌊 7 havuz ve 7 gölden,\
    \n🌿 7 bahar ve 7 çayırdan,\
    \n🏙 7 şehir ve 7 mahalleden,\
    \n🏘 7 blok ve 7 evden...\n\
    \n🤡 Kısaca, bu gruptan en uzak yere..!",
]
DOGEKICKME = f"{str(choice(DEF_KICKMES))}"


# STICKERS:
DEF_KANGS = [
    "🤪 Çıkartmayı dızlıyorum...",
    "😈 Yaşasın dızcılık..!",
    "🎫 Bu çıkartmayı paketime davet ediyorum...",
    "🐾 Bunu dızlamak zorundayım..!",
    "💫 Çıkartmayı hapsediyorum..!",
    "🪐 Neden bu güzel çıkartma, paketimde değilmiş ki?",
    "👁‍🗨 Neden paketimde bu güzel çıkartma olmamalı?",
    "👀 Bay Dızcı bu çıkartmayı dızlıyor...",
    "🔮 Bu efsanevi çıkartmayı dızlarken üstün büyücülük yeteneklerimi kullanıyorum...",
]
DOGEKANG = f"{str(choice(DEF_KANGS))}"


# HMM:
hm_st_rd_v = "**🐕‍🦺 Üzgünüm dostum.\
    \n🐾 Bunu yapmamı isteme!\
    \n🐾 Bunu sahibime yapmayacağım.**"

m_st_rd_v = "\n\n<b>🧡 Bu kullanıcı benim geliştiricim!</b>"


b_ng_y = "\n\n<b>🤡 Bu kullanıcı Doge'den yasaklandı.</b>"

c_nf_rm_dg_y = "**🏳️‍🌈 #ONAYLI_GAY BEN ONAYLANMIŞ BİR GAY'IM!**\n\n"

cc_nf_rm_dg_y = (
    f"{c_nf_rm_dg_y}**💨 ÇÜNKÜ BURADA KULLANICILARI KİŞİLERİME EKLEMEYE ÇALIŞIYORDUM.**"
)

pc_nf_rm_dg_y = f"{c_nf_rm_dg_y}**💨 ÇÜNKÜ BURADA PORNO İZLEMEYE ÇALIŞIYORDUM.**"

sc_nf_rm_dg_y = f"{c_nf_rm_dg_y}**💨 ÇÜNKÜ BURADA ÜYELERİ ÇALMAYA ÇALIŞIYORDUM.**"

sndmsgg_ys = "**🦮 ÜZGÜNÜM DOSTUM!\
    \n💔 Seninle çalışamam!\
    \n🐶 Yöneticilerim @DogeUserBot kullanmanı yasakladı.\n\
    \n💡 Sebebini öğrenmek için,\
    \n🤡 @DogeGays'ı kontrol edebilirsin.\n\
    \n🌪 İtiraz için,\
    \n💬 @TeleDoge'ye yazabilirsin.**"

l_gmsgg_ys = "🐶 Yöneticilerim sizi @DogeUserBot kullanmaktan alıkoydu!.\
    \n🐾 Telegram'da kayıtlı mesajlarınızı kontrol edin."
