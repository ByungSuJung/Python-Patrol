from map import Map 
import matplotlib
import matplotlib.pyplot as plt
import constants as c
import numpy as np
from intersection import Intersection
from car import Car

#Varying Map Parameters:
CENTER_LATITUDE = 47.608013
CENTER_LONGITUDE = -122.335167
DISTANCE_FROM_CENTER = 500
NUM_CARS = 1000
RANDOM_START_DESTINATION = True
TRAFFIC_TOLERANCE = 0.75 
MODIFIED = False


#Varying Driver parameters
VISUALIZATION = False
SINGLE_ SIM = True

car_data = None
fig, ax = plt.subplots()

def drawCars(cars,draw=True):
    '''Plot nodes and edges
    Args:
        cars: list, list of all cars
        draw: bool, draw is only set to be True the first time. \
                While cars are updating, draw should always be False
    Return:
        list of line object, only used for updating graph
    '''
    global car_data
    car_list = np.zeros((len(cars),2))
    it = 0
    for icar in cars:
        cur_p = icar.current_position
        if type(cur_p) is Intersection:
            #-car is on node, using node coordinates
            car_list[it,0] = cur_p.x
            car_list[it,1] = cur_p.y
        else:
            #- car is on edge, calculates coordinates
            portion = icar.ts_on_current_position / icar.current_position.time_steps #cur_steps
            
            car_list[it,0] = cur_p.u.x + (cur_p.v.x - cur_p.u.x) * portion
            car_list[it,1] = cur_p.u.y + (cur_p.v.y - cur_p.u.y) * portion
            
        it += 1
    if draw:
        car_data, = ax.plot(car_list[:,0],car_list[:,1],linestyle='none',\
            marker=c.CAR_PLOT_SHAPE,markersize=c.CAR_PLOT_SIZE,color='red')
    else:
        return car_list

def update(cars):
    '''Updates graph
    '''
    global car_data
    car_list = drawCars(cars,draw=False)

    car_data.set_xdata(car_list[:,0])
    car_data.set_ydata(car_list[:,1])
    plt.draw()
    if len(cars) < 100:
        plt.pause(c.ANIMATION_SEG)
 

def _init_graph(nodes,edges,cars,text=False):
    '''Initialize graph with nodes, edgew and cars
    '''
    drawMap(nodes,edges)
    drawCars(cars)


