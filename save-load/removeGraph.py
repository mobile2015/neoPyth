from py2neo import Graph, Node, Relationship
graph = Graph()

# Get username
usr_name = input("Enter username: ")
print ("Username: " + usr_name)
# Get user_id
usr_id = input("Enter user id: ")
print ("User id: " + usr_id)

print("Nodes")
resultsAllNodes = graph.cypher.execute("MATCH (n) RETURN n")
print(resultsAllNodes)
print("Nodes plus relationships")
resultsAll = graph.cypher.execute("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
print(resultsAll)

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

print("Nodes")
resultsAllNodes = graph.cypher.execute("MATCH (n) RETURN n")
print(resultsAllNodes)
print("Nodes plus relationships")
resultsAll = graph.cypher.execute("START n=node(*) MATCH (n)-[r]->(m) RETURN n,r,m")
print(resultsAll)

