import matplotlib.pyplot as plt
import constants as c
from car import Car
from node import Node
from road import Road
import numpy as np

car_data = None

def drawMap(nodes,edges):
    for inode in nodes:
        #draw node
        plt.plot(inode.x,inode.y,linestyle='none',\
                marker=c.NODE_PLOT_SHAPE,markersize=c.NODE_PLOT_SIZE)
    for iedge in edges:
        #draw edges
        plt.plot([iedge.u.x,iedge.v.x],[iedge.v.y,iedge.v.y],\
                linestyle='-',marker='none']

def drawCars(cars,draw=True):
    global car_data
    car_list = np.zeros((len(cars),2))
    it = 0
    for icar in cars:
        cur_p = icar.current_position
        if type(cur_p) is Node:
            car_list[it,0] = cur_p.x
            car_list[it,1] = cur_p.y
        else:
            #- car is on edge
            #car.ts_on_current_position
            portion = icar.ts_on_current_position / cur_p.time_steps
            
            car_list[it,0] = cur_p.u.x + (cur_p.v.x-cur_p.u.x) * portion
            car_list[it,1] = cur_p.u.y + (cur_p.v.y-cur_p.u.y) * portion
    if draw:
        car_data = plt.plot(car_list[0],car_list[1],linestyle='none',\
            marker=c.CAR_PLOT_SHAPE,markersize=c.CAR_PLOT_SIZE)
    else:
        return car_list

def update(cars):
    global car_data
    car_list = drawCars(cars,draw=False)
    car_data.set_xdata(car_list[0])
    car_data.set_ydata(car_list[1])
    #- assum plt.draw() update only cars
    plt.draw()
    plt.pause(1)
    

def init(nodes,edges,cars):
    drawMap(nodes,edges)
    drawCars(cars)
    plt.ion()
    plt.show()
