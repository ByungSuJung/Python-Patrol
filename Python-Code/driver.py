from map import Map 
import matplotlib
#import visualize 
import matplotlib.pyplot as plt
import constants as c
import numpy as np
from intersection import Intersection
from car import Car
#import visualize

# CONSTANTS 
CENTER_LATITUDE = 47.608013
CENTER_LONGITUDE = -122.335167
DISTANCE_FROM_CENTER = 500
NUM_CARS = 1000
VISUALIZATION = False
RANDOM_START_DESTINATION = True
NUM_SIMULATION = 10
TRAFFIC_TOLERANCE = 0.75  
car_data = None

fig, ax = plt.subplots()
"""
def drawMap(nodes,edges,text=False):
    '''Plot nodes and edges
    Args:
        nodes: dict, dictionary of all nodes
        edges: dict, dictionary of all edges
        text: bool, if display edge id on map
    '''
    #- plot each node in dictionary using their coordinates
    for key, node in nodes.items():
        ax.plot(node.x,node.y,linestyle='none',\
            marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
    #- plot each edge in dictionary using their parents' coordinates
    for key, edge in edges.items():
        u = nodes[str(edge.u)]
        v = nodes[str(edge.v)]
        ax.plot([u.x,v.x],[u.y,v.y],linestyle='-',\
            color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
                
                    
def drawPoint(pt1):
    ax.plot(pt1[0],pt1[1],linestyle='none',marker='o',markersize=12,color='red')
"""

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



"""
def drawCars(cars, draw=True):
    global car_data
    car_list = np.zeros((len(cars), 2))
    row = 0
    for car in cars: 
        current_position = car.current_position
        if type(current_position) is Intersection: 
            car_list[row, 0] = current_position.x
            car_list[row, 1] = current_position.y
        else: 
            portion = car.ts_on_current_position / car.current_position.time_steps
            car_list[row, 0] = (current_position.u.x  \
                            + (current_position.v.x \
                            - current_position.u.x)) * portion
            car_list[row, 1] = (current_position.u.y  \
                            + (current_position.v.y \
                            - current_position.u.y)) * portion
        row += 1
    if draw: 
        car_data, = ax.plot(car_list[:,0],car_list[:,1],linestyle='none',\
            marker=c.CAR_PLOT_SHAPE,markersize=c.CAR_PLOT_SIZE,color='red')
    else: 
        return car_list

def update(cars): 
    global car_data
    car_list = drawCars(cars, draw=False)

    car_data.set_xdata(car_list[:,0])
    car_data.set_ydata(car_list[:,1])

    plt.draw()
    plt.pause(c.ANIMATION_SEG)

# for image initiation 
"""
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
"""
def _init_graph(nodes,edges,cars):
    drawMap(nodes,edges)
    drawCars(cars)

"""
def updateStatus(map):
    individual_travel_time = []
    for car in map.car_map:
        car.update()
        if car.done:
            individual_travel_time.append(car.total_times_for_car)
            print("car's trip history--------------------------------------")
            print(car.path)
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
    plt.show()
    print("time", total_time)
    return total_time, individual_travel_time

def multi_simulations(number_of_simulation): 
    total_time_list = []
    avg_individual_time = []
    m_list = []
    for i in np.arange(number_of_simulation):
        map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
            DISTANCE_FROM_CENTER, NUM_CARS, \
            random_init=RANDOM_START_DESTINATION, modified=True)
        m_list.append(map)
    for map in m_list:
        total_time, individual_travel_time = \
            run_simulation(map, visualization=False)
        total_time_list.append(total_time)
        individual_travel_time = np.array(individual_travel_time)
        avg_individual_time.append(np.mean(individual_travel_time))
    return total_time_list, avg_individual_time
        

#single simulation plotting (int) total_time_steps (list) individual_travel_time

"""
map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
         DISTANCE_FROM_CENTER, NUM_CARS, \
         random_init=RANDOM_START_DESTINATION, modified=True, traffic_tolerance=TRAFFIC_TOLERANCE)      
total_time, individual_travel_time = run_simulation(map, visualization=VISUALIZATION)
individual_travel_time = np.array(individual_travel_time)
np.random.shuffle(individual_travel_time)
x = np.arange(len(individual_travel_time))

map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
         DISTANCE_FROM_CENTER, NUM_CARS, \
         random_init=RANDOM_START_DESTINATION, modified=False)      
total_time, individual_travel_time = run_simulation(map, visualization=VISUALIZATION)
"""
"""
print("total_time_step", total_time)
plt.plot(x, individual_travel_time)
plt.show()
"""



total_time_list, avg_individual_time = multi_simulations(NUM_SIMULATION)
"""
x = np.arange(len(total_time_list))
plt.figure(0)
plt.plot(x, total_time_list)
plt.show()

plt.figure(1)
x = np.arange(len(avg_individual_time))
plt.plot(x, avg_individual_time)
plt.show()
"""

    






    
