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
		self.edge_list = []
		self.in_edges = []					#List - List of connected edges
		self.neighbor_nodes = []				#List - List of neighboring nodes
		self.cap = 0			#int - Allowed size of queue
		self.time_steps = 2	+ 1						#int - Number of time steps to pass through node
		self.visted = False							#bool - Used for dijkstra's shortest path
		self.value = sys.maxsize					#int - Used for dijkstra's shortest path
		self.trail = []	
		self.priority_Q = PriorityQueue()			#List - The list of nodes in the shortest path

	def __lt__(self, other): 
		return self.value <= other.value

	def __str__(self):
		return str(self.id)

	def add_edge(self, edge, out=True):
		self.edge_list.append(edge)
		if str(edge.u) == str(self):
			out = True
		else:
			out = False
		if out == True:
			self.out_edges.append(edge)
		else:
			self.in_edges.append(edge)
			self.cap += edge.num_lanes
		
		#Add the edge to list of edges
		#Determine which node your neighbor is
		#neighbor_node = edge.u if self.id \
		#!= edge.u.id else edge.v
		#self.neighbor_nodes.append(neighbor_node)#Add the node to your neighbor list

	def add(self, car):
		if(len(self.queue) + 1 <= self.cap):
			self.queue.append(car)					#Place the car onto the queue
			self.q_size += 1						#Properly track queue size
			car.ts_on_current_position = 1						#Reset the time on object for the car
			return True

		return False								#If it was not added to the queue return False

	def remove(self):
		self.queue.pop()							#Remove the front car from the queue
		self.q_size -= 1							#Properly track queue size

	def run(self): 
		for car in self.queue: 
			car.move()
	def isFull(self):
		return self.q_size >= self.cap


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
		self.value = 0 
		#self.priority_Q.put_nowait(self)
		print("here")
		current = self
		current.trail.append(current)
		while current != destination:
			current.visited = True
			current.relax_neighbors()
			print("before first pop")
			current = self.priority_Q.get_nowait()
			print("after first pop")

		"""if current == destination: 
			current.trail = 
			self.trail.append(current)
		else: 
			pass """
		return current.trail


	def relax_neighbors(self):
		for edge in self.out_edges: 
			print("relaxing")
			neighbor_node = edge.v
			temp_value = edge.time_steps + neighbor_node.time_steps
			if not neighbor_node.visted and temp_value < neighbor_node.value:
			#if temp_value < neighbor_node.value:
				neighbor_node.value = temp_value
				neighbor_node.trail = self.trail
				neighbor_node.trail.append(neighbor_node)
				#self.priority_Q.put_nowait((self.value, neighbor_node))
				self.priority_Q.put_nowait(neighbor_node)
				print("inside if")
			else: 
				print("inside else")
				pass 
	
	def reset_nodes(self):
		for node in self.map.node_list:
			node.priority_Q = PriorityQueue()
			node.visted = False
			node.value = sys.maxsize
			node.trail = []


