import matplotlib.pyplot as plt
import constants as c
from car import Car
from intersection import Intersection as Node
from road import Road
import numpy as np
import utility as util
import navigate as nv
import visualizer as vis
import copy

if __name__ == '__main__':
    '''Note
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !For now, ts on each road is set to be 10!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    
    #- CONSTANTS are in constants.py Feel free to change
    
    nodes_file_path = 'map/nodes.npy'
    edges_file_path = 'map/edges.npy'
    
    def one_simulation(lat = 47.608013, lon = -122.335167, distance = 500, num_cars = round(c.NUMBER_CARS/2), \
         num_modified = round(c.NUMBER_CARS/2), animated = False):
        avg_inv_time = 0 #Avg time for the cars 
        avg_inv_wait_time = 0 #Avg time in traffic for cars
        avg_inv_dist = 0 #Avg distace travelled by the cars
        sum_of_time = 0 #Total time for all of the cars

        nodes, edges = util.retreiveMap(place=(lat, lon),distance=distance,savefile=True)
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

        
        car_size = num_cars + num_modified #Number of cars to create
        norm_counter = 0#Keeps track of the number of normal cars. This makes  
                        #you know when to stop making norms and make modified
        
        #- pick random starts and ends
        cars_u = np.random.randint(len(node_key),size=car_size)
        cars_v = np.random.randint(len(node_key),size=car_size)
        cars =[]
        cars_copy = [] #Used for computaional purposes at the end of function

        for i in range(car_size):
            print(int((i+1)/car_size*100),'%')
            st = nodes[node_key[cars_u[i]]]
            end = nodes[node_key[cars_v[i]]]
            paths = nv.dk(st.id,end.id,weight_on_length=1.0) #Initial shortest path for the car
            while type(paths) is bool or len(paths) == 0 or st.isFull():
                #print('Re-routing')
                r_v = np.random.randint(len(nodes),size=2)
                while node_key[r_v[0]] == node_key[r_v[1]]:
                    r_v = np.random.randint(len(nodes),size=2)
                st = nodes[node_key[r_v[0]]]
                end = nodes[node_key[r_v[1]]]
                #print(str(st),str(end))
                paths = nv.dk(st.id,end.id,weight_on_length=1.0)

            car = None #Temp None so it's in scope
            if(norm_counter < num_cars):
                car = Car(st,end,modified=False)
                norm_counter += 1
            else:
                car = Car(st,end,modified=True)

            car.set_path(paths[1:])
            cars.append(car)
            st.add()

        # text=False to avoid edge id in plot
        vis.init_graph(nodes,edges,cars,text=False)

        cars_copy = cars[:] #Do this to create a deep copy since copy.deepcopy doesn't work
        total_time = 0
        compute=0
        skip=0
        f = open('arrival.txt','w')

        while len(cars) > 0:
            for car in cars:
                if car.current_position.id == car.dest.id:
                    nodes[car.current_position.id].remove()
                    statement = '{1},{0} to {3},{2} time {4}'.format(car.start.x,car.start.y,car.dest.x,car.dest.y,car.total_ts)
                    #print('{1},{0} to {3},{2}'.format(car.start.x,car.start.y,car.dest.x,car.dest.y),car.total_ts)
                    #print(statement)
                    #print(statement,file=f)
                    cars.remove(car)
                else:
                    total_time+=1
                    car.total_ts+=1
                    nxt_move = str(car.paths[0].id)
                    cur_pos = str(car.current_position.id)
                    #print('car position', cur_pos, type(car.current_position))
                    if type(car.current_position) == Road:
                        if car.ts_on_current_position < edges[cur_pos].time_steps:
                            car.ts_on_current_position += 1 #Keep track of total time driving
                            car.total_ts += 1
                            continue
                    else:
                        if car.ts_on_current_position < nodes[cur_pos].time_steps:
                            car.ts_on_current_position += 1
                            car.total_ts += 1 #Keep track of total time driving
                            continue
                    if nxt_move in edges:
                        #print(str(car.current_position),str(car.dest))
                        '''
                        Change True to modified
                        '''
                        if car.modified:
                            tmp_path = nv.dk(str(car.current_position),str(car.dest),weight_on_length=0.0)
                            if type(tmp_path) != bool:
                                new_path = tmp_path
                                car.set_path(new_path[1:])
                                nxt_move = new_path[1].id
                                compute+=1
                            else:
                                skip+=1
                            #print('re-calculated',compute,'skipped',skip)
                        if not edges[nxt_move].add():
                            #print('on hold edge',edges[nxt_move])
                            car.time_stopped += 1 #Keep track of time in traffic
                            car.total_ts += 1 #Keep track of total time driving
                            continue
                        car.current_position = edges[nxt_move]
                        nodes[cur_pos].remove()
                        car.ts_on_current_position = 0
                        car.total_dist += edges[nxt_move].length #Keep car distance travelled
                    elif nxt_move in nodes:
                        if not nodes[nxt_move].add():
                            #print('on hold node',nodes[nxt_move])
                            car.time_stopped += 1 #Keep track of time in traffic
                            car.total_ts += 1 #Keep track of total time driving
                            continue
                        car.current_position = nodes[nxt_move]
                        edges[cur_pos].remove()
                        car.ts_on_current_position = 0
                    car.paths.pop(0)

            if(animated):
                vis.update(cars)
        f.close()

        if(animated):
            plt.ion()
            plt.show()

        #Get the results
        for car in cars_copy:
            avg_inv_time += car.total_ts
            avg_inv_wait_time += car.time_stopped
            avg_inv_dist += car.total_dist
            sum_of_time += car.total_ts

        return (avg_inv_time/len(cars_copy), avg_inv_wait_time/len(cars_copy), \
            avg_inv_dist/len(cars_copy), sum_of_time)


def normal_vs_modified(iterations = 1, cars = c.NUMBER_CARS):

    #Each row is a different field while each column is
    #a different iteration
    comp_norm = np.zeros((4, 20))
    comp_mod = np.zeros((4, 20))
    num_cars = np.arange(1, 21) * 50#Segments of cars

    for car_count in range(len(num_cars)):
        print("Car Count: ", num_cars[car_count])
        #Each row is a different field while each column is
        #a different iteration
        norm_time = np.zeros((4, iterations))
        mod_time = np.zeros((4, iterations))

        #For each iteration run the simulation one with only normal
        #and the other with modified calculations
        for it in range(iterations):
            print("Running Iteration: " + str(it+1) + "/" + str(iterations))

            print("Simulating Normal Dijkstra")
            #Extract all the proper information for the results
            norm_results = one_simulation(num_cars = cars, num_modified = 0) #Do a normal run
            norm_time[0, it] = norm_results[0]
            norm_time[1, it] = norm_results[1]
            norm_time[2, it] = norm_results[2]
            norm_time[3, it] = norm_results[3]

            print("Simulating Modified Dijkstra")
            modi_results = one_simulation(num_cars = 0, num_modified = cars)
            mod_time[0, it] = modi_results[0]
            mod_time[1, it] = modi_results[1]
            mod_time[2, it] = modi_results[2]
            mod_time[3, it] = modi_results[3]

        '''print("----------Normal Dijkstra's Results----------")
        print("Avg. Individual Time: ", np.average(norm_time[0, :]))
        print("Avg. Individual Wait Time: ", np.average(norm_time[1, :]))
        print("Avg. Individual Distance Travelled: ", np.average(norm_time[2, :]))
        print("Avg. Sum of All Time: ", np.average(norm_time[3, :]))
        print("---------------------------------------------\n")

        print("----------Modified Dijkstra's Results----------")
        print("Avg. Individual Time: ", np.average(mod_time[0, :]))
        print("Avg. Individual Wait Time: ", np.average(mod_time[1, :]))
        print("Avg. Individual Distance Travelled: ", np.average(mod_time[2, :]))
        print("Avg. Sum of All Time: ", np.average(mod_time[3, :]))
        print("-----------------------------------------------\n\n")'''

        #Place the the values into the correct array section of the overall results
        comp_norm[0, car_count] = np.average(norm_time[0, :])
        comp_norm[1, car_count] = np.average(norm_time[1, :])
        comp_norm[2, car_count] = np.average(norm_time[2, :])
        comp_norm[3, car_count] = np.average(norm_time[3, :])

        comp_mod[0, car_count] = np.average(mod_time[0, :])
        comp_mod[1, car_count] = np.average(mod_time[1, :])
        comp_mod[2, car_count] = np.average(mod_time[2, :])
        comp_mod[3, car_count] = np.average(mod_time[3, :])

    #-----------------------Graph normal vs modified------------------------#
    plt.clf()
    plt.plot(num_cars, comp_norm[0], '-', num_cars, comp_mod[0], '--')
    plt.title("Normal Dijkstra's vs Modified Dijkstra's")
    plt.xlabel("Number of Cars")
    plt.ylabel("Average Individual Time")
    plt.show()

    plt.plot(num_cars, comp_norm[1], '-', num_cars, comp_mod[1], '--')
    plt.title("Normal Dijkstra's vs Modified Dijkstra's")
    plt.xlabel("Number of Cars")
    plt.ylabel("Average Individual Wait Time")
    plt.show()

    plt.plot(num_cars, comp_norm[2], '-', num_cars, comp_mod[2], '--')
    plt.title("Normal Dijkstra's vs Modified Dijkstra's")
    plt.xlabel("Number of Cars")
    plt.ylabel("Average Individual Distance Travelled")
    plt.show()

    plt.plot(num_cars, comp_norm[3], '-', num_cars, comp_mod[3], '--')
    plt.title("Normal Dijkstra's vs Modified Dijkstra's")
    plt.xlabel("Number of Cars")
    plt.ylabel("Average Sum of Time")
    plt.show()
    #-----------------------------------------------------------------------#

normal_vs_modified()
#----------------------------Test that the graphing is working properly-----------------------------#
'''results = one_simulation(distance=500, num_cars = 500, num_modified = 500, animated = True)

print("Avg. Individual Time: ", results[0])
print("Avg. Individual Wait Time: ", results[1])
print("Avg. Individual Distance Travelled: ", results[2])
print("Sum of Time: ", results[3])'''
#---------------------------------------------------------------------------------------------------#