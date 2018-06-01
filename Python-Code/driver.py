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
import time, threading


nodes = None
edges = None
node_key = None
edge_key = None
CORES=8 #- cores=-1 to use all cores, -2 to use all cores except first core
visual=False

def initialize_car(st,end,weight=1.0):
    #- get working starting point and destinations
    paths = nv.dk(st,end,weight_on_length=weight,parallel=True)
    while type(paths) is bool or len(paths) <=1 or nodes[str(st)].isFull():
        r_v = np.random.randint(len(nodes),size=2)
        while node_key[r_v[0]] == node_key[r_v[1]]:
            r_v = np.random.randint(len(nodes),size=2)
        st = nodes[node_key[r_v[0]]]
        end = nodes[node_key[r_v[1]]]
        paths = nv.dk(str(st),str(end),weight_on_length=weight,parallel=True)
    return str(st),str(end),paths

def dk_parallel(nxt_move,current_position,dest,weight=1.0):
    if nxt_move in edges:
        tmp_path = nv.dk(current_position,dest,weight_on_length=weight,parallel=True)
        if type(tmp_path) != bool:
            nxt_move=tmp_path[1]
            if not edges[nxt_move].add():return None

            return tmp_path #- tuple

def start_simulation(cars_data=None,conti=False,car_size=c.NUMBER_CARS,error_count=0,filename=None,weight=1.0,std_out=True):
    global nodes, edges
    print('-------------------start new simulation-----------------------')
    f = None
    global_time_ts = 0

    cars=[]
    ts = time.time()
    if cars_data is None:
        print('initializing cars...')
        cars_u = np.random.randint(len(node_key),size=car_size)
        cars_v = np.random.randint(len(node_key),size=car_size)
        cars_data = Parallel(n_jobs=CORES)(delayed(initialize_car)\
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

    if filename is not None:f=open(filename,'w')

    def operate_data(path,indice):
        if path is not None:
            cur_pos=str(cars[indice].current_position)
            cars[indice].set_path(list(path)[1:])
            nxt_move = cars[indice].paths[0]
            if edges[nxt_move].add():
                nodes[cur_pos].remove()
                cars[indice].current_position = edges[nxt_move]
                cars[indice].ts_on_current_position=0
                cars[indice].paths.pop(0)

    while len(cars) > error_count:
        global_time_ts += 1
        car_indeces_re_rout = []
        rm_list = []
        for i in range(len(cars)):
            try:
                arrived = cars[i].current_position.id == cars[i].dest.id
            except IndexError:
                print(i,len(cars),'IndexError')
            if arrived:
                nodes[cars[i].dest.id].remove()
                statement = '{1},{0} to {3},{2} time {4} {5}'.format(cars[i].start.x,cars[i].start.y,cars[i].dest.x,cars[i].dest.y,cars[i].total_ts,cars[i].id)
                if std_out:print(statement,len(cars))

                if f is not None:print(statement,file=f)

                rm_list.append(cars[i].id)
                continue
            else:
                cars[i].total_ts+=1
                nxt_move = str(cars[i].paths[0])
                cur_pos = str(cars[i].current_position)
                if type(cars[i].current_position) == Road:
                    if cars[i].ts_on_current_position < edges[cur_pos].time_steps:
                        cars[i].ts_on_current_position += 1
                        continue
                else:
                    if cars[i].ts_on_current_position < nodes[cur_pos].time_steps:
                        cars[i].ts_on_current_position += 1
                        continue

                if nxt_move in edges:
                    #- run algrithm in parallel
                    car_indeces_re_rout.append(i)
                elif nxt_move in nodes:
                    if nodes[nxt_move].add():
                        cars[i].current_position = nodes[nxt_move]
                        edges[cur_pos].remove()
                        cars[i].ts_on_current_position = 0
                        cars[i].paths.pop(0)
                    #else:
                        #print('on hold node',nodes[nxt_move])

        pl_job = len(car_indeces_re_rout)
        if pl_job > 0 :
            results = Parallel(n_jobs=CORES)(delayed(dk_parallel)\
                (str(cars[i].paths[0]),str(cars[i].current_position),str(cars[i].dest),weight) for i in car_indeces_re_rout)
            #- do threading to operate data
            jobs = []
            for i in range(len(results)):
                path = results[i]
                indice = car_indeces_re_rout[i]
                tmp_thread = threading.Thread(target=operate_data(path,indice))
                jobs.append(tmp_thread)
                tmp_thread.start()
                #if path is not None:
                #    cur_pos=str(cars[indice].current_position)
                #    cars[indice].set_path(list(path)[1:])
                #    nxt_move = cars[indice].paths[0]
                #    if edges[nxt_move].add():
                #        nodes[cur_pos].remove()
                #        cars[indice].current_position = edges[nxt_move]
                #        cars[indice].ts_on_current_position=0
                #       cars[indice].paths.pop(0)
            for j in jobs:
                j.join()

        car_index_list = [c.id for c in cars]
        rm_list.sort(reverse=True)

        for r in rm_list:cars.pop(car_index_list.index(r))

        #- update graph
        if visual:vis.update(cars)
    te=time.time()
    print('This simulation takes {0}'.format(te-ts))
    if f is not None:f.close()
    print('-------------------Simulation ends here-----------------------')
    return global_time_ts, cars_data


    

if __name__ == '__main__':
    '''Note
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !For now, ts on each road is set to be 10!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    
    nodes_file_path = 'map/nodes.npy'
    edges_file_path = 'map/edges.npy'
    
    nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=1500,savefile=True)

    #- If files do not exist, un-comment the line above and comment 3 lines below
    
    #nodes, edges = util.retreiveMap(fromfile=True,filename=(nodes_file_path,edges_file_path))
    
    #- nodes and edges in dictionary form
    edge_id_distributor=0
    car_id_distributor=0
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)

    del nodes['53221383']
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
            nodes[u].cap += 4
            nodes[v].cap += 4
    edges = new_edges

    node_key = list(nodes.keys())
    edge_key = list(edges.keys())
    
    #- initialize navigator
    nv.init(nodes,edges,node_key,edge_key)
    if visual:
        vis.init_graph(nodes,edges,cars,text=False)
    
    #def start_simulation(cars_data=None,conti=False,car_size=c.NUMBER_CARS,error_count=0,visual=False,filename=None)
    size=[500,2000,4000,8000,16000,40000]
    for s in size:
        w = 0.0
        results = []
        tot_ts1, cars_data = start_simulation(error_count=10,std_out=False,weight=w,car_size=size)
        results.append(tot_ts1)
        while w <= 1.0:
            t,d = start_simulation(error_count=10,cars_data=cars_data,weight=w,std_out=False,car_size=size)
            results.append(t)
            w += 0.1
        printout = str(len(cars_data))
        for r in results:
            printout += ' '
            printout += str(r)
        with open ('log.txt','a') as f:
            f.write(printout)
        print(printout)

    quit()