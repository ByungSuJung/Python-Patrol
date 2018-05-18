import numpy as np
import queue as q

class Road(object):
    def __init__(self, id, start, destination, max_speed, num_lanes, time_steps, length):
        # CONSTANTS
        self.AVG_CAR_LENGTH = 4.6
        
        self.id = id                    # float
        self.start = start              # Node u 
        self.destination = destination  # Node v
        self.queue = q.Queue()          # Cars
        self.q_size = 0                 # int
        self.max_speed = max_speed      # int
        self.time_steps = time_steps    # int
        self.num_lanes = num_lanes      # int
        self.length = length            # int
        self.calculate_capacity()       # int 

    def calculate_capacity(self): 
        # for now 
        self.capacity = (self.num_lanes * self.length) / self.AVG_CAR_LENGTH

if __name__ == '__main__': 
    myRoad = Road(0, 153426, 141414, 40, 2, 5, 2111)
    print("id: ", myRoad.id)
    print("start: ", myRoad.start)
    print("destination: ", myRoad.destination)
    print("queue: ", myRoad.queue)
    print("q_size: ", myRoad.q_size)
    print("max_speed: ", myRoad.max_speed)
    print("time_steps: ", myRoad.time_steps)
    print("num_lanes: ", myRoad.num_lanes)
    print("length: ", myRoad.length)
    print("capcity: ", myRoad.capacity)
