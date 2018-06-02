'''
#------------------------------------------------------------------------------#
File: road.py
Date: April 4th, 2018
By: Cole, Kris, Sam, And Trece

Purpose: This file contains the Road class that is responsible for 
         simulating the behaviors of a road in our traffic simulation.
#------------------------------------------------------------------------------#
'''

import queue as q #Import queueu package

class Road(object):
 """ Class: Road
    
        Description:
        * This class represents a real world road object within
          our simulation, with simplifying assumptions. The main
          features of this class along with their descriptions can
          be seen in the member variables and member methods.

        Member Variables:
        * AVG_CAR_LENGTH - Simplifying assumption of the size of the
                           cars on all the roads.

        * ONE_TIME_STEP - The value of what one time step is equal to,
                          currently set at .8 seconds.

        * id - The unique identifier given to this specific road to 
               differentiate it from all other roads.

        * u - The start intersection of the road.

        * v - The end intersection of the road.

        * max_speed - The maximum speed for the specified road.

        * num_lanes - The number of lanes the specified road has.

        * length - The length of the specified road.

        * queue - Queue of the cars on this road.

        * q_size - Current number of cars on this road.

        Member Methods:
        * __hash__ - Overwritten functionality of the hash function
                     to hash the id of each road.

        * __str__ - Overwrittnen functionality of the str function
                    used to print out the id of each road.

        * calculate_capacity - Calculates the capacity of this road
                               based off the number of lanes, the length,
                               the average car length.

        * calculate_time_step - Calculates the number of times steps it
                                takes to travel the road based off the
                                length, max speed, and the value of one
                                time step.

        * add - Responsible for adding cars onto the specified queue of the 
                road and making sure to adjust the size accordingly.

        * remove - Responsible for removing cars from the specified queue of the 
                   road and making sure to adjust the size accordingly.

        * run - Makes each car within the queue at on the road attempt to
                perform their move functionality.
          """

    def __init__(self, id, start, destination, max_speed, num_lanes, length):
        # CONSTANTS
        self.AVG_CAR_LENGTH = 4.6 #meters, float
        self.ONE_TIME_STEP = 0.8 #seconds????        

        self.id = id #int
        self.u = start #Node u 
        self.v = destination #Node v
        self.max_speed = max_speed #mph, int
        self.num_lanes = num_lanes #int
        self.length = length #meters, float
        self.calculate_time_steps() #int (floor)
        self.calculate_capacity() #int 
        self.queue = [] #Queue of the cars on this road.
        self.q_size = 0 #Current number of cars on this road.

    def __hash__(self):
        """
        Method: __hash__

        Method Arguments:
        * None

        Output:
        * Returns the hashed value of the string version of the road's id.
        """ 

        return hash(str(self))
    
    def __str__(self):
        """
        Method: __str__

        Method Arguments:
        * None

        Output:
        * Returns the string version of the road's id.
        """ 

        return str(self.id)

    def calculate_capacity(self):
        """
        Method: calculate_capacity

        Method Arguments:
        * None

        Output:
        * Returns the total capacity of cars able to be placed on the road at
          one time based off the number of lanes, the length, the average car length.
        """ 

        self.capacity = (int) ((self.num_lanes*self.length) / self.AVG_CAR_LENGTH)
        

    def calculate_time_steps(self):
        """
        Method: calculate_time_steps

        Method Arguments:
        * None

        Output:
        * Returns the amount of time steps required to travel the length of
          the road based off the length, max speed, and the value of one time step.
        """ 

        self.time_steps = \
        (int) (((self.length / self.max_speed)) / self.ONE_TIME_STEP) 
        if self.time_steps < 1: 
            self.time_steps = 1
    
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

        self.queue.remove(car)
        self.q_size -= 1

    def run(self):
        """
        Method: run

        Method Arguments:
        * None

        Output:
        * None
        """ 

        for car in self.queue: 
            car.move()
    
