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
        
    nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=350,savefile=False)
    #nodes, edges = util.retreiveMap(place=(37.7749, -122.4194),distance=1000,savefile=True)

    #- If files do not exist, un-comment the line above and comment 3 lines below
    
    #nodes, edges = util.retreiveMap(fromfile=True,filename=(nodes_file_path,edges_file_path))
    
    #- nodes and edges in dictionary form
    edge_id_distributor=0
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)

    #badnodes = ['418825595','53142970']
    #rm_list = ['531678155', '425811432', '33294637199', '428248112']


    del nodes['53221383']
    new_edges = {}
    for key,edge in edges.items():
        id = str(edge_id_distributor)
        edge_id_distributor+=1
        u = str(edge.u)
        v = str(edge.v)
        if u in nodes and v in nodes:
            #new_edges[id] = Road(id,nodes[u],nodes[v],edge.max_speed,edge.num_lanes,edge.length)
            new_edges[id] = Road(id,nodes[u],nodes[v],40,4,200)
            nodes[u].add_edge(new_edges[id])
            nodes[v].add_edge(new_edges[id])
            nodes[u].cap += 4
            nodes[v].cap += 4
    edges = new_edges
    
    

    node_key = list(nodes.keys())
    edge_key = list(edges.keys())
    
    #- initialize navigator
    nv.init(nodes,edges,node_key,edge_key)
    
    #-some pairs of start and end dont work, do not why
    

    
    car_size = c.NUMBER_CARS
    
    #- pick random starts and ends
    cars_u = np.random.randint(len(node_key),size=car_size)
    cars_v = np.random.randint(len(node_key),size=car_size)
    cars =[]
    for i in range(car_size):
        st = nodes[node_key[cars_u[i]]]
        end = nodes[node_key[cars_v[i]]]

        equal = True
        while equal:
            st = nodes[node_key[np.random.randint(len(nodes))]]
            #end = nodes[node_key[np.random.randint(len(nodes))]]
            while len(st.out_edges) == 0 or st.isFull():
                st = nodes[node_key[np.random.randint(len(nodes))]]
            while len(end.in_edges) == 0:
                end = nodes[node_key[np.random.randint(len(nodes))]]
            equal = st.id == end.id
            print(st.id,end.id,equal)
        cars.append(Car(st,end,modified=False))
        st.add()
    
    startid = '53160863'
    endid = '53114266'

    print(edges['38'].u.id,edges['38'].v.id)
    print(edges['19'].u.id,edges['19'].v.id)
    print(edges['18'].u.id,edges['18'].v.id)
    print(edges['17'].u.id,edges['17'].v.id)

    

    vis.drawPoint((nodes[startid].x,nodes[startid].y))
    vis.drawPoint((nodes[endid].x,nodes[endid].y))

    #- have map and cars ready on plot
    vis.init_graph(nodes,edges,cars)
    plt.show()
    quit()
    #- calculate shortest path for each car
    for car in cars:
        paths = nv.dk(car.start.id,car.dest.id,weight_on_length=1.0)
        #paths = car.start.shortest_path(car.dest)
        #while type(paths) is bool:
        #    print('Re-routing')
        #    #- when pair of starts and destinations do not work, get new destination
        #   r_v = np.random.randint(len(nodes),size=2)
        #    while r_v[0] == r_v[1]:
        #        r_v = np.random.randint(len(nodes),size=2)
        #    car.start=nodes[node_key[r_v[0]]]
        #    paths = nv.dk(car.start.id,car.dest.id)
        #    print(type(paths),car.start.id,car.dest.id)
        #- add paths to car object
        car.set_path(paths[1:])

    #vis.init_graph(nodes,edges,cars)

    counter=0
    total_time = 0
    while len(cars) > 0:
        for car in cars:
            if car.current_position.id == car.dest.id:
                counter+=1
                nodes[car.current_position.id].remove()
                print('{1},{0} to {3},{2}'.format(car.start.x,car.start.y,car.dest.x,car.dest.y),car.total_ts)
                cars.remove(car)
            else:
                total_time+=1
                car.total_ts+=1
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
                    print(str(car.current_position),str(car.dest))
                    if True:
                        new_path = nv.dk(str(car.current_position),str(car.dest),weight_on_length=1.0)
                        car.set_path(new_path[1:])
                        nxt_move = new_path[1].id
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
