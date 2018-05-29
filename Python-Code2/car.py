from road import Road as edge
from node import Node as node 

class Car(object):
    def __init__(self, start, destination, path=None):
        self.current_position = start
        self.destination = destination 
        self.next_to_visit
        self.ts_on_current_position = 0
        self.total_times_for_car = 0
        # self.queue or list_path to update for normal_move
        self.path = path  
    
    # move for normal disjktra, require list of shortest path node and edges
    def normal_move(self):
        if self.ts_on_current_position == self.current_position.time_steps: 
            can_move = self.try_move()
            if can_move:
                self.current_position.remove()
                self.next_to_visit.add(self)
                self.current_position = self.next_to_visit
                #self.next_to_visit = # next from given list of path
            else: 
                pass
        else: 
            self.ts_on_current_position += 1
        self.total_times_for_car += 1        
                    

    def modified_move(self): 
        if self.ts_on_current_position == self.current_position.time_steps: 
            if type(current_position) is Node:
                can_move = self.try_move_from_node()
                if can_move: 
                    self.current_position.remove()
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    #self.next_to_visit = # now on edge so next node 
                else: 
                    pass
            else: #on edge
                can_move = self.try_move_from_edge()
                if can_move:
                    self.current_position.queue.remove()
                    self.next_to_visit.add(self)
                    self.current_position = self.next_to_visit
                    #self.next_to_visit = # now on node so next edge
                else: 
                    pass
                    # change all the car in edge.queue become False 
                    # should I do this just going through all the cars
                    # in the queue? pop pushback pop pushback ?   
        else: 
            self.ts_on_obj += 1 
        self.total_times_for_car += 1
             
    def try_move(self): 
        return self.next_to_visit.q_size < self.next_to_visit.capacity

    def try_move_from_node(self):
        self.next_to_visit = self.find_shortest_path()
        return self.try_move()
    
    # This is same as self.try_move() I just made one for readability 
    # and for possible later modification. 
    def try_move_from_edge(self): 
        return self.try_move()

    def find_shortest_path(self): 
        # modified dijsktra
        
        return next_edge 

if __name__ == '__main__': 
    myCar = Car() 