def drawMap(nodes,edges):
    if type(nodes) is dict:
        for key, node in nodes.items():
            ax.plot(node.x,node.y,linestyle='none',\
                marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
        for key, edge in edges.items():
            if type(edge.u) is int:
                u = nodes[str(edge.u)]
                v = nodes[str(edge.v)]
                ax.plot([u.x,v.x],[u.y,v.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
            else:
                ax.plot([edge.u.x,edge.v.x],[edge.u.y,edge.v.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
    else:
        nl = np.array([i.id for i in nodes])
        for inode in nodes:
            #draw node
            ax.plot(inode.x,inode.y,linestyle='none',\
                    marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
        for iedge in edges:
            #draw edges
            if type(iedge.u) == int:
                i = nodes[np.where(nl==str(iedge.u))[0][0]]
                j = nodes[np.where(nl==str(iedge.v))[0][0]]
                #print('plot',iedge.id,i.id,i.x,i.y,j.id,j.x,j.y)
                ax.plot([i.x,j.x],[i.y,j.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
            else:
                ax.plot([iedge.u.x,iedge.v.x],[iedge.u.y,iedge.v.y],\
                    linestyle='-',color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)

def updateStatus(map):
    individual_travel_time = []
    for car in map.car_map:
        car.update()
        if car.done:
            individual_travel_time.append(car.total_times_for_car)
            #print("car's trip history--------------------------------------")
            #print(car.path)
            map.car_map.remove(car)
            del car
    return individual_travel_time

def run_simulation(map, visualization=False): 
    if visualization:
        _init_graph(map.node_map, map.edge_map, map.car_map)
    individual_travel_time = []
    total_time = 0
    while len(map.car_map) > 0:
        temp = updateStatus(map)
        individual_travel_time += temp
        for car in map.car_map:
            if car.done:
                pass
            else:
                car.visited = False
        total_time += 1
        if visualization:
            update(map.car_map)
            plt.ion()
            #plt.show()
    #print("time", total_time)
    return total_time, individual_travel_time

def multi_simulations(maps, visualization=False) : 
    total_time_list = []
    avg_individual_time = []
    for m in maps:
        total_time, individual_travel_time = run_simulation(m, \
        visualization=visualization)
        
        total_time_list.append(total_time)
        individual_travel_time = np.array(individual_travel_time)

        avg_individual_time.append(np.mean(individual_travel_time))
    return total_time_list, avg_individual_time
        

#single simulation plotting (int) total_time_steps (list) individual_travel_time
if SINGLE:
    single_map=Map(center_lat=CENTER_LATITUDE,center_long=CENTER_LONGITUDE,\
    dist=DISTANCE_FROM_CENTER,num_cars=NUM_CARS,random_init=RANDOM_START_DESTINATION,\
    modified=MODIFIED,traffic_tolerance=TRAFFIC_TOLERANCE)
    t_time, i_travel_time = run_simulation(single_map ,visualization=VISUALIZATION)

"""
-------------------Start of Analysis-------------------------------------
"""
def analysis():
    non_mod_maps = []
    mod_maps = []

    #x = None
    #Varying num cars
    car_numbers_to_test = np.arange(100,1001,100) #100, 200, 300..1000
    #car_numbers_to_test = np.arange(100,201,50) #100,150, 200

    for i in car_numbers_to_test:
        print(i)
        non_mod_maps.append(Map(num_cars=i))
        mod_maps.append(Map(num_cars=i, modified=True))

    #print(len(non_mod_maps))
    #print(len(car_numbers_to_test))
    total_time, avg_ind_time = multi_simulations(non_mod_maps)
    m_total_time, m_avg_ind_time = multi_simulations(mod_maps)

    print("now displaying graph 1")
    plt.title("Non-mod vs mod: total-time")
    plt.figure(1)
    plt.plot(car_numbers_to_test, total_time, "-o")
    plt.plot(car_numbers_to_test, m_total_time, "-o")
    plt.xlabel("number of cars")
    plt.ylabel("total-time")

    print("now displaying graph 2")
    plt.title("Non-mod vs mod: avg ind time")
    plt.figure(2)
    plt.plot(car_numbers_to_test, avg_ind_time, "-o")
    plt.plot(car_numbers_to_test, m_avg_ind_time, "-o")
    plt.xlabel("number of cars")
    plt.ylabel("avg in time")
    
    
    non_mod_maps = []
    mod_maps = []
    #Varying num cars
    radii_to_test = np.arange(200,1001,100) #200, 300, 400..1000
    #radii_to_test = np.arange(200,1001,100) #200, 300, 400..1000

    for i in car_numbers_to_test:
        print(i)
        non_mod_maps.append(Map(dist=i))
        mod_maps.append(Map(dist=i, modified=True))

    #print(len(non_mod_maps))
    #print(len(car_numbers_to_test))
    total_time, avg_ind_time = multi_simulations(non_mod_maps)
    m_total_time, m_avg_ind_time = multi_simulations(mod_maps)

    print("now displaying figure 3")
    plt.title("Non-mod vs mod: total-time")
    plt.figure(3)
    plt.plot(radii_to_test, total_time, "-o")
    plt.plot(radii_to_test , m_total_time, "-o")
    plt.xlabel("map radius")
    plt.ylabel("average total time")

    print("now displaying figure 4")
    plt.title("Non-mod vs mod: avg ind-time")
    plt.figure(4)
    plt.plot(radii_to_test, avg_ind_time, "-o")
    plt.plot(radii_to_test , m_avg_ind_time, "-o")
    plt.xlabel("map radius")
    plt.ylabel("average ind time")

    non_mod_maps = []
    mod_maps = []
    #Varying num cars
    caps_to_test = np.arange(0.1,1.1,0.1) #0.1, 0.2, 0.3...1
    caps_to_test = np.arange(0.1,1.1,0.5) #0.1, 0.2, 0.3...1

    for i in car_numbers_to_test:
        print(i)
        non_mod_maps.append(Map(traffic_tolerance=i))
        mod_maps.append(Map(traffic_tolerance=i, modified=True))

    #print(len(non_mod_maps))
    #print(len(car_numbers_to_test))
    total_time, avg_ind_time = multi_simulations(non_mod_maps)
    m_total_time, m_avg_ind_time = multi_simulations(mod_maps)

    print("now displaying figure 5")
    plt.title("Non-mod vs mod: total-time")
    plt.figure(5)
    plt.plot(caps_to_test, total_time, "-o")
    plt.plot(caps_to_test , m_total_time, "-o")
    plt.xlabel("traffic tolerance")
    plt.ylabel("total-time")

    print("now displaying figure 6")
    plt.title("Non-mod vs mod: avg ind time")
    plt.figure(6)
    plt.plot(caps_to_test, avg_ind_time, "-o")
    plt.plot(caps_to_test , m_avg_ind_time, "-o")
    plt.xlabel("traffic tolerance")
    plt.ylabel("avg ind-time")
    
    plt.show()
if not VISUALIZATION:
    analysis()


    
