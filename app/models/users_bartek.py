__author__ = 'bartek'

from py2neo import Node
import uuid as uid


class Users:

    LABEL = "USERS"

    def __init__(self):
        pass

    @staticmethod
    def create_user(name):
        Node(Users.LABEL, uuid=uid.uuid1(), name=name)