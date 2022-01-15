# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from threading import RLock

from sqlalchemy import Column, UnicodeText

try:
    from . import BASE, SESSION
except ImportError:
    raise AttributeError


class Global_msg(BASE):
    __tablename__ = "msg"
    cmd = Column(UnicodeText, primary_key=True, nullable=False)
    msg = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, cmd, msg):
        self.cmd = cmd
        self.msg = msg

    def __repr__(self):
        return "<Doge Global Messages lists '%s' for %s>" % (self.cmd, self.msg)

    def __eq__(self, other):
        return bool(isinstance(other, Global_msg)
                    and self.cmd == other.cmd
                    and self.msg == other.msg)


Global_msg.__table__.create(checkfirst=True)

CMD_INSERTION_LOCK = RLock()

def smsg(cmd, msg):
    with CMD_INSERTION_LOCK:
        try:
            SESSION.query(Global_msg).filter(Global_msg.cmd == cmd).delete()
        except:
            pass
        cmd = Global_msg(cmd, msg)
        SESSION.merge(cmd)
        SESSION.commit()


def gmsg(cm):
    try:
        MSG = SESSION.query(Global_msg).filter(Global_msg.cmd == cm).first()
        return MSG.msg
    except:
        return False
    

def dmsg(cm):
    try:
        SESSION.query(Global_msg).filter(Global_msg.cmd == cm).delete()
        SESSION.commit()
    except Exception as e:
        return e
    return True
