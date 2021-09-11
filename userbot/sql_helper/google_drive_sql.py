# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from sqlalchemy import Column, String, Text

from . import BASE, SESSION


class GoogleDriveCreds(BASE):
    __tablename__ = "gdrive"
    user = Column(String, primary_key=True)
    credentials = Column(Text, nullable=False)

    def __init__(self, user):
        self.user = user


GoogleDriveCreds.__table__.create(checkfirst=True)


def save_credentials(user, credentials):
    saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
    if not saved_credentials:
        saved_credentials = GoogleDriveCreds(user)

    saved_credentials.credentials = credentials

    SESSION.add(saved_credentials)
    SESSION.commit()
    return True


def get_credentials(user):
    try:
        saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
        return saved_credentials.credentials if saved_credentials is not None else None
    finally:
        SESSION.close()


def clear_credentials(user):
    saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
    if saved_credentials:
        SESSION.delete(saved_credentials)
        SESSION.commit()
        return True
