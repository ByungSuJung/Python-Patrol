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
		for car in self.queue: 
			done = car.move()
			if done: 
				car.destination.remove(car)

	def shortest_path(self, destination): 
		print("start point = ", self.id)
		print("passed in destination = ", destination.id)
		self.value = 0 
		priority_Q = PriorityQueue()
		current = self
		self.parent = None
		while current != destination:
			current.visited = True
			current.relax_neighbors(priority_Q)
			current = priority_Q.get_nowait()
		
		return self.make_trail(current)

	def make_trail(self, current):
		result = [current]
		while current.parent != None: 
			parent = current.parent
			for edge in parent.out_edges:
				if edge.v == current: 
					result.insert(0, edge)
			result.insert(0, current.parent)
			current = current.parent
		return result



	def relax_neighbors(self, priority_Q):
		for edge in self.out_edges: 
			neighbor_node = edge.v
			temp_value = self.value + edge.time_steps + neighbor_node.time_steps
			if not neighbor_node.visited and temp_value < neighbor_node.value:
				neighbor_node.value = temp_value
				neighbor_node.parent = self
				priority_Q.put_nowait(neighbor_node)
			else:
				pass 
	
	def reset_nodes(self):
		for node_id in self.map.node_map:
			self.map.node_map[node_id].visited = False
			self.map.node_map[node_id].value = sys.maxsize
			self.map.node_map[node_id].trail = []
