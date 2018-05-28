from road import Road as road
from intersection import Intersection as intersection 
	
class Car(object):
    def __init__(self, start, destination, path=None):
        self.current_position = start
        self.destination = destination 
        self.next_to_visit = path[0]
        self.ts_on_current_position = 0
        self.total_times_for_car = 0
        self.path = path # list of nodes from start to destination
        self.visited = False
    
    def update(self): 
        if self.visited: 
            pass
        else: 
            self.current_position.run()

    # move for normal and modified dijkstra 
    def move(self):
        if self.ts_on_current_position == self.current_position.time_steps: 
            if type(self.current_position) is intersection: 
                can_move = self.try_move_from_node()
                if can_move:
                    self.current_position.remove()
                    self.next_to_visit.add(self)
                    temp = self.path.index(self.current_position) + 1
                    self.current_position = self.next_to_visit
                    self.next_to_visit = self.path[temp] # next in given list of path
                else: 
                    pass
            else: # if on edge(road) 
                can_move = self.try_move_from_edge() 
                if can_move: 
                    self.current_position.remove()
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    temp = self.path.index(self.current_position) + 1
                    for edge in self.current_position.edge_list: 
                        if edge.destination == self.path[temp]: 
                            self.next_to_visit = self.path[temp]
                else: 
                    pass 
        else: 
            self.ts_on_current_position += 1
        self.total_times_for_car += 1     
        self.visited = True    
                    
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
        self.find_shortest_path()
        return self.try_move_from_edge()
    
    # This is same as self.try_move() I just made one for readability 
    # and for possible later modification. 
    def try_move_from_edge(self): 
        return self.next_to_visit.qsize < self.next_to_visit.capacity

    def find_shortest_path(self): 
        # modified dijsktra
        self.path = self.current_position.find_shortest_path(self.destination)
        

if __name__ == '__main__': 
    myCar = Car() 