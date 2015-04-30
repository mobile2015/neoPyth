__author__ = 'rikkt0r'


class Node:

    def __init__(self, node):
        self.node = node

    @property
    def serialize(self):

        return {
            "id": self.node.id,
            "name": self.node.name
        }