from map import Map 
import matplotlib
#import visualize 
import matplotlib.pyplot as plt
import constants as c
import numpy as np
from intersection import Intersection
#import visualize

# CONSTANTS 
CENTER_LATITUDE = 47.608013
CENTER_LONGITUDE = -122.335167
DISTANCE_FROM_CENTER = 300
NUM_CARS = 100
VISUALIZATION = False
RANDOM_START_DESTINATION = True
NUM_SIMULATION = 10
car_data = None

fig, ax = plt.subplots()

from car import Car
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
            portion = car.ts_on_current_position / 10
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

def _init_graph(nodes,edges,cars):
    plt.ion()
    drawMap(nodes,edges)
    drawCars(cars)

def updateStatus(map):
    individual_travel_time = []
    for car in map.car_map:
        car.update()
        if car.done:
            individual_travel_time.append(car.total_times_for_car)
            map.car_map.remove(car)
            del car
    return individual_travel_time

def run_simulation(map, visualization=False): 
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
            random_init=RANDOM_START_DESTINATION, modified=False)
        m_list.append(map)
    for map in m_list:
        total_time, individual_travel_time = \
            run_simulation(map, visualization=False)
        total_time_list.append(total_time)
        individual_travel_time = np.array(individual_travel_time)
        avg_individual_time.append(np.mean(individual_travel_time))
    return total_time_list, avg_individual_time
        

#single simulation plotting (int) total_time_steps (list) individual_travel_time
map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
         DISTANCE_FROM_CENTER, NUM_CARS, \
         random_init=RANDOM_START_DESTINATION, modified=False)      
total_time, individual_travel_time = run_simulation(map)
individual_travel_time = np.array(individual_travel_time)
np.random.shuffle(individual_travel_time)
x = np.arange(len(individual_travel_time))
"""
print("total_time_step", total_time)
plt.plot(x, individual_travel_time)
plt.show()
"""


"""
total_time_list, avg_individual_time = multi_simulations(NUM_SIMULATION)

x = np.arange(len(total_time_list))
plt.figure(0)
plt.plot(x, total_time_list)
plt.show()

plt.figure(1)
x = np.arange(len(avg_individual_time))
plt.plot(x, avg_individual_time)
plt.show()
"""

    






    
