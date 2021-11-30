# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)


def start() -> scoped_session:
    database_url = Config.DB_URI
    if "postgres://" in database_url:
        database_url = database_url.replace("postgres:", "postgresql:")
    engine = create_engine(database_url)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    LOGS.error(
        "🚨  DB_URI yapılandırılmamış. Veritabanına bağlı özelliklerin sorunları olabilir."
    )
    LOGS.error(f"🚨 {str(e)}")
