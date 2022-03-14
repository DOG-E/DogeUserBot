# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from sample_config import Config


class Development(Config):
    # Bu değerleri https://my.telegram.org/apps adresinden alın.
    APP_ID = 6
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
    # Alive mesajınızda görüntülenecek ad.
    ALIVE_NAME = "Takma veya gerçek adınızı yazın ya da boş bırakın."
    # Herhangi bir PostgreSQL veritabanı oluşturun (ElephantSQL kullanmanızı öneririz) ve bu bağlantıyı buraya yapıştırın.
    DB_URI = "PostgreSQL bağlantınızı buraya yazın."
    # https://t.me/DogeHelperBot?start botumuzdan StringSession'i alabilirsiniz.
    STRING_SESSION = "StringSession kodunuzu buraya yazın."
    # @Botfather'da yeni bir bot oluşturun https://t.me/botfather ve BotToken'i buraya yapıştırın.
    BOT_TOKEN = "Bot tokeninizi buraya yazın ya da boş bırakın."
    # Gizli bir grup oluşturun, @MissRose_bot'u davet edin, /id yazın ve Rose'un mesajındaki Chat ID değerini buraya yapıştırın.
    PRIVATE_GROUP_BOT_API_ID = 0
    # Komutların başında kullanacağınız karakter.
    CMDSET = "."
    # Sudo komutları için komutların başında kullanacağınız karakter.
    SUDO_CMDSET = "."