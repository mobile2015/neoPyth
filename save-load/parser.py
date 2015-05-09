from py2neo import Graph, Node, Relationship

graph = Graph()

file = open("graph.txt",'r')

wierzch = 0
usr_id = ""
usr_name = ""

for i,line in enumerate(file):
	#-------------------------------------------
	if i == 0:
		if line[0] != ' ' or line[0] != '-':
			usr_name = line.replace("\n","")
		else:
			print ("Can't read user name!")
			break
	#-------------------------------------------	
	if i == 1:
		if line[0] != ' ' or line[0] != '-':
			usr_id = line.replace("\n","")
		else:
			print ("Can't read user id!")
			break
	#-------------------------------------------
	if i > 1:
		find_user = graph.cypher.execute("MATCH(n:user {username:\"" + usr_name + "\"}) RETURN n")
		if len(find_user) != 1:
			print ("User not found")
			break
	
		if line.replace(" ","") == "|n\n":
			wierzch = 1
			continue

		#--------------------------------------
		if wierzch == 1 and line[0] != '-':
			if line.replace(" ","") == "|r\n":
				wierzch = 2
				continue
			else:
				graph.cypher.execute("CREATE" + line.split('|')[1])
				graph.cypher.execute("MATCH(n:user {username:\"" + usr_name + "\"}),(m" + line.split('|')[1].split()[1] + " CREATE n-[:" + usr_id + "]->m")
		
		#---------------------------------------
		if wierzch == 2 and line[0] != '-':
			if line.replace(" ","") == '':
				wierzch = 0
				continue
			else:
				graph.cypher.execute("MATCH(n" + line.split('|')[1].split('-')[0].replace('(','') + ",(m" + line.split('|')[1].split('-')[2].replace('(','').replace('>','') + " CREATE n-[:" + line.split('|')[1].split('-')[1].split(':')[1] + "->m")