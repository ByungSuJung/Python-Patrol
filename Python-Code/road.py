import queue as q

class Road(object):
    def __init__(self, id, start, destination, max_speed, num_lanes, length):
        # CONSTANTS
        self.AVG_CAR_LENGTH = 4.6 #meters, float
        self.ONE_TIME_STEP = 0.3 #seconds????        

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
        # for now 
       # print("num_lanes", self.num_lanes)
       # print("length", self.length)
        self.capacity = (int) ((self.num_lanes*self.length) / self.AVG_CAR_LENGTH)
        #print ("road capacity", self.capacity)
        

    def calculate_time_steps(self): 
        self.time_steps = \
        (int) (((self.length / self.max_speed)) / self.ONE_TIME_STEP) 
        #print("time_steps", self.time_steps)
    
    def add(self, car):
        self.queue.append(car)
        self.q_size += 1
        car.ts_on_current_position = 0 

    def remove(self): 
        self.queue.pop(0)
        self.q_size -= 1

    def run(self): 
        #print("road run start")
        for car in self.queue: 
            car.move()
        #print("road run done")
    

"""
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
    """
