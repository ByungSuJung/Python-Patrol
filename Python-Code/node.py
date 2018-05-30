import numpy as np
import sys
import matplotlib.pyplot as plt

class Node(object):
	def __init__(self, name, x, y):
		self.id = name								#int - Unique identifier for this node
		self.x = x 									#int - X coordinate on the map
		self.y = y 									#int - Y coordinate on the map
		self.queue = []								#Queue - Queue of Cars at this location
		self.q_size = 0								#int - Current number of elements in the queue
		self.edge_list = [] 						#List - List of connected edges
		self.neighbor_nodes = []					#List - List of neighboring nodes
		self.cap = len(self.edge_list)				#int - Allowed size of queue
		self.ts = 2									#int - Number of time steps to pass through node
		self.visted = False							#bool - Used for dijkstra's shortest path
		self.value = sys.maxsize					#int - Used for dijkstra's shortest path
		self.trail = None							#List - The list of nodes in the shortest path
        
	def __hash__(self):
            return hash(str(self))
	def __str__(self):
	    return str(self.id)+str(self.x)+str(self.y)
	def add_edge(self, edge):
		self.edge_list.append(str(edge))						#Add the edge to list of edges


		#self.neighbor_nodes.append(neighbor_node)	#Add the node to your neighbor list

	def add(self, car):
		if(len(self.queue) + 1 <= self.cap):
			self.queue.append(car)					#Place the car onto the queue
			self.q_size += 1						#Properly track queue size
			car.ts_on_obj = 0						#Reset the time on object for the car
			return True

		return False								#If it was not added to the queue return False

	def remove(self):
		self.queue.pop()							#Remove the front car from the queue
		self.q_size -= 1							#Properly track queue size

	def tick(self, modified):
		for car in self.queue:						#Go through each item in the queue if you can and move accordingly

			if(car.ts_on_obj == self.ts):			#If the car has been at the node long enough it'll try to move

				#Decide whcich function to run
				#based off the modified param
				moved = self.modi_dijkstra(car)	if \
				modified else car.follow_trail()

				if(moved):
					self.remove()					#Pop the car off the queue since it moved to an edge

			else:									#If it was not time for the car to move yet
				car.ts_on_obj += 1					#increment how long it's been at the node for
			
			car.total_ts += 1						#Keep track of the cars total time steps in transit

		def shortest_path(self, all_nodes):
			for car in self.queue:
				self.value = 0						#Set starting destination distance to zero
				start.trail = str(start.id)			#Update the trail
				to_vist = all_nodes					#Copy list of all nodes into a list seperate list to visit

				#Continue looking at each node until the destination has been visited
				while(not car.destination.visted and len(to_vist) > 0):

					#Sort the list in place by the node values, the values will be
					#sorted from smallest to largest
					to_vist.sort(key = lambda intesection: node.value, reverse=False)	#If this is too slow, we can figure out how to get
																						#the min node.value
					
					#Visit the node with the lowest value
					self.visit_node(to_vist[0])

					#Remove the front node from the to visit list since it has been visited
					to_vist.pop(0)

				car.path = car.destination.trail
				self.reset_nodes(all_nodes)

		def visit_node(self, node):
			node.visted = True

			#Edit each connected node to this current node
			for edge in node.edge_list:

				#Determine what node you are i.e. nodeA or nodeB
				my_node = edge.nodeA if node.id == edge.nodeA.id else edge.nodeB
				other_node = edge.nodeA if node.id != edge.nodeA.id else edge.nodeB

				#Make sure the node you're about to edit isn't already visited
				if(not other_node.visted):

					#Check if you've found a shorter path
					if(my_node.value + edge.length < other_node.value):
						other_node.value = my_node.value + edge.length#Update the distance to that node
						other_node.trail = my_node.trail.append(other_node)#Update where that distance came from

		def reset_nodes(self, all_nodes):
			for node in all_nodes:
				node.visted = False
				node.value = sys.maxsize
				node.trail = None

		def modi_dijkstra(self, car):
			decide = np.random.randint(0,2).astype(bool)

			if(decide):
				print("You've been give your next node")
				return True
			else:
				print("You can't move")
				return False
"""
#Testing area for this module
if __name__ == '__main__': 
	test = node("a", 1, 2)

	node = np.load("node.npy")
	edge = np.load("edge.npy")

	#print(edge)
	#print(node)

	lis = [1,2,3]
	print(lis)
	lis.pop(0)
	print(lis)
	x_vals = node[:, 1].astype(np.float64)
	y_vals = node[:, 2].astype(np.float64)

	plt.plot(x_vals, y_vals, 'o')
	#plt.show()
"""