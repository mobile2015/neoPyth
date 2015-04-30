from app import db


class Reset:

    def __init__(self):
        pass

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