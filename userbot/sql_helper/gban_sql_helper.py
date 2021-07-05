#    Copyright (C) 2020  sandeep.n(π.$)
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
from sqlalchemy import Column, String

from . import BASE, SESSION


class GBan(BASE):
    __tablename__ = "gban"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason


GBan.__table__.create(checkfirst=True)


def is_gbanned(chat_id):
    try:
        return SESSION.query(GBan).filter(GBan.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_gbanuser(chat_id):
    try:
        return SESSION.query(GBan).get(str(chat_id))
    finally:
        SESSION.close()


def dogegban(chat_id, reason):
    adder = GBan(str(chat_id), str(reason))
    SESSION.add(adder)
    SESSION.commit()


def dogeungban(chat_id):
    rem = SESSION.query(GBan).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_gbanned():
    rem = SESSION.query(GBan).all()
    SESSION.close()
    return rem
