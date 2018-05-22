import osmnx as ox
import networkx as nx 
import numpy as np
from node import node 
from road import Road

class Driver:
	def __init__(self, center_lat=47.608013, center_long=-122.335167):
		center_pt = (center_lat, center_long)
		g = ox.graph_from_point(center_pt, network_type='drive', \
			distance=1000)

		node_dict = {}
		for n in g.nodes(data=True):
			n = n[1]
			node_to_insert = node(n['osmid'],n['x'],n['y'])
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
				max_speed =  int(f['maxspeed'][0].split(" ")[0]) #doesnt grab correctly fix later
			else:
				print("check if/else is working, maxspeed")
				max_speed = 25 #temp, figure out later

			if 'lanes' in f.keys():
				num_lanes = int(f['lanes'][0]) #Doesnt grab correctly fix later 
			else:
				print("check if/else is working, lanes")
				num_lanes = 1 

			length = f['length'] 

			edge_to_insert = Road(id, start, destination, max_speed, num_lanes, length)
		
			#edge_to_insert = Road(id, e[0], e[1], \
			#int(f['maxspeed'].split(" ")[0]), int(f['lanes']), \
			#f['length'])
			edge_list.append(edge_to_insert)
			id+=1

		self.edge_map = edge_list
		#print(g.edges(data=True))
		#print(len(edges))
		#'osmid': 322777956, 'oneway': True, 'lanes': '2', 'name': 'South 
		# Jackson Street', 'highway': 'secondary', 'maxspeed': '30 mph', 
		# 'length': 51.632, 'geometry': <shapely.geometry.
		# linestring.LineString object at 0x7f46ca69d5f8>}
		#nodes, edges = ox.graph_to_gdfs(self.graph)
		#print("nodes items")
		#print(nodes.items)
		#print("nodes ")

#print(Driver().node_map[1730789422].x)


    

