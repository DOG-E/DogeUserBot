try:
    from . import BASE, SESSION
except ImportError:
    raise AttributeError
from os import environ

from sqlalchemy import Column, String, UnicodeText


class Globals(BASE):
    __tablename__ = "globals"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value


Globals.__table__.create(checkfirst=True)


def gvarstatus(variable):
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


def addgvar(variable, value):
    if SESSION.query(Globals).filter(Globals.variable == str(variable)).one_or_none():
        delgvar(variable)
    adder = Globals(str(variable), value)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(variable):
    rem = (
        SESSION.query(Globals)
        .filter(Globals.variable == str(variable))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()


class Railway_Variables(BASE):
    __tablename__ = "Variables_Railway"
    VarName = Column(String(14), primary_key=True)
    Value = Column(UnicodeText, primary_key=True)

    def __init__(self, VarName, Value):
        self.Key = VarName
        self.Value = Value


Railway_Variables.__table__.create(checkfirst=True)


async def isr_set(key):
    """Basically to check if the var is already there or not."""
    try:
        _result = SESSION.query(Railway_Variables).get(key)
        if _result:
            return True
        return None
    finally:
        SESSION.close()


async def setr_var(key, value):
    """To insert a key and value in the table."""
    to_check = isr_set(key)
    if to_check:
        value_match = SESSION.query(Railway_Variables).get(value)
        if value != value_match:
            rem = SESSION.query(Railway_Variables).get(key)
            SESSION.delete(rem)
            SESSION.commit()
            variable = Railway_Variables(key, value)
            SESSION.add(variable)
            SESSION.commit()
            return True
        return False
    variable = Railway_Variables(key, value)
    SESSION.add(variable)
    SESSION.commit()
    return True


async def delr_var(key):
    """To delete the variable."""
    to_check = isr_set(key)
    if not to_check:
        if await getr_var(key):
            return "Click Clack!"
        return False
    rem = SESSION.query(Railway_Variables).get(key)
    SESSION.delete(rem)
    SESSION.commit()
    return True


async def getr_var(key, value):
    """To get the value of the var"""
    to_check = isr_set(key)
    ext_value = environ.get(key, None)
    if not to_check:
        if not ext_value:
            return False
        return ext_value
    value = SESSION.query(Railway_Variables).get(value)
    SESSION.close()
    return value
