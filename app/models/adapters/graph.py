__author__ = 'rikkt0r'


class Graph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    @property
    def serialize(self):

        return {
            "nodes": [node.serialize for node in self.nodes],
            "edges": [edge.serialize for edge in self.edges]
        }