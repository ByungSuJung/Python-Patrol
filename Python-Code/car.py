from road import Road as road
from intersection import Intersection as intersection 
	
class Car(object):
    def __init__(self, start, destination, map=None, path=None):
        self.map = map
        self.current_position = start
        self.destination = destination 
        self.ts_on_current_position = 0
        self.total_times_for_car = 0
        self.path = path # list of nodes from start to destination
        self.next_to_visit = path[1]
        self.visited = False
        self.done = False
    
    def update(self): 
        if self.visited: 
            pass
        else: 
            self.current_position.run()

    # move for normal and modified dijkstra 
    def move(self):
        if self.visited:
            return False
        if self.ts_on_current_position == self.current_position.time_steps: 
            if type(self.current_position) is intersection:
                can_move = self.try_move_from_node()
                #print(can_move)
                if can_move:
                    print("intersection to edge")
                    print("car id", self.map.car_map.index(self))
                    print(type(self.current_position), " ", self.current_position.id)
                    self.next_to_visit.add(self)
                    self.current_position.remove(self)
                    self.current_position = self.next_to_visit
                    print(type(self.current_position), " ", self.current_position.id)
                    #if self.current_position != self.destination:
                    temp = self.path.index(self.current_position) + 1 # index
                    print("index of temp = ", temp)
                    #if self.current_position != self.des
                    self.next_to_visit = self.path[temp] # next in given list of path
                else: 
                    pass
            else: # if on edge(road) 
                can_move = self.try_move_from_edge() 
                #print(can_move)
                if can_move: 
                    print("edge to intersection")
                    self.next_to_visit.add(self)
                    self.current_position.remove(self) 
                    self.current_position = self.next_to_visit
                    print("current_position:", self.current_position.id)
                    print("self.destination: ", self.destination.id)
                    if self.current_position != self.destination:
                        temp = self.path.index(self.current_position) + 1
                        print("temp index = ", temp)
                        print("length of list = ", len(self.path))
                    # in the intersection 
                        self.next_to_visit = self.path[temp]
                    else: 
                        print("reached destination")
                        print("index = ", self.path.index(self.current_position))
                        print("finished car", self.map.car_map.index(self))
                        self.destination.remove(self)
                        self.done = True
                        return True
                    """for edge in self.current_position.edge_list: 
                        if edge.destination == self.path[temp]: 
                            self.next_to_visit = self.path[temp]"""
                else: 
                    pass 
        else: 
            self.ts_on_current_position += 1
            #print(self.ts_on_current_position)
        self.total_times_for_car += 1     
        self.visited = True    
        #print("path", self.path)
        #for position in self.path: 
            #print(position.id, ", ")
        #print("current", self.current_position.id)
        return False
            
                    
    """
    def modified_move(self): 
        if self.ts_on_current_position == self.current_position.time_steps: 
            if type(self.current_position) is intersection:
                can_move = self.try_move_from_node()
                if can_move: 
                    self.current_position.remove()
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    self.next_to_visit = # now on edge so next node 
                else: 
                    pass
            else: #on edge
                can_move = self.try_move_from_edge()
                if can_move:
                    self.current_position.queue.remove()
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    self.next_to_visit = # now on node so next edge
                else: 
                    # change all the car in edge.queue become False 
                    # should I do this just going through all the cars
                    # in the queue? pop pushback pop pushback ?   
        else: 
            self.ts_on_obj += 1 
        self.total_times_for_car += 1
    """
    def try_move_from_node(self):
        # if total_times_for_car % 2 == 0: 
        #self.find_shortest_path()
        #print("here")
        return self.try_move_from_edge()
    
    # This is same as self.try_move() I just made one for readability 
    # and for possible later modification. 
    def try_move_from_edge(self):
        #print("type", type(self.next_to_visit))
        #print("q",  self.next_to_visit.q_size)
        #print("cap", self.next_to_visit.capacity) 
        return self.next_to_visit.q_size < self.next_to_visit.capacity

    def find_shortest_path(self): 
        # modified dijsktra
        self.path = self.current_position.find_shortest_path(self.destination)
        

if __name__ == '__main__': 
    myCar = Car() 