import matplotlib.pyplot as plt
import constants as c
from car import Car
from intersection import Intersection as Node
from road import Road
import numpy as np
import utility as util
import navigate as nv
import visualizer as vis 
from joblib import Parallel, delayed
import time, threading, sys
from multiprocessing import Queue

#---------------------------User Adjustable-------------------------------------------------------#
size=[500,1000,10000,100000] #- put # of cars here. NOTE: actual car size might be smaller than values here
weights_ratio = [0.0,1.0]
place_coord = (47.608013, -122.335167) #- logitude and altitude
map_size = 1500 #- size of the map
CORES=-1 #- cores=-1 to use all cores, -2 to use all cores except first core, 1 is single process\
            # parallel does not provide performance boost on smaller car clusters
visual=True #- set visual to False if need results only
console_output=False #- Useful when details are needed
#--------------------------User Adjustable END-----------------------------------------------------#

nodes = None
edges = None
node_key = None
edge_key = None
WEIGHT=0.0
dk_arg_q = Queue()
q_size = 0
cars_data = None
last_size = 0

def __initialize_car(st,end):
    '''Designed for parallel computation for initializing car agents, don't call it directly
    
    Args:
        st: start id, str
        end: end id, str
    Returns:
        str, str, tuple.
        Verified start point, end point and one calculated path
    '''
    #- get working starting point and destinations
    paths = nv.dk(st,end,weight_on_length=WEIGHT,parallel=True)
    while type(paths) is bool or len(paths) <=1 or nodes[str(st)].isFull():
        r_v = np.random.randint(len(nodes),size=2)
        while node_key[r_v[0]] == node_key[r_v[1]]:
            r_v = np.random.randint(len(nodes),size=2)
        st = nodes[node_key[r_v[0]]]
        end = nodes[node_key[r_v[1]]]
        paths = nv.dk(str(st),str(end),weight_on_length=WEIGHT,parallel=True)
    return str(st),str(end),paths

def __dk_parallel():
    '''Designed for parallel computation for car agents, don't directly call it
    
    Args:
        None
    Returns:
        tuple, integer. Tuple of paths if exists, else return None. Integer is the indice in cars
    '''
    #- get parameters for the process from queue
    current_position,dest,i = dk_arg_q.get()
    #- calculate path using parameters
    tmp_path = nv.dk(current_position,dest,weight_on_length=WEIGHT,parallel=True)
    if type(tmp_path) != bool:
        nxt_move=tmp_path[1]
        if not edges[nxt_move].add():return None,i
        return tmp_path,i #- tuple, indice
    else:
        raise RuntimeWarning('Can not find path for car object # {0}'.format(i))

