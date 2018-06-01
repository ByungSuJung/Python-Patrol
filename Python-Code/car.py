from road import Road as road
from intersection import Intersection as intersection 
	
class Car(object):
    def __init__(self, start, destination, map=None, path=None, modified=False):
        self.map = map
        self.current_position = start
        self.destination = destination 
        self.ts_on_current_position = 0
        self.total_times_for_car = 0
        self.path = path # list of nodes from start to destination
        self.next_to_visit = path[1]
        self.visited = False
        self.done = False
        self.modified = modified
    
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
                if can_move:
                    print("intersection to edge")
                    print("car id", self.map.car_map.index(self))
                    print(type(self.current_position), " ", self.current_position.id)
                    self.next_to_visit.add(self)
                    self.current_position.remove(self)
                    self.current_position = self.next_to_visit
                    print(type(self.current_position), " ", self.current_position.id)
                    try: 
                        temp = self.path.index(self.current_position) + 1 # index
                        print("road that is not in the list = ", self.current_position.id)
                        print("index of temp = ", temp)
                        self.next_to_visit = self.path[temp] # next in given list of path
                    except ValueError:
                        print(self.current_position.id)
                else: 
                    pass
            else: # if on edge(road) 
                can_move = self.try_move_from_edge() 
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
                else: 
                    pass 
        else: 
            self.ts_on_current_position += 1
        self.total_times_for_car += 1     
        self.visited = True    
        return False
            
    def try_move_from_node(self):
        self.find_shortest_path()
        return self.try_move_from_edge()
    
    def try_move_from_edge(self):
        return self.next_to_visit.q_size < self.next_to_visit.capacity

    def find_shortest_path(self): 
        # modified dijsktra
        if self.current_position != self.path[0]:
            self.current_position.reset_nodes()
            success, self.path = self.current_position.shortest_path(self.destination)
            #while not success: 
                #success, self.path = self.current_position.shortest_path(self.destination)