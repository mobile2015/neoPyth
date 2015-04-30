__author__ = 'rikkt0r'

from app import db
from app.models.adapters.graph import Graph
from app.models.adapters.helpers.node import Node
from app.models.adapters.helpers.edge import Edge


class ExampleModel:

    def __init__(self):
        pass

    @staticmethod
    def get_some_graph():

        nodes_tmp = db.cypher.execute("MATCH (c:Car)-[:HAS]->(:Part) RETURN DISTINCT ID(c) AS id, c.name AS name LIMIT 10")
        edges_tmp = db.cypher.execute("MATCH (c1:Car)-[:HAS]->(:Part)<-[:HAS]-(c2:Car) RETURN ID(c1) AS source, ID(c2) AS target LIMIT 10")

        nodes = [Node(node) for node in nodes_tmp]
        edges = [Edge(edge) for edge in edges_tmp]

        return Graph(nodes, edges)