def start_simulation(car_size=c.NUMBER_CARS,error_count=0,filename=None,std_out=True):
    '''start simulation
    
    Args:
        car_size: int, Number of cars in this simulation. Actual cars might be less than the value
        filename: str, File/path name for log output
        std_out: bool, Print out to console or not
    Returns:
        int, total time steps take for this set of cars to finish
    '''
    global nodes, edges,cars_data, last_size
    print('-------------------start new simulation-----------------------')
    print('Weight ratio is',WEIGHT)
    f = None
    global_time_ts = 0

    cars=[]

    ts = time.time()

    if cars_data is None or last_size!=car_size:
        print('initializing cars...')
        last_size = car_size
        cars_u = np.random.randint(len(node_key),size=car_size)
        cars_v = np.random.randint(len(node_key),size=car_size)
        cars_data = Parallel(n_jobs=CORES)(delayed(__initialize_car)\
            (str(nodes[node_key[cars_u[i]]]),str(nodes[node_key[cars_v[i]]])) for i in range(car_size))
    for i in range(len(cars_data)):
        st = cars_data[i][0]
        ed = cars_data[i][1]
        path = cars_data[i][2]
        if nodes[st].add():
            car = Car(nodes[st],nodes[ed])
            car.set_path(list(path)[1:])
            car.id=i
            cars.append(car)

    te = time.time()

    print('# of cars',len(cars),'time takes',te-ts)
    #-initialize plot if visual
    if visual: vis.init_graph(nodes,edges,cars,text=False)
    #- initialize file if filename is provided
    if filename is not None:f=open(filename,'a')

    #- while cars left in car pool
    while len(cars) > error_count:
        #- reset queue size counter
        q_size=0
        global_time_ts += 1

        car_indeces_re_rout = []
        rm_list = []

        #- iterate through cars
        for i in range(len(cars)):
            if cars[i].current_position.id == cars[i].dest.id:
                #- car has arrived!
                nodes[cars[i].dest.id].remove()
                statement = '{6} || {1},{0} to {3},{2} time {4} {5}'.format(cars[i].start.x,cars[i].start.y,cars[i].dest.x,cars[i].dest.y,cars[i].total_ts,cars[i].id,time.ctime())
                if std_out or visual:print(statement,'| cars left -',len(cars)-error_count)

                if f is not None:print(statement,file=f)

                rm_list.append(cars[i].id)
                continue
            else:
                #- car is on the way
                cars[i].total_ts+=1
                nxt_move = str(cars[i].paths[0])
                cur_pos = str(cars[i].current_position)

                if type(cars[i].current_position) == Road:
                    if cars[i].ts_on_current_position < edges[cur_pos].time_steps:
                        #- car is waiting on the edge
                        cars[i].ts_on_current_position += 1
                        continue
                else:
                    if cars[i].ts_on_current_position < nodes[cur_pos].time_steps:
                        #- car is waiting on the node
                        cars[i].ts_on_current_position += 1
                        continue

                if nxt_move in edges:
                    #- compute next optimized route
                    car_indeces_re_rout.append(i)
                    dk_arg_q.put((str(cars[i].current_position),str(cars[i].dest),i))
                    q_size+=1

                elif nxt_move in nodes:
                    #- keep moving from edge to node, no computation required
                    if nodes[nxt_move].add():
                        cars[i].current_position = nodes[nxt_move]
                        edges[cur_pos].remove()
                        cars[i].ts_on_current_position = 0
                        cars[i].paths.pop(0)
                    else:
                        if visual:print('on hold node',nodes[nxt_move])
        #- if at least one car needs to calculate routes
        if len(car_indeces_re_rout) > 0 :
            #- run algrithm in parallels
            results = Parallel(n_jobs=CORES)(delayed(__dk_parallel)() for i in range(q_size))
            #- apply results to agents
            for i in range(len(results)):
                path,indice = results[i]
                if path is not None:
                    cur_pos=str(cars[indice].current_position)
                    cars[indice].set_path(list(path)[1:])
                    nxt_move = cars[indice].paths[0]
                    if edges[nxt_move].add():
                        nodes[cur_pos].remove()
                        cars[indice].current_position = edges[nxt_move]
                        cars[indice].ts_on_current_position=0
                        cars[indice].paths.pop(0)

        car_index_list = [c.id for c in cars]
        rm_list.sort(reverse=True)
        #- remove arrived cars
        for r in rm_list:cars.pop(car_index_list.index(r))
        #- update graph
        if visual:vis.update(cars)

    te=time.time()
    print('This simulation takes {0}'.format(te-ts))

    if f is not None:f.close()
    print('-------------------Simulation ends here-----------------------')
    return global_time_ts

if __name__ == '__main__':
    #- program starts here

    nodes_file_path = 'map/nodes.npy'
    edges_file_path = 'map/edges.npy'
    
    #- Read nodes from existing data or from map
    nodes, edges = util.retreiveMap(place=place_coord,distance=map_size,savefile=True)

    '''
    If files do not exist, un-comment the line above and comment 3 lines below
    '''

    #nodes, edges = util.retreiveMap(fromfile=True,filename=(nodes_file_path,edges_file_path))
    edge_id_distributor=0
    car_id_distributor=0
    
    #- nodes and edges in dictionary form
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)

    del nodes['53221383']

    #- add edge into its parent nodes, also reset edges' ids
    new_edges = {}
    for key,edge in edges.items():
        id = str(edge_id_distributor)
        edge_id_distributor+=1
        u = str(edge.u)
        v = str(edge.v)
        if u in nodes and v in nodes:
            new_edges[id] = Road(id,nodes[u],nodes[v],edge.max_speed,edge.num_lanes,edge.length)
            nodes[u].add_edge(new_edges[id])
            nodes[v].add_edge(new_edges[id])
            nodes[u].cap += new_edges[id].num_lanes
            nodes[v].cap += new_edges[id].num_lanes
    edges = new_edges

    node_key = list(nodes.keys())
    edge_key = list(edges.keys())
    
    #- initialize navigator
    nv.init(nodes,edges,node_key,edge_key)

    if visual:
        total_time, d = start_simulation(error_count=0,std_out=True,car_size=size[0],filename='log.txt')
        plt.ion()
        plt.show()
        quit()
    
    for s in size:
        WEIGHT = weights_ratio[0]
        weights_ratio.pop(0)
        results = []
        results.append(tot_ts1)
        for w in weights_ratio:
            WEIGHT = w
            t = start_simulation(error_count=10,std_out=console_output,car_size=s,filename='log.txt')
            results.append(t)
        printout = str(len(cars_data))
        for r in results:
            printout += ' '
            printout += str(r)
        with open ('results.txt','a') as f:
            f.write(printout)
        print(printout)
#- ------------------EOF----------------------