from py2neo import Graph, Node, Relationship
graph = Graph()

alice = Node("Person", name="Alice", age=22)
bob = Node("Person", name="Bob", age=33)
anna = Node("Person", name="Anna", age=44)
mary = Node("Person", name="Mary", age=55)

usr_name = input("Enter username: ")
print ("Username: " + usr_name)
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

query1 = "MATCH (user { username:'"
query1 = query1 + usr_name
query1 = query1 + "' })-[:"
query1 = query1 + usr_id
query1 = query1 + "]->(n) RETURN n"

results = graph.cypher.execute(query1);
print(results)

query2 = "MATCH (user { username:'"
query2 = query2 + usr_name
query2 = query2 + "' })-[:"
query2 = query2 + usr_id
query2 = query2 + "]->(n)-[r]->(m) RETURN r"

results2 = graph.cypher.execute(query2);
print(results2)

f = open('graph.txt', 'w')

f.write(usr_name+"\n")
f.write(usr_id+"\n")
s = str(results)
s2 = str(results2)
f.write(s)
f.write(s2)
f.close()

query3 = "MATCH (user { username:'"
query3 = query3 + usr_name
query3 = query3 + "' })-[:"
query3 = query3 + usr_id
query3 = query3 + "]->(n)-[r]->(m) DELETE r"

results3 = graph.cypher.execute(query3);

query4 = "MATCH (user { username:'"
query4 = query4 + usr_name
query4 = query4 + "' })-[r:"
query4 = query4 + usr_id
query4 = query4 + "]->(n) DELETE r, n"

results4 = graph.cypher.execute(query4);

print("Nodes plus relationships")
resultsAll = graph.cypher.execute("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
print(resultsAll)

