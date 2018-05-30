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
        
    nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=1000,savefile=True)
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
        nodes[str(edge.v)].add_edge(edge)
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
            st = nodes[node_key[np.random.randint(len(nodes))]]
        cars.append(Car(st,nodes[node_key[cars_v[i]]]))
    
    #- have map and cars ready on plot
    #vis.init_graph(nodes,edges,cars)
    
    #- calculate shortest path for each car
    for car in cars:
        paths = nv.dk(car.start.id,car.dest.id)
        #paths = car.start.shortest_path(car.dest)
        while type(paths) is bool:
            print('Re-routing')
            #- when pair of starts and destinations do not work, get new destination
            r_v = np.random.randint(len(nodes),size=2)
            car.start=nodes[node_key[r_v[0]]]
            car.dest = nodes[node_key[r_v[1]]]
            paths = nv.dk(car.start.id,car.dest.id)
        #- add paths to car object
        #path_id = [p.id for p in paths]
        #paths = nv._expand_path(path_id)
        car.set_path(paths[1:])
        
    while len(cars) > 0:
        for car in cars:
            if car.current_position.id == car.dest.id:
                cars.remove(car)
            else:
                m = car.move()
                if not m:
                    #- on hold
                    if type(car.paths[0]) is Road:
                        print(car.current_position,car.current_position.id,car.paths[0].id,edges[car.paths[0].id].capacity,edges[car.paths[0].id].q_size)
                    else:
                        print(car.current_position,car.current_position.id,car.paths[0].id,nodes[car.paths[0].id].cap,nodes[car.paths[0].id].q_size)
        vis.update(cars)
    plt.ion()
    plt.show()