'''
#------------------------------------------------------------------------------#
File: intersection.py
Date: April 4th, 2018
By: Cole, Kris, Sam, And Trece

Purpose: This file contains the Intersection class that is responsible for 
         simulating the behaviors of a intersection in our traffic simulation.
#------------------------------------------------------------------------------#
'''

#------------------Imports Statements-------------------#
from queue import PriorityQueue
import numpy as np
import sys
import matplotlib.pyplot as plt
#-------------------------------------------------------#

class Intersection(object):
    """ Class: Intersection
    
    	Description:
    	* This class represents a real world intersection object within
          our simulation, with simplifying assumptions. The main
          features of this class along with their descriptions can
          be seen in the member variables and member methods.

        Member Variables:
        * map - The realworld map that the car we be performing its actions on.

        * id - The unique identifier given to this specific intersection to 
        	   differentiate it from all other intersections.

       	* x - The x coordinate of this intersections position on the simulation
       		  map.

       	* y - The y coordinate of this intersections position on the simulation
       		  map.

        * queue - Represents the order of which the cars have arrived at this
        		  specific intersection, this is used to determine the order in
        		  which the cars will attempt to travel onto the roads (edges).

        * q_size - Keeps track of the total count of cars that are currently in
        		   the intersections queue. This is of importance to determine
        		   if the cars attempting to goto that intersection will be able
        		   to actually move onto it or do they have to remain on the road
        		   and possibly cause additional traffic.

        * capacity - The limit of allowed cars at the specific intersection. This
        			 too is of importance when creating a traffic effect, because
        			 cars won't be able to move onto the intersection if the
        			 intersection q_size is at its capacity.

        * out_edges - List of roads where their direction leads them straight out
        			  of this specific intersection.

        * in_edges - List of roads where their direction leads them straight into
        			 this specific intersection.

        * time_steps - The number of timesteps that are required for a car to pass
        			   this specific intersection.

        * visited - Flag that indicates if this specific node has already been
        			visited or not, this is only used when performing the normal
        			and/or modified dijkstra's algorithm.

        * value - Value that indicates the current weight of the node given its
        		  path to reach it, this too is only used when performing the 
        		  normal and/or modified dijkstra's algorithm.

        * trail - This shows the path that was taken to reach the current node,
        		  this is only used when performing the normal and/or modified
        		  dijkstra's algorithm.

        * priority_Q - The priorty queue that is used to determine the order for 
					   which nodes will be checked next when performing the normal
					   and modified dijkstra's algorithm.

        Member Methods:
        * __lt__ - Overwritting of the less than operator. This is because we
        		   wanted to put nodes into the priority queue based off their
        		   values.

        * add_edge - Responsible for determining if the edge is an incoming of
        			 an out going edge, then once figured out it will put that
        			 edge into the proper edge list of the node.

        * add - Responsible for adding cars onto the specified queue of the 
        		intersection and making sure to adjust the size accordingly.

        * remove - Responsible for removing cars onto the specified queue of the 
        		   intersection and making sure to adjust the size accordingly.

        * run - Makes each car within the queue at the intersection attempt to
        		perform their move functionality.

		* shortest_path - Finds the shortest path to the destination provided
						  using either normal or modified dijkstra's algorithm.

		* make_trail - Assisting function to shortest_path, this function creates
					   the path as list for the car to know which nodes to follow.

		* relax_neighbor - Assiting function to shortest_path, used to check all
						   neighboring nodes that are connected to the current node.

		* reset_nodes - Assisting function to shortest_path, used to reset all nodes
						dijkstra's used values to their starting values so that the
						algorithm can be used again througout the simulations.
    """

	def __init__(self, name, x, y, map=None):
		self.map = map
		self.id = name #int - Unique identifier for this node
		self.x = x #int - X coordinate on the map
		self.y = y #int - Y coordinate on the map
		self.queue = [] #Queue - Queue of Cars at this location
		self.q_size = 0 #int - Current number of elements in the queue
		self.out_edges = [] #List - List of out going connected edges
		self.in_edges = [] #List - List of incoming connected edges
		self.capacity = 0 #int - Allowed size of queue
		self.time_steps = 2	#int - Number of time steps to pass through node
		self.visited = False #bool - Used for dijkstra's shortest path
		self.value = sys.maxsize #int - Used for dijkstra's shortest path
		self.trail = []	
		self.priority_Q = PriorityQueue() #List - The list of nodes in the shortest path

	def __lt__(self, other):
	    """
	    Method: __lt__

        Method Arguments:
        * other - The other intersection that you will be comparing your value to.

        Output:
        * Return the boolean value of the result for self.value <= other.value
        """  

		return self.value <= other.value

	def add_edge(self, edge, out=True):
        """
        Method: add_edge

        Method Arguments:
        * edge - The edge that will be added to one of the intersections list
        		  of the edges.

        * out - Flag indicating if it is an out going or incoming edge, which
        		determines which list the edge will be added to.

        Output:
        * No return value, but the edge lists of the intersection will be
          adjusted accordingly.
        """ 

		if out == True:
			self.out_edges.append(edge)
			self.capacity += edge.num_lanes
		else:
			self.in_edges.append(edge)
			self.capacity += edge.num_lanes

	def add(self, car):
        """
        Method: add

        Method Arguments:
        * car - The car that is going to be added to this specific intersection.

        Output:
        * No return value, but the queue and the q_size will be adjusted accordingly.
        """ 

		self.queue.append(car)
		self.q_size += 1
		car.ts_on_current_position = 0 

	def remove(self, car):
        """
        Method: remove

        Method Arguments:
        * car - The car that is going to be removed from this specific intersection.

        Output:
        * No return value, but the queue and the q_size will be adjusted accordingly.
        """  

		self.queue.remove(car) #Remove the front car from the queue
		self.q_size -= 1 #Properly track queue size

	def run(self): 
		"""
        Method: run

        Method Arguments:
        * None

        Output:
        * None
        """ 

		for car in self.queue: 
			done = car.move()
			if done: 
				car.destination.remove(car)


	def shortest_path(self, destination, modified=False): 
	    """
        Method: shortest_path

        Method Arguments:
        * destination - The destination that needs to have a shortest path plotted
          to it from this specific node.

        * modified - Flag indicating if the path to the destination will be computed
        			 using normal or modified dijkstra's algorithm.

        Output:
        * Returns True if a path was found and the path that was found, if no path is
		  found False is returned and a error path is also returned.
        """ 

		#print("start point = ", self.id)
		#print("passed in destination = ", destination.id)
		self.value = 0
		priority_Q = PriorityQueue()
		current = self
		self.parent = None
		while current != destination:
			current.visited = True
			current.relax_neighbors(priority_Q, modified)
			if priority_Q.empty(): 
				return False, self.make_trail(current)
			current = priority_Q.get_nowait()
		return True, self.make_trail(current)

	def make_trail(self, current):
	    """
        Method: make_trail

        Method Arguments:
        * current - The current node to start creating the path from.

        Output:
        * Returns the path that has been found with the addition of adding
          edges that connect the nodes as part of the path.
        """ 

		result = [current]
		while current.parent != None: 
			parent = current.parent
			for edge in parent.out_edges:
				if edge.v == current: 
					result.insert(0, edge)
			result.insert(0, current.parent)
			current = current.parent
		return result

	def relax_neighbors(self, priority_Q, modified=False):
		"""
        Method: relax_neighbors

        Method Arguments:
        * priority_Q - The queue that is being used to keep track of which
        			   nodes to be visited next based of their values.

        * modified - Flag indicating if the path to the destination will be computed
        			 using normal or modified dijkstra's algorithm.

        Output:
        * No return value, but the nodes and priority queue will be adjusted 
          accordinly.
        """ 

		for edge in self.out_edges: 
			neighbor_node = edge.v
			if modified:
				temp_value = self.value + (edge.q_size / edge.capacity) \
						+ (neighbor_node.q_size / neighbor_node.capacity)
			else:
				temp_value = self.value + edge.time_steps + neighbor_node.time_steps
			if not neighbor_node.visited and temp_value < neighbor_node.value:
				neighbor_node.value = temp_value
				neighbor_node.parent = self
				priority_Q.put_nowait(neighbor_node)
			else:
				pass 
	
	def reset_nodes(self):
		"""
        Method: reset_nodes

        Method Arguments:
        * None

        Output:
        * No return value, but all nodes dijkstra's used values are set to their
          starting values so that the algorithm can be used again througout
          the simulations.
        """

		for node_id in self.map.node_map:
			self.map.node_map[node_id].visited = False
			self.map.node_map[node_id].value = sys.maxsize
			self.map.node_map[node_id].trail = []
