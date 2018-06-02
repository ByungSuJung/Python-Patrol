import sys
import numpy as np 

class node(object):
	def __init__(self, node_name):
		self.id = node_name#Name of node
		self.edges = []#List of connected edges
		self.visted = False#If the node has been visited
		self.value = sys.maxsize#Set initial value to very large number
		self.trail = None#Keep track of its trail

	#Add an edge to the nodes edge list
	def add_edge(self, edge):
		self.edges.append(edge)

#NOTE: These edges are undirected at the moment
class edge(object):
	def __init__(self, nodeA, nodeB, length):
		self.nodeA = nodeA#One of the nodes connected to the edge
		self.nodeB = nodeB#The other node connected to the edge
		self.length = length#The length of the edge

class graph(object):
	def __init__(self, nodes = [], edges = []):
		self.graph_nodes = nodes
		self.graph_edges = edges


def shortest_path(start, destination):
	start.value = 0#Set starting destination distance to zero
	start.trail = start.id#Update the trail
	to_vist = all_nodes#Copy list of all nodes into a list seperate list to visit

	#Continue looking at each node until the destination has been visited
	while(not destination.visted and len(to_vist) > 0):
		#Sort the list in place by the node values, the values will be
		#sorted from smallest to largest
		to_vist.sort(key = lambda node: node.value, reverse=False)
		
		#Visit the node with the lowest value
		visit_node(to_vist[0])

		#Remove the front node from the to visit list since it has been visited
		to_vist = to_vist[1:]		

	print("Trail: " + destination.trail + ", Distance: " + str(destination.value))

	reset_nodes()#Reset the values of the nodes for later short path runs

def visit_node(node):
	node.visted = True

	#Edit each connected node to this current node
	for edge in node.edges:

		#Determine what node you are i.e. nodeA or nodeB
		my_node = edge.nodeA if node.id == edge.nodeA.id else edge.nodeB
		other_node = edge.nodeA if node.id != edge.nodeA.id else edge.nodeB

		#Make sure the node you're about to edit isn't already visited
		if(not other_node.visted):

			#Check if you've found a shorter path
			if(my_node.value + edge.length < other_node.value):
				other_node.value = my_node.value + edge.length#Update the distance to that node
				other_node.trail = my_node.trail + " " + other_node.id#Update where that distance came from

	return

#Reset all the nodes to their initial values
def reset_nodes():
	for node in all_nodes:
		node.visted = False
		node.value = sys.maxsize
		node.trail = None

#Print the graph to make sure the connections are correct
def print_connections():
	for node in all_nodes:
		for edge in node.edges:
			print("Node (" + str(node.id) + ") Has Edge: " + str(edge.nodeA.id) + "-" + str(edge.nodeB.id))

#----------------------Initialize the Nodes-----------------------#
A = node('A')
B = node('B')
C = node('C')
D = node('D')
E = node('E')
F = node('F')
G = node('G')

all_nodes = [A, B, C, D, E, F, G]
#-----------------------------------------------------------------#

#----------------------Initialize the Edges-----------------------#
A_B = edge(A, B, 7)
A_C = edge(A, C, 4)
A_D = edge(A, D, 6)

B_E = edge(B, E, 12)

C_E = edge(C, E, 4)
C_G = edge(C, G, 7)
C_F = edge(C, F, 3)

D_F = edge(D, F, 10)

E_G = edge(E, G, 5)

F_G = edge(F, G, 9)
#-----------------------------------------------------------------#

#----------Assign each edge to their corresponding nodes----------#
A.add_edge(A_B)
A.add_edge(A_C)
A.add_edge(A_D)

B.add_edge(A_B)
B.add_edge(B_E)

C.add_edge(A_C)
C.add_edge(C_E)
C.add_edge(C_F)
C.add_edge(C_G)

D.add_edge(A_D)
D.add_edge(D_F)

E.add_edge(E_G)
E.add_edge(C_E)
E.add_edge(B_E)

F.add_edge(C_F)
F.add_edge(D_F)
F.add_edge(F_G)

G.add_edge(E_G)
G.add_edge(F_G)
G.add_edge(C_G)
#-----------------------------------------------------------------#

shortest_path(F, B)
shortest_path(A, G)