import queue as q
import constants as c
import numpy as np

class Road(object):
    def __init__(self, id, start, destination, max_speed, num_lanes, length):
        # CONSTANTS
        self.AVG_CAR_LENGTH = 4.6       # meters
        self.ONE_TIME_STEP = 0.3         
        self.origin_steps = None
        self.id = id                    # float
        self.u = start              # Node u 
        self.v = destination  # Node v
        self.max_speed = max_speed      # int
        self.num_lanes = num_lanes      # int
        self.length = length            # int
        self.calculate_time_steps()     # int (floor)
        self.calculate_capacity()       # int 
        #self.queue = q.Queue(maxsize=self.capacity)
        self.queue = []
        self.q_size = 0
        self.time = length/max_speed
    def __hash__(self):
        return hash(str(self))
    def __str__(self):
        return str(self.id)
    def _re_time_steps_(self):
        self.time_steps = self.origin_steps * np.exp(1.2*self.q_size/self.capacity) 

    def calculate_capacity(self): 
        # for now 
        self.capacity = (self.num_lanes * self.length) / self.AVG_CAR_LENGTH

    def calculate_time_steps(self): 
        self.time_steps = \
        (int) (((self.length / self.max_speed) * 3600) / c.ONE_TIME_STEP) + 1
        self.origin_steps = self.time_steps
    
    def add(self):
        if self.q_size + 1 <= self.capacity:
            #self.queue.put_nowait('car')
            self.queue.append('car')
            self.q_size += 1
            #car.ts_on_current_position = 1
            self._re_time_steps_()
            return True
        return False
        

    def remove(self):
        self._re_time_steps_()
        #self.queue.get_nowait()
        self.queue.pop(0)
        self.q_size -= 1
        #car.ts_on_current_position = 0 

if __name__ == '__main__': 
    myRoad = Road(0, 153426, 141414, 40, 2, 2111)
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
