# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
try:
    from . import BASE, SESSION
except ImportError:
    raise Exception("Hello!")

from sqlalchemy import Column, String


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


GMute.__table__.create(checkfirst=True)


def is_gmuted(sender_id):
    try:
        return SESSION.query(GMute).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gmute(sender):
    adder = GMute(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender):
    rem = SESSION.query(GMute).get((str(sender)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
