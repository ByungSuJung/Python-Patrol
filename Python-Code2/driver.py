import osmnx as ox
import networkx as nx 
import numpy as np
"""
from t_node import TNode #Change to Node 
"""
from road import Road

class Driver:
	def __init__(self, center_lat=47.608013, center_long=-122.335167, dist=500):
		center_pt = (center_lat, center_long)
		graph = ox.graph_from_point(center_pt, network_type='drive', distance=dist)

		edge_list = []
		id = 0
		for e in graph.edges(data=True):
			start = e[0]
			destination = e[1]
			tmp = e[2]['maxspeed']
			max_speed = tmp.split(" ")[0]
			num_lanes = e[2]['lanes'] 
			length = e[2]['length'] 
			#edge_to_insert = Road(id, start, destination, max_speed, num_lanes, length)
			#edge_list.append = edge_to_insert
			id+=1
		#self.edge_map = edge_dict

		node_dict = {}
		for n in graph.nodes(data=True):
			name = n[1]['osmid']
			x = n[1]['x']
			y = n[1]['y']
			outgoing_edges = []
			incoming_edges = []
			accsessible_nodes = []
			for e in edge_list:
				if e.u == name:
					outgoing_edges.append(e.id)
					accsessible_nodes.append(e.v)
				if e.v == name:
					incoming_edges.append(e.id)

		
			#node_to_insert = TNode()
			#node_dict[n['osmid']] = node_to_insert
		self.node_map = node_dict
		


		car_dict = {}


    

