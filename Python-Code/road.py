import queue as q

class Road(object):
    def __init__(self, id, start, destination, max_speed, num_lanes, length):
        # CONSTANTS
        self.AVG_CAR_LENGTH = 4.6       # meters
        self.ONE_TIME_STEP = 0.3         

        self.id = id                    # float
        self.u = start              # Node u 
        self.v = destination  # Node v
        self.max_speed = max_speed      # int
        self.num_lanes = num_lanes      # int
        self.length = length            # int
        self.calculate_time_steps()     # int (floor)
        self.calculate_capacity()       # int 
        self.queue = q.Queue(maxsize=self.capacity)
        self.q_size = 0
        self.time = length/max_speed
    def __hash__(self):
        return hash(str(self))
    def __str__(self):
        return str(self.id)
    def calculate_capacity(self): 
        # for now 
        self.capacity = (self.num_lanes * self.length) / self.AVG_CAR_LENGTH
        self.capacity=10

    def calculate_time_steps(self): 
        self.time_steps = \
        (int) (((self.length / self.max_speed) * 3600) / self.ONE_TIME_STEP) 
    
    def add(self, car):
        if self.q_size + 1 <= self.capacity:
            self.queue.put_nowait(car)
            self.q_size += 1
            car.ts_on_current_position = 0
            return True
        return False
        

    def remove(self): 
        self.queue.get_nowait()
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
