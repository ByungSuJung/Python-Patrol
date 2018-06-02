'''
#------------------------------------------------------------------------------#
File: car.py
Date: April 4th, 2018
By: Cole, Kris, Sam, And Trece

Purpose: This file contains the Car class that is responsible for simulating
         the behaviors of a car in our traffic simulation.
#------------------------------------------------------------------------------#
'''

#------------------Imports Statements-------------------#
from road import Road as road
from intersection import Intersection as intersection 
#-------------------------------------------------------#
	
class Car(object):
    """ Class: Car
        
        Description:
        * This class represents a real world car object within
          our simulation, with simplifying assumptions. The
          main features of this class along with their descriptions 
          can be seen in the member variables and member methods.

        Member Variables:
        * map - The realworld map that the car we be performing its actions on.

        * current_position - Initial location of the car on the map.

        * destination - Destination that the car is attempting to reach on the map.

        * path - The current path that the car is told to travel, this can be
                 provided by the regular or modified dijkstra's algorithm.

        * next_to_vist - The list of nodes and edges that the car is going to be
                         visiting next. This is different from the path b/c the
                         path strictly provides the nodes and no edges.

        * visited - This is an indicator for if the car has performed an action
                    during the time step, meaning it is a flag that shows if the
                    car has moved or is stuck in traffic.

        * done - A flag that indicates when the car has reached its destination.

        * modified - Used to represent if a car will be running regular or the 
                     modified version of dijkstra's.

        Member Methods:
        * update - Updates the specific car, if it has not performed any actions
                   in that time step.

        * move - If the car is able to move, provided that there is no traffic,

        * try_move_from_node - Determines if moving from the node to an edge is
                               possible.

        * try_move_from_edge - Determines if moving from the edge to a node is
                               possible.

        * find_shortest_path - Determines if the car is using normal or modified
                               dijkstra's then get the shortest path from current
                               position to the destination.
    """

    def __init__(self, start, destination, map=None, path=None, modified=False, traffic_tolerance=0.75):
        self.TRAFFIC_TOLERANCE = traffic_tolerance #Capacity percent that is considered traffic
        self.map = map #The realworld map that the car we be performing its actions on
        self.current_position = start #Initial location of the car
        self.destination = destination #Desired destinaiton of the car
        self.ts_on_current_position = 0 #How long it's been on the road or at an intersection
        self.total_times_for_car = 0 #Keeps track of how long the car has been traveling
        self.path = path #list of nodes from start to destination
        self.next_to_visit = path[1] #The path that the car is supposed to follow
        self.visited = False #If the car has performed an action during a time step
        self.done = False #If the car has reached its destination
        self.modified = modified #If it should be using modified dijkstra
    
    def update(self):
        """
        Method: update

        Method Arguments:
        * None

        Output:
        * Nothing will be returned but the car will begin to attempt to either move
          or remain stuck in traffic.
        """ 

        if self.visited: 
            pass
        else: 
            self.current_position.run()

    # move for normal and modified dijkstra 
    def move(self):
        """
        Method: move

        Method Arguments:
        * None

        Output:
        * Nothing will be returned but the car will begin to attempt to either move
          or remain stuck in traffic, the actions for it's path will also be determined
          by either normal or modified dijkstra's.
        """ 

        if self.visited:
            return False
        if self.ts_on_current_position == self.current_position.time_steps: 
            if type(self.current_position) is intersection:
                can_move = self.try_move_from_node()
                if can_move:
                    #print("intersection to edge")
                    #print("car id", self.map.car_map.index(self))
                    #print(type(self.current_position), " ", self.current_position.id)
                    self.current_position.remove(self)
                    if not self.next_to_visit in self.path: 
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    #print(type(self.current_position), " ", self.current_position.id)
                    #print("HELPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                    if self.current_position in self.path: 
                        #print("HELPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                        #print("finished")
                    else: 
                        #print("error in intersection to edge ~~~~~~~~~~~~~~~~~~~~~~~~~~~``")
                        #print(self.current_position.id)
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                    
                else: 
                    pass
            else: # if on edge(road) 
                can_move = self.try_move_from_edge() 
                if can_move: 
                    #print("edge to intersection")
                    self.next_to_visit.add(self)
                    self.current_position.remove(self) 
                    print("current_position:", self.current_position.id)
                    print("self.destination: ", self.destination.id)
                    self.current_position = self.next_to_visit
                    if self.current_position != self.destination:
                        if self.current_position in self.path:
                            temp = self.path.index(self.current_position) + 1
                            print("temp index = ", temp)
                            print("length of list = ", len(self.path))
                            self.next_to_visit = self.path[temp]
                        else:
                            print(self.current_position.id)
                            print(self.path)
                            temp = self.path.index(self.current_position) + 1
                            print("temp index = ", temp)
                            print("length of list = ", len(self.path))
                            self.next_to_visit = self.path[temp]
                    # in the intersection 
                    else: 
                        print("reached destination")
                        print("index = ", self.path.index(self.current_position))
                        print("finished car", self.map.car_map.index(self))
                        self.current_position.remove(self)
                        self.done = True
                        return True
                else: 
                    pass 
        else: 
            self.ts_on_current_position += 1
        self.total_times_for_car += 1     
        self.visited = True    
        return False
            
    def try_move_from_node(self):
        """
        Method: try_move_from_node

        Method Arguments:
        * None

        Output:
        * Nothing will be returned but the car will determine if it is considered
          to be in traffic or if it is not in traffic, if it is not in traffic
          it will determine it's new shortest path.
        """ 

        if self.modified: 
            temp_value = self.next_to_visit.q_size / self.next_to_visit.capacity
            if temp_value > self.TRAFFIC_TOLERANCE:
                self.find_shortest_path()
            else: 
                pass
            
        return self.try_move_from_edge()
    
    def try_move_from_edge(self):
        """
        Method: try_move_from_edge

        Method Arguments:
        * None

        Output:
        * Nothing will be returned but the car will determine if it is considered
          to be in traffic or if it is not in traffic, if it is not in traffic
          it will continue to travel along the road.
        """ 

        return self.next_to_visit.q_size < self.next_to_visit.capacity

    def find_shortest_path(self):
        """
        Method: find_shortest_path
        
        Method Arguments:
        * None

        Output:
        * Nothing will be returned but the car will determine its new shortest
          path and adjust as needed.
        """
     
        # modified dijsktra
        if self.current_position != self.path[0]:
            self.current_position.reset_nodes()
            success, self.path = self.current_position.shortest_path(self.destination, modified=self.modified)
            if not success: 
                success, self.path = self.current_position.shortest_path(self.destination, modified=False)
            #while not success: 
                #success, self.path = self.current_position.shortest_path(self.destination)