__author__ = 'rikkt0r'


class Edge:

    def __init__(self, edge):
        self.edge = edge

    @property
    def serialize(self):

        return {
            "source": self.edge.source,
            "target": self.edge.target
        }