__author__ = 'bartek'

from py2neo import Node, Relationship

class Groups:

    LABEL = "GROUP"

    @staticmethod
    def create_group(db, name, owner):
        node = Node(Groups.LABEL, name=name)
        db.create(node)
        rel = Relationship(owner, Relationships.OWNS, node)
        db.create(rel)

    @staticmethod
    def add_user(db, group, user):
        rel = Relationship(user, Relationships.IS_MEMBER, group)
        db.create(rel)


class Relationships:

    IS_MEMBER = "IS_MEMBER"
    OWNS = "OWNS"