import osmnx as ox
import networkx as nx 
import numpy as np
from t_node import TNode 
from road import Road

class Driver:
	def __init__(self, center_lat=47.608013, center_long=-122.335167, dist=150):
		center_pt = (center_lat, center_long)
		graph = ox.graph_from_point(center_pt, network_type='drive', distance=dist)

		t_node_dict = 
		for n in graph.nodes(data=True):
			n = n[1]
			node_to_insert = TNode(n['osmid'],n['x'],n['y'])
			node_dict[n['osmid']] = node_to_insert
		

		self.node_map = node_dict
		
		edge_list = []
		id = 0
		for e in g.edges(data=True):
			f = e[2]
			print(f)
			start = e[0]
			destination = e[1]

			if 'maxspeed' in f.keys():
				max_speed =  int(f['maxspeed'][0].split(" ")[0]) 
			else:
				print("check if/else is working, maxspeed")
				max_speed = 25 

			if 'lanes' in f.keys():
				num_lanes = int(f['lanes'][0]) 
			else:
				print("check if/else is working, lanes")
				num_lanes = 1 

			length = f['length'] 

			edge_to_insert = Road(id, start, destination, max_speed, num_lanes, length)
		

			edge_list.append(edge_to_insert)
			id+=1

		self.edge_map = edge_list



    

