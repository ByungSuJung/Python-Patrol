import osmnx as ox
import networkx as nx 
import numpy as np
import random as rn 
from intersection import Intersection
from road import Road 
from car import Car

class Map:
	"""

	"""
	def __init__(self, center_lat=47.608013, center_long=-122.335167, \
		dist=100, num_cars=10):
		"""

		"""
		center_pt = (center_lat, center_long)
		G = ox.graph_from_point(center_pt, network_type='drive', distance=dist)
		self.node_map = self.set_intersections(G) #dictionary of nodes
		self.edge_map = self.set_roads(G, self.node_map) #dictionary of edges
		self.add_edges(self.node_map, self.edge_map) #adds edges to nodes
		self.car_map = self.set_cars(G, self.edge_map, \
			self.node_map, num_cars) #list of cars 
		G.get_
	
	def set_intersections(self, G):
		"""

		"""
		node_dict = {}
		for n in G.nodes(data=True):
			name = n[1]['osmid']
			x = n[1]['x']
			y = n[1]['y']
			node_to_insert = Intersection(name, x, y, map=self)
			node_dict[name] = node_to_insert
		return node_dict

	def set_roads(self, G, node_dict):
		"""

		"""
		edge_dict = {}
		id = 0
		for e in G.edges(data=True):
			start = node_dict[e[0]]
			destination = node_dict[e[1]]

			if 'maxspeed' in e[2]:
				tmp = e[2]['maxspeed']
				if type(tmp) is list:
					max_speed = int(tmp[0].split(" ")[0])
				else:
					max_speed = int(tmp.split(" ")[0])
			else:
				max_speed = 25

			if 'lanes' in e[2]:
				tmp2 = e[2]['lanes']
				if type(tmp2) is list:
					num_lanes = int(tmp2[0])
				else:
					num_lanes = int(tmp2)
			else:
				num_lanes = 2

			length = int(e[2]['length']) 
			edge_to_insert = Road(id, start, destination, max_speed, \
				num_lanes, length)
			edge_dict[id] = edge_to_insert
			id+=1
		return edge_dict

	def add_edges(self, node_dict, edge_dict):
		for n in list(node_dict.values()): #list of intersection objs
			for e in list(edge_dict.values()): #list of road objs
				if e.u == n: #outgoing edge
					n.add_edge(e)
				if e.v == n: #incoming edge
					n.add_edge(e, False)

	def set_cars(self, G, edge_dict, node_dict, num_cars):
		"""

		"""
		start = rn.choice(list(node_dict.values()))
		
		destination = rn.choice(list(node_dict.values()))
		#path = nx.dijkstra_path(G,start,destination)
		path = start.shortest_path(destination)
		print(start.id)
		print(destination.id)
		print(path)
		car_list = []
		for i in range(num_cars):
			"""
			if rand node is full:
			Option A 
			init car on a diff node 
			option B
			init car on on next t-frame
			option C
			init car on nearest road obj where start node
			would be either null or the closest edge
			choosing option B 
			"""
			#start = rn.choice(node_dict.keys())
			#destination = rn.choice(node_dict.keys())
			"""
			if destination == start:
				then what???
			"""
			#path = nx.dijkstra_path(G,start,destination)
			car_list.append(Car(start, destination, path))
		return car_list



