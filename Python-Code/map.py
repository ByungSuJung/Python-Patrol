import osmnx as ox
import networkx as nx 
import numpy as np
import random as rn 
from intersection import Intersection
from road import Road 
from car import Car

import utility as util

class Map:
	"""

	"""
	def __init__(self, center_lat=47.608013, center_long=-122.335167, dist=150, num_cars=500):
		"""

		"""
		#nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=1000)
		center_pt = (center_lat, center_long)
		G = ox.graph_from_point(center_pt, distance=300, network_type='drive') # distance = dist
		self.node_map = self.set_intersections(G) #dictionary of nodes
		#print(self.node_map)
		self.edge_map = self.set_roads(G, self.node_map) #dictionary of edges
		#print(self.edge_map)
		self.add_edges(self.node_map, self.edge_map) #adds edges to nodes"""
		#self.nodes = util.node_to_object(nodes)
		#self.edges = util.edge_to_object(edges)
		#for key, edge in self.edges.items():
		#	self.nodes[str(edge.u)].add_edge(edge))
		#	self.nodes[str(edge.u)].cap += edge.num_lanes
		#	self.nodes[str(edge.v)].add_edge(edge)
		#	self.nodes[str(edge.v)].cap += edge.num_lanes
		self.car_map = self.set_cars(G, self.edge_map, self.node_map, num_cars) #list of cars 
		node_list = list(self.node_map.values())
		for node in node_list: 
			for car in self.car_map: 
				if car.current_position == node: 
					node.add(car)
	
	def set_intersections(self, G):
		"""

		"""
		node_dict = {}
		for n in G.nodes(data=True):
			name = n[1]['osmid']
			x = n[1]['x']
			y = n[1]['y']
			node_to_insert = Intersection(name, x, y, self)
			if name in node_dict: 
				print("duplicate")
				pass
			else:
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
			if id in edge_dict: 
				print("duplicate edge")
			edge_dict[id] = edge_to_insert
			id+=1
		return edge_dict

	def add_edges(self, node_dict, edge_dict):
		for n in list(node_dict.values()): #list of intersection objs
			for e in list(edge_dict.values()): #list of road objs
				if e.u == n: #outgoing edge
					n.add_edge(e)
				if e.v == n:
					n.add_edge(e, out=False)
					

	def set_cars(self, G, edge_dict, node_dict, num_cars):
		"""

		"""

		start = rn.choice(list(node_dict.values()))
		destination = rn.choice(list(node_dict.values()))
		while start == destination: 
			destination = rn.choice(list(node_dict.values()))
		#start = node_dict[53213414]
		#destination = node_dict[53213413]
		#path = nx.dijkstra_path(G,start,destination)
		print("passing dest", destination.id)
		path = start.shortest_path(destination)
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
			car_list.append(Car(start, destination, map=self, path=path))
		return car_list
