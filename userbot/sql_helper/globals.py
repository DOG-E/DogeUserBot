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
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class Globals(BASE):
    __tablename__ = "globals"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value


Globals.__table__.create(checkfirst=True)


def gvar(variable):
    try:
        return (
            SESSION.query(Globals)
            .filter(Globals.variable == str(variable))
            .first()
            .value
        )
    except BaseException:
        return None
    finally:
        SESSION.close()


def sgvar(variable, value):
    if SESSION.query(Globals).filter(Globals.variable == str(variable)).one_or_none():
        dgvar(variable)
    adder = Globals(str(variable), value)
    SESSION.add(adder)
    SESSION.commit()


def dgvar(variable):
    rem = (
        SESSION.query(Globals)
        .filter(Globals.variable == str(variable))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()
