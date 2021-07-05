# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
import threading

from sqlalchemy import Column, PickleType, UnicodeText, distinct, func

from . import BASE, SESSION


class Dog_GlobalCollection(BASE):
    __tablename__ = "dog_globalcollection"
    keywoard = Column(UnicodeText, primary_key=True)
    contents = Column(PickleType, primary_key=True, nullable=False)

    def __init__(self, keywoard, contents):
        self.keywoard = keywoard
        self.contents = tuple(contents)

    def __repr__(self):
        return "<Dog Global Collection lists '%s' for %s>" % (
            self.contents,
            self.keywoard,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, Dog_GlobalCollection)
            and self.keywoard == other.keywoard
            and self.contents == other.contents
        )


Dog_GlobalCollection.__table__.create(checkfirst=True)

DOG_GLOBALCOLLECTION = threading.RLock()


class COLLECTION_SQL:
    def __init__(self):
        self.CONTENTS_LIST = {}


COLLECTION_SQL_ = COLLECTION_SQL()


def add_to_collectionlist(keywoard, contents):
    with DOG_GLOBALCOLLECTION:
        keyword_items = Dog_GlobalCollection(keywoard, tuple(contents))

        SESSION.merge(keyword_items)
        SESSION.commit()
        COLLECTION_SQL_.CONTENTS_LIST.setdefault(keywoard, set()).add(tuple(contents))


def rm_from_collectionlist(keywoard, contents):
    with DOG_GLOBALCOLLECTION:
        keyword_items = SESSION.query(Dog_GlobalCollection).get(
            (keywoard, tuple(contents))
        )
        if keyword_items:
            if tuple(contents) in COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set()):
                COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set()).remove(
                    tuple(contents)
                )
            SESSION.delete(keyword_items)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def is_in_collectionlist(keywoard, contents):
    with DOG_GLOBALCOLLECTION:
        keyword_items = COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set())
        return any(tuple(contents) == list1 for list1 in keyword_items)


def del_keyword_collectionlist(keywoard):
    with DOG_GLOBALCOLLECTION:
        keyword_items = (
            SESSION.query(Dog_GlobalCollection.keywoard)
            .filter(Dog_GlobalCollection.keywoard == keywoard)
            .delete()
        )
        COLLECTION_SQL_.CONTENTS_LIST.pop(keywoard)
        SESSION.commit()


def get_item_collectionlist(keywoard):
    return COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set())


def get_collectionlist_items():
    try:
        chats = SESSION.query(Dog_GlobalCollection.keywoard).distinct().all()
        return [i[0] for i in chats]
    finally:
        SESSION.close()


def num_collectionlist():
    try:
        return SESSION.query(Dog_GlobalCollection).count()
    finally:
        SESSION.close()


def num_collectionlist_item(keywoard):
    try:
        return (
            SESSION.query(Dog_GlobalCollection.keywoard)
            .filter(Dog_GlobalCollection.keywoard == keywoard)
            .count()
        )
    finally:
        SESSION.close()


def num_collectionlist_items():
    try:
        return SESSION.query(
            func.count(distinct(Dog_GlobalCollection.keywoard))
        ).scalar()
    finally:
        SESSION.close()


def __load_item_collectionlists():
    try:
        chats = SESSION.query(Dog_GlobalCollection.keywoard).distinct().all()
        for (keywoard,) in chats:
            COLLECTION_SQL_.CONTENTS_LIST[keywoard] = []

        all_groups = SESSION.query(Dog_GlobalCollection).all()
        for x in all_groups:
            COLLECTION_SQL_.CONTENTS_LIST[x.keywoard] += [x.contents]

        COLLECTION_SQL_.CONTENTS_LIST = {
            x: set(y) for x, y in COLLECTION_SQL_.CONTENTS_LIST.items()
        }

    finally:
        SESSION.close()


__load_item_collectionlists()
