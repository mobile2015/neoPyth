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

    @staticmethod
    def reset_cars(cars=100, parts=10, relations=800, relations_probability=0.1):

        # remove all
        db.cypher.execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")

        # create cars
        db.cypher.execute(
            """WITH ["audi", "bmw", "ford", "mercedes", "nissan", "opel", "peugeot", "renault", "toyota", "volkswagen"]
             AS names FOREACH (r IN range(0,100) | CREATE (:Car {id:r, name:names[r % size(names)]+" "+r}));"""
        )

        # create car parts
        db.cypher.execute(
            """WITH ["hybrid engine", "spare wheel", "computer", "digital speedometer", "sunroof",
             "alarm", "abs", "esp", "asr", "muffler"] AS names FOREACH
             (r IN range(0,9) | CREATE (:Part {id:r, name:names[r % size(names)]+" "+r}));"""
        )

        # add relations
        db.cypher.execute("MATCH (c:Car),(p:Part) WITH c,p LIMIT 800 WHERE rand() < 0.1 CREATE (c)-[:HAS]->(p);")

        # add indexes
        db.cypher.execute("create index on :Car(id);")
        db.cypher.execute("create index on :Part(id);")

