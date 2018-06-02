import osmnx as ox
import networkx as nx 
import numpy as np
import random as rn 
import constants as c
from intersection import Intersection
from road import Road 
from car import Car

class Map:
    """ Class: Map
    
    	Description:
    	* This class represents a real world layout of specified sections
    	  of the world in our simulation, with simplifying assumptions. 
    	  The main features of this class along with their descriptions can
          be seen in the member variables and member methods.

        Member Variables:
        * traffic_tolerance - The percentage of capacity met that is considered
        					  to be traffic.

        * modified - Flag indicating if the map will be running a modified
        			 version of dijkstra's algorithm or the standard.

        * random_init - Flag indicating if the cars on the map will be
        				randomly initialized or not.

        * node_map - The list of intersections (nodes) that are on the map.

        * edge_map - The list of roads (edges) that are on the map.

        * car_map - The list of cars that are initialized on the map.

        Member Methods:
        * set_intersections - Responsible for adding intersections to
        					  this specific map.

        * set_roads - Responsible for adding roads to this specific map.

        * add_edges - Determines for each edge if they are incoming or out
        			  going edges for specific nodes.

        * set_cars - Creates a certain amount of cars that will be placed
        			 on the map at some location.

        * init_trip - For each car in the map it gives them a starting
        			  and ending location.
    """

	def __init__(self, center_lat=47.608013, center_long=-122.335167, \
	dist=700, num_cars=1000, random_init=True, modified=False, \
	traffic_tolerance=0.75):

		print("mapstart")
		self.traffic_tolerance = traffic_tolerance
		self.modified = modified
		self.random_init = random_init
		center_pt = (center_lat, center_long)
		print("before getting data")
		G = ox.graph_from_point(center_pt, distance=dist, network_type='drive') 
		print("got data")
		self.node_map = self.set_intersections(G) #dictionary of nodes
		print("set node")
		self.edge_map = self.set_roads(G, self.node_map) #dictionary of edges
		print("set edge")
		self.add_edges(self.node_map, self.edge_map) #adds edges to nodes"""
		self.car_map = self.set_cars(G, self.edge_map, self.node_map, num_cars)
		print("set car")
		node_list = list(self.node_map.values())
		for node in node_list: 
			for car in self.car_map: 
				if car.current_position == node: 
					node.add(car)
	
	def set_intersections(self, G):
        """
        Method: set_intersections

        Method Arguments:
        * G - The graph of a real section of the world that will be produced
              from using the osmnx package and the lat and lon provided by the
              user input.

        Output:
        * A dictionary of the nodes created will be returned, where each node id
          is their key.
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
        Method: set_roads

        Method Arguments:
        * G - The graph of a real section of the world that will be produced
              from using the osmnx package and the lat and lon provided by the
              user input.

        * node_dict - The node dictionary that will be used to show which roads
          			  are connected to each other.

        Output:
        * A dictionary of the edges created will be returned, where each edge id
          is their key.
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
		#removed bad edge
		return edge_dict

	def add_edges(self, node_dict, edge_dict):
	        """
        Method: add_edges

        Method Arguments:
        * node_dict - Dictionary of nodes that are contained within the map.

        * edge_dict - Dictionary of edges that are contained within the map.

        Output:
        * No return value, but the edges will be placed into categories for
          incoming and out going edges of specific nodes.
          """

		for n in list(node_dict.values()): #list of intersection objs
			for e in list(edge_dict.values()): #list of road objs
				if e.u == n: #outgoing edge
					n.add_edge(e)
				if e.v == n:
					n.add_edge(e, out=False)
					

	def set_cars(self, G, edge_dict, node_dict, num_cars):
	    """
        Method: set_cars

        Method Arguments:
        * G - The graph of a real section of the world that will be produced
              from using the osmnx package and the lat and lon provided by the
              user input.

        * node_dict - Dictionary of nodes that are contained within the map.

        * edge_dict - Dictionary of edges that are contained within the map.

        * nums_cars - The number of cars that will be places on this map.

        Output:
        * No return value, but the provided number of cars will be created
          and placed within the list of cars for the map.
          """

		start, destination = self.init_trip(node_dict)
		#start = node_dict[53213414]
		#destination = node_dict[53144260]
		#path = nx.dijkstra_path(G,start,destination)
		print("passing dest", destination.id)
		success, path = start.shortest_path(destination, modified=False)
		print(success)
		print(path)
		while not success:  
			print("insde first loop")
			start.reset_nodes()
			start, destination = self.init_trip(node_dict)
			success, path = start.shortest_path(destination, modified=False)

		car_list = []
		for i in range(num_cars):
			car_list.append(Car(start, destination, map=self, path=path,\
			modified=self.modified, traffic_tolerance=self.traffic_tolerance))
			
			if self.random_init: #if modified dijkstra
				#print("assigning each car start and destnination")
				start, destination = self.init_trip(node_dict)
				start.reset_nodes()
				success, path = start.shortest_path(destination, modified=False)

				while not success: 
					#print("failed so go again")
					#print(path)
					start, destination = self.init_trip(node_dict)
					start.reset_nodes()
					success, path = start.shortest_path(destination, modified=False)

				print("success")
				print(path)
		return car_list

	def init_trip(self, node_dict):
	    """
        Method: init_trip

        Method Arguments:
        * node_dict - Dictionary of nodes that are contained within the map.

        Output:
        * The return value is a start and destination, this is used to provide
          a trip for a specific car within the map.
          """

		start = rn.choice(list(node_dict.values()))
		destination = rn.choice(list(node_dict.values()))
		while start == destination: 
			destination = rn.choice(list(node_dict.values()))
		return start, destination