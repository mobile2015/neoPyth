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
