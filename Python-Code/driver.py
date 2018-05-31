from map import Map 
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
RANDOM_START_DESTINATION = False
NUM_SIMULATION = 10

"""
def drawMap(nodes,edges):
    if type(nodes) is dict:
        for key, node in nodes.items():
            plt.plot(node.x,node.y,linestyle='none',\
                marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
        for key, edge in edges.items():
            if type(edge.u) is int:
                u = nodes[str(edge.u)]
                v = nodes[str(edge.v)]
                plt.plot([u.x,v.x],[u.y,v.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
            else:
                plt.plot([edge.u.x,edge.v.x],[edge.u.y,edge.v.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
    else:
        nl = np.array([i.id for i in nodes])
        for inode in nodes:
            #draw node
            plt.plot(inode.x,inode.y,linestyle='none',\
                    marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
        for iedge in edges:
            #draw edges
            if type(iedge.u) == int:
                i = nodes[np.where(nl==str(iedge.u))[0][0]]
                j = nodes[np.where(nl==str(iedge.v))[0][0]]
                #print('plot',iedge.id,i.id,i.x,i.y,j.id,j.x,j.y)
                plt.plot([i.x,j.x],[i.y,j.y],linestyle='-',\
                    color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)
            else:
                plt.plot([iedge.u.x,iedge.v.x],[iedge.u.y,iedge.v.y],\
                    linestyle='-',color=c.EDGE_COLOR,linewidth=edge.num_lanes*c.PLOT_EDGE_WIDTH)


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
    if draw: 
        car_data, = plt.plot(car_list[:,0],car_list[:,1],linestyle='none',\
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
""" 

def updateStatus(map):
    for car in map.car_map:
        car.update()
        if car.done:
            map.car_map.remove(car)

def run_simulation(map): 
    total_time = 0
    while len(map.car_map) > 0:
        updateStatus(map)
        for car in map.car_map:
            if car.done:
                pass
            else:
                car.visited = False
        total_time += 1
    print("time", total_time)

def multi_simulations(number_of_simulation): 
    m_list = []
    for i in np.arange(number_of_simulation):
        map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
            DISTANCE_FROM_CENTER, NUM_CARS, \
            random_init=RANDOM_START_DESTINATION, modified=False)
        m_list.append(map)
    for map in m_list:
        run_simulation(map)

map = Map(CENTER_LATITUDE, CENTER_LONGITUDE,\
         DISTANCE_FROM_CENTER, NUM_CARS, \
         random_init=RANDOM_START_DESTINATION, modified=False)       
run_simulation(map)
#multi_simulations(NUM_SIMULATION)


    






    
