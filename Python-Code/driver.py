import matplotlib.pyplot as plt
import constants as c
from car import Car
from intersection import Intersection as Node
from road import Road
import numpy as np
import utility as util
import navigate as nv
import visualizer as vis 

if __name__ == '__main__':
    '''Note
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !For now, ts on each road is set to be 10!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    
    #- CONSTANTS are in constants.py Feel free to change
    
    nodes_file_path = 'map/nodes.npy'
    edges_file_path = 'map/edges.npy'
        
    nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=400,savefile=True)
    #nodes, edges = util.retreiveMap(place=(37.7749, -122.4194),distance=1000,savefile=True)

    #- If files do not exist, un-comment the line above and comment 3 lines below
    
    #nodes, edges = util.retreiveMap(fromfile=True,filename=(nodes_file_path,edges_file_path))
    
    #- nodes and edges in dictionary form
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)
    
    #add edges to nodes
    for key, edge in edges.items():
        edge.u = nodes[str(edge.u)]
        edge.v = nodes[str(edge.v)]
        nodes[str(edge.u)].add_edge(edge)
        nodes[str(edge.u)].cap += edge.num_lanes
        #nodes[str(edge.v)].add_edge(edge)
        nodes[str(edge.v)].cap += edge.num_lanes
    #- get seperate list of ids
    node_key = list(nodes.keys())
    edge_key = list(edges.keys())
    
    #test_end = (nodes[node_key[339]].x,nodes[node_key[339]].y)
    
    #- initialize navigator
    nv.init(nodes,edges,node_key,edge_key)
    
    #-some pairs of start and end dont work, do not why
    

    
    car_size = c.NUMBER_CARS
    
    #- pick random starts and ends
    cars_u = np.random.randint(len(nodes),size=car_size)
    cars_v = np.random.randint(len(nodes),size=car_size)
    cars =[]
    for i in range(car_size):
        st = nodes[node_key[cars_u[i]]]
        while st.isFull():
            n = np.random.randint(len(nodes))
            while n == cars_v[i]:
                n = np.random.randint(len(nodes))
            st = nodes[node_key[n]]
        cars.append(Car(st,nodes[node_key[cars_v[i]]]))
        st.add()
    
    #- have map and cars ready on plot
    vis.init_graph(nodes,edges,cars)
    
    #- calculate shortest path for each car
    for car in cars:
        paths = nv.dk(car.start.id,car.dest.id)
        '''
        test_start = [car.start.x,car.start.y]
        test_end = [car.dest.x,car.dest.y]
        plt.plot(test_end[0],test_end[1],color='red',linestyle='none',marker='o',markersize=10)
        plt.plot(test_start[0],test_start[1],color='red',linestyle='none',marker='o',markersize=10)
        '''
        #paths = car.start.shortest_path(car.dest)
        while type(paths) is bool:
            print('Re-routing')
            #- when pair of starts and destinations do not work, get new destination
            r_v = np.random.randint(len(nodes),size=2)
            while r_v[0] == r_v[1]:
                r_v = np.random.randint(len(nodes),size=2)
            car.start=nodes[node_key[r_v[0]]]
            car.dest = nodes[node_key[r_v[1]]]
            paths = nv.dk(car.start.id,car.dest.id)
        #- add paths to car object
        #path_id = [p.id for p in paths]
        #paths = nv._expand_path(path_id)
        if len(paths) == 1:
            print('length is 1')
        car.set_path(paths[1:])
        for i in paths:
            print(str(i))
    
    counter=0
    while len(cars) > 0:
        for car in cars:
            if car.current_position.id == car.dest.id:
                counter+=1
                nodes[car.current_position.id].remove()
                cars.remove(car)
            else:
                nxt_move = str(car.paths[0].id)
                cur_pos = str(car.current_position.id)
                #print('car position', cur_pos, type(car.current_position))
                if type(car.current_position) == Road:
                    if car.ts_on_current_position < edges[cur_pos].time_steps:
                        car.ts_on_current_position += 1
                        continue
                else:
                    if car.ts_on_current_position < nodes[cur_pos].time_steps:
                        car.ts_on_current_position += 1
                        continue
                if nxt_move in edges:
                    """
                    #recalculate new path 
                    """
                    if not edges[nxt_move].add():
                        print('on hold edge',edges[nxt_move])
                        continue
                    car.current_position = edges[nxt_move]
                    nodes[cur_pos].remove()
                    car.ts_on_current_position = 0
                elif nxt_move in nodes:
                    if not nodes[nxt_move].add():
                        print('on hold node',nodes[nxt_move])
                        continue
                    car.current_position = nodes[nxt_move]
                    edges[cur_pos].remove()
                    car.ts_on_current_position = 0
                car.paths.pop(0)
        vis.update(cars)
    
    plt.ion()
    plt.show()
