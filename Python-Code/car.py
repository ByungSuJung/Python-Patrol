from road import Road as road
from intersection import Intersection as intersection 
	
class Car(object):
    def __init__(self, start, destination, map=None, path=None, modified=False, traffic_tolerance=0.75):
        self.TRAFFIC_TOLERANCE = traffic_tolerance

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
                    self.current_position.remove(self)
                    if not self.next_to_visit in self.path: 
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    print(type(self.current_position), " ", self.current_position.id)
                    print("HELPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                    if self.current_position in self.path: 
                        print("HELPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                        print("finished")
                    else: 
                        print("error in intersection to edge ~~~~~~~~~~~~~~~~~~~~~~~~~~~``")
                        print(self.current_position.id)
                        temp = self.path.index(self.current_position) + 1 # index
                        self.next_to_visit = self.path[temp] # next in given list of path
                    
                else: 
                    pass
            else: # if on edge(road) 
                can_move = self.try_move_from_edge() 
                if can_move: 
                    print("edge to intersection")
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
        if self.modified: 
            temp_value = self.next_to_visit.q_size / self.next_to_visit.capacity
            if temp_value > self.TRAFFIC_TOLERANCE:
                self.find_shortest_path()
            else: 
                pass
            
        return self.try_move_from_edge()
    
    def try_move_from_edge(self):
        return self.next_to_visit.q_size < self.next_to_visit.capacity

    def find_shortest_path(self): 
        # modified dijsktra
        if self.current_position != self.path[0]:
            self.current_position.reset_nodes()
            success, self.path = self.current_position.shortest_path(self.destination, modified=self.modified)
            #while not success: 
                #success, self.path = self.current_position.shortest_path(self.destination)