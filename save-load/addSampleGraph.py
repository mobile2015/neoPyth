from py2neo import Graph, Node, Relationship
graph = Graph()

alice = Node("Person", name="Alice", age=22, sex="F")
bob = Node("Person", name="Bob", age=33, sex="M")
anna = Node("Person", name="Anna", age=44, sex="F")
mary = Node("Person", name="Mary", age=55, sex="F")

# Get username
usr_name = input("Enter username: ")
print ("Username: " + usr_name)
# Get user_id - relationship to nodes
usr_id = input("Enter user id: ")
print ("User id: " + usr_id)

user = Node("user", username=usr_name)

alice_knows_bob = Relationship(alice, "KNOWS", bob)
alice_knows_mary = Relationship(alice, "KNOWS", mary)
alice_knows_anna = Relationship(alice, "KNOWS", anna)
mary_knows_bob = Relationship(mary, "KNOWS", bob)
anna_knows_mary = Relationship(anna, "KNOWS", mary)
bob_knows_anna = Relationship(bob, "KNOWS", anna)

user_relation_alice = Relationship(user, usr_id, alice)
user_relation_bob = Relationship(user, usr_id, bob)
user_relation_anna = Relationship(user, usr_id, anna)
user_relation_mary = Relationship(user, usr_id, mary)

graph.create(alice_knows_bob)
graph.create(alice_knows_mary)
graph.create(alice_knows_anna)
graph.create(mary_knows_bob)
graph.create(anna_knows_mary)
graph.create(bob_knows_anna)

graph.create(user_relation_alice)
graph.create(user_relation_bob)
graph.create(user_relation_anna)
graph.create(user_relation_mary)


print("Nodes")
resultsAllNodes = graph.cypher.execute("MATCH (n) RETURN n")
print(resultsAllNodes)
print("Nodes plus relationships")
resultsAll = graph.cypher.execute("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
print(resultsAll)
