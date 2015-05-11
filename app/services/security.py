__author__ = 'bartek'

from py2neo import Relationship


class Security:

    def __init__(self):
        pass

    KNOWS = "KNOWS"
    SECURITY = "SECURITY"
    IS_MEMBER_OF = "IS_MEMBER_OF"

    def __int__(self):
        pass

    @staticmethod
    def create_person(db, person):
        db.create(person)

    @staticmethod
    def create_permission(db, entity, resource, permissions):
        sec = Relationship(entity, Security.SECURITY, resource, permissions=permissions)
        db.create(sec)

    @staticmethod
    def add_person_to_group(db, person, group):
        sec = Relationship(group, Security.IS_MEMBER_OF, person)
        db.create(sec)

    @staticmethod
    def __accessable(db, user, resource, permissions):
        relations = db.match(user, Security.SECURITY, resource)
        for rel in relations:
            if rel[Security.SECURITY].contains(permissions):
                return True
        return False

    @staticmethod
    def has_access(db, user, resource):
        return Security.__accessable(db, user, resource, Permissions.R)

    @staticmethod
    def can_write(db, user, resource):
        return Security.__accessable(db, user, resource, Permissions.W)


class Permissions:

    RW = "RW"
    R = "R"
    W = "W"

    def __init__(self):
        pass