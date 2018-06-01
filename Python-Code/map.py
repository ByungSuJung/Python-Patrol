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
	def __init__(self, center_lat, center_long, dist, num_cars,\
				 random_init=False, modified=False, traffic_tolerance=0.75):
		"""

		"""
		print("mapstart")
		self.traffic_tolerance = traffic_tolerance
		self.modified = modified
		self.random_init = random_init
		center_pt = (center_lat, center_long)
		print("before getting data")
		G = ox.graph_from_point(center_pt, distance=dist, network_type='drive', simplify=True) # distance = dist
		print("got data")
		self.node_map = self.set_intersections(G) #dictionary of nodes
		print("set node")
		self.edge_map = self.set_roads(G, self.node_map) #dictionary of edges
		print("set edge")
		self.add_edges(self.node_map, self.edge_map) #adds edges to nodes"""
		self.car_map = self.set_cars(G, self.edge_map, self.node_map, num_cars) #list of cars 
		print("set car")
		node_list = list(self.node_map.values())
		for node in node_list: 
			for car in self.car_map: 
				if car.current_position == node: 
					node.add(car)
	
	def set_intersections(self, G):
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
		#removed bad edge
		return edge_dict

	def add_edges(self, node_dict, edge_dict):
		for n in list(node_dict.values()): #list of intersection objs
			for e in list(edge_dict.values()): #list of road objs
				if e.u == n: #outgoing edge
					n.add_edge(e)
				if e.v == n:
					n.add_edge(e, out=False)
					

	def set_cars(self, G, edge_dict, node_dict, num_cars):
		start, destination = self.init_trip(node_dict)
		#start = node_dict[53213414]
		#destination = node_dict[53144260]
		#path = nx.dijkstra_path(G,start,destination)
		print("passing dest", destination.id)
		success, path = start.shortest_path(destination, modified=self.modified)
		print(success)
		print(path)
		if not success:  
			print("insde first loop")
			start, destination = self.init_trip(node_dict)
			success, path = start.shortest_path(destination, modified=self.modified)

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
			"""
			if destination == start:
				then what???
			"""
			car_list.append(Car(start, destination, map=self, path=path, modified=self.modified, traffic_tolerance=self.traffic_tolerance))
			
			if self.random_init: #if modified dijkstra
				print("assigning each car start and destnination")
				start, destination = self.init_trip(node_dict)
				start.reset_nodes()
				success, path = start.shortest_path(destination, modified=self.modified)

				while not success: 
					print("failed so go again")
					print(path)
					start, destination = self.init_trip(node_dict)
					start.reset_nodes()
					success, path = start.shortest_path(destination, modified=self.modified)

				print("success")
				print(path)
		return car_list

	def init_trip(self, node_dict): 
		start = rn.choice(list(node_dict.values()))
		destination = rn.choice(list(node_dict.values()))
		while start == destination: 
			destination = rn.choice(list(node_dict.values()))
		return start, destination