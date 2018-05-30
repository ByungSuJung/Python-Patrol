from queue import PriorityQueue
import numpy as np
import sys
import matplotlib.pyplot as plt


class Intersection(object):
	def __init__(self, name, x, y, map=None):
		self.map = map
		self.id = name #int - Unique identifier for this node
		self.x = x #int - X coordinate on the map
		self.y = y #int - Y coordinate on the map
		self.queue = []								#Queue - Queue of Cars at this location
		self.q_size = 0								#int - Current number of elements in the queue
		self.out_edges = []
		self.in_edges = []					#List - List of connected edges
		self.neighbor_nodes = []				#List - List of neighboring nodes
		self.capacity = 0			#int - Allowed size of queue
		self.time_steps = 2							#int - Number of time steps to pass through node
		self.visited = False							#bool - Used for dijkstra's shortest path
		self.value = sys.maxsize					#int - Used for dijkstra's shortest path
		self.trail = []	
		self.priority_Q = PriorityQueue()			#List - The list of nodes in the shortest path

	"""def calculate_capacity(self): 
		sum = 0 
		for edge in self.out_edges:
			print(edge.num_lanes) 
			sum += edge.num_lanes

		for edge in self.in_edges:
			print("incoming", edge.num_lanes)
			sum += edge.num_lanes
		#print("sum", sum)
		return sum  """

	def __lt__(self, other): 
		return self.value <= other.value

	def add_edge(self, edge, out=True):
		if out == True:
			self.out_edges.append(edge)
			self.capacity += edge.num_lanes
		else:
			self.in_edges.append(edge)
			self.capacity += edge.num_lanes

	def add(self, car):
		self.queue.append(car)
		self.q_size += 1
		car.ts_on_current_position = 0 

	def remove(self, car):
		self.queue.remove(car)							#Remove the front car from the queue
		self.q_size -= 1							#Properly track queue size

	def run(self): 
		#print("intersection run start")
		for car in self.queue: 
			done = car.move()
			if done: 
				car.destination.remove(car)

		#print("intersection run end")


	"""
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
	"""

	def shortest_path(self, destination): 
		print("passed in destination = ", destination.id)
		self.value = 0 
		priority_Q = PriorityQueue()
		#self.priority_Q.put_nowait(self)
		#print("here")
		current = self
		self.parent = None
		#self.trail.append(current)
		while current != destination:
			current.visited = True
			current.relax_neighbors(priority_Q)
			#print("before first pop")
			current = priority_Q.get_nowait()
			print("just popped", current.id)
			#print(current.value)
			#print("after first pop")
			if current == destination: 
				print("final popped", current.id)
				##for position in current.trail: 
					##print("dijks trail: ")
					##print(position.id)
				

		"""if current == destination: 
			current.trail = 
			self.trail.append(current)
		else: 
			pass """
		result = [current]
		while current.parent != None: 
			parent = current.parent
			for edge in parent.out_edges:
				if edge.v == current: 
					result.insert(0, edge)
			result.insert(0, current.parent)
			current = current.parent
		#if current == self: 
		#	result.insert(0, current)

		for position in result: 
			print("dijks trail: ")
			print(position.id)
		#self.reset_nodes
		return result


	def relax_neighbors(self, priority_Q):
		for edge in self.out_edges: 
			#print("relaxing")
			neighbor_node = edge.v
			temp_value = self.value + edge.time_steps + neighbor_node.time_steps
			#print(temp_value)
			if not neighbor_node.visited and temp_value < neighbor_node.value:
			#if temp_value < neighbor_node.value:
				neighbor_node.value = temp_value
				neighbor_node.parent = self
				#neighbor_node.trail = self.trail
				#neighbor_node.trail.append(edge)
				#neighbor_node.trail.append(neighbor_node)
				#print("trail till now: ")
				#for position in neighbor_node.trail: 
				#	print(position.id, end=' ')
				#print()

				#self.priority_Q.put_nowait((self.value, neighbor_node))
				priority_Q.put_nowait(neighbor_node)
				#print("inside if")
			else: 
				#print("inside else")
				pass 
	
	def reset_nodes(self):
		for node_id in self.map.node_map:
			self.map.node_map[node_id].visited = False
			self.map.node_map[node_id].value = sys.maxsize
			self.map.node_map[node_id].trail = []


	"""
	def shortest_path(self, all_nodes):
		for car in self.queue:
			self.value = 0						#Set uing destination distance to zero
			u.trail = str(u.id)			#Update the trail
			to_vist = all_nodes					#Copy list of all nodes into a list seperate list to visit

			#Continue looking at each node until the destination has been visited
			while(not car.v.visted and len(to_vist) > 0):

				#Sort the list in place by the node values, the values will be
				#sorted from smallest to largest
				to_vist.sort(key = lambda intesection: node.value, reverse=False)	#If this is too slow, we can figure out how to get
																					#the min node.value
				
				#Visit the node with the lowest value
				self.visit_node(to_vist[0])

				#Remove the front node from the to visit list since it has been visited
				to_vist.pop(0)

			car.path = car.v.trail
			self.reset_nodes(all_nodes)
	
	def visit_node(self, node):
		node.visted = True

		#Edit each connected node to this current node
		for edge in node.out_edges:

			#Determine what node you are i.e. nodeA or nodeB
			my_node = edge.nodeA if node.id == edge.nodeA.id else edge.nodeB
			other_node = edge.nodeA if node.id != edge.nodeA.id else edge.nodeB

			#Make sure the node you're about to edit isn't already visited
			if(not other_node.visted):

				#Check if you've found a shorter path
				if(my_node.value + edge.length < other_node.value):
					other_node.value = my_node.value + edge.length#Update the distance to that node
					other_node.trail = my_node.trail.append(other_node)#Update where that distance came from

	

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