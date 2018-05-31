import queue as q

class Road(object):
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
        self.queue = []
        self.q_size = 0

    def __hash__(self):
        return hash(str(self))
    
    def __str__(self):
        return str(self.id)

    def calculate_capacity(self): 
        self.capacity = (int) ((self.num_lanes*self.length) / self.AVG_CAR_LENGTH)
        

    def calculate_time_steps(self): 
        self.time_steps = \
        (int) (((self.length / self.max_speed)) / self.ONE_TIME_STEP) 
    
    def add(self, car):
        self.queue.append(car)
        self.q_size += 1
        car.ts_on_current_position = 0 

    def remove(self, car): 
        self.queue.remove(car)
        self.q_size -= 1

    def run(self): 
        for car in self.queue: 
            car.move()
    
