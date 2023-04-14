import threading

from sqlalchemy import Column, String

from QueenBot.modules.sql import BASE, SESSION


class VenomChats(BASE):
    __tablename__ = "venom_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


VenomChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_venom(chat_id):
    try:
        chat = SESSION.query(VenomChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()


def set_venom(chat_id):
    with INSERTION_LOCK:
        venomchat = SESSION.query(VenomChats).get(str(chat_id))
        if not venomchat:
            venomchat = VenomChats(str(chat_id))
        SESSION.add(venomchat)
        SESSION.commit()


def rem_venom(chat_id):
    with INSERTION_LOCK:
        venomchat = SESSION.query(VenomChats).get(str(chat_id))
        if venomchat:
            SESSION.delete(venomchat)
        SESSION.commit()
