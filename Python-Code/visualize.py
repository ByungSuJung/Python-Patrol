import matplotlib.pyplot as plt
import constants as c
from sam_car import Car
from sam_node import Node
from sam_edge import Road
import numpy as np
import utility as util

car_data = None

def drawMap(nodes,edges):
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
            plt.plot([i.x,j.x],[i.y,j.y],linestyle='-')
        else:
            plt.plot([iedge.u.x,iedge.v.x],[iedge.u.y,iedge.v.y],\
                linestyle='-')


def drawCars(cars,draw=True):
    global car_data
    car_list = np.zeros((len(cars),2))
    it = 0
    for icar in cars:
        cur_p = icar.current_position
        if type(cur_p) is Node:
            car_list[it,0] = cur_p.x
            car_list[it,1] = cur_p.y
            print(cur_p.id,cur_p.x,cur_p.y)
        else:
            #- car is on edge
            #car.ts_on_current_position
            portion = icar.ts_on_current_position / 10 #cur_steps
            
            car_list[it,0] = cur_p.u.x + (cur_p.v.x-cur_p.u.x) * portion
            car_list[it,1] = cur_p.u.y + (cur_p.v.y-cur_p.u.y) * portion
        it += 1
    if draw:
        car_data, = plt.plot(car_list[:,0],car_list[:,1],linestyle='none',\
            marker=c.CAR_PLOT_SHAPE,markersize=c.CAR_PLOT_SIZE,color='black')
    else:
        return car_list

def update(cars):
    global car_data
    car_list = drawCars(cars,draw=False)

    car_data.set_xdata(car_list[:,0])
    car_data.set_ydata(car_list[:,1])
    #- assum plt.draw() update only cars
    plt.draw()
    plt.pause(1)
    

def init(nodes,edges,cars):
    drawMap(nodes,edges)
    drawCars(cars)
    plt.ion()
    plt.show()

if __name__ == '__main__':
    #nodes = [Node('node1',2,3),Node('node2',6,8),Node('node3',14,7)]
    #edges = [Road(0,nodes[0],nodes[1],50,1,10),Road(1,nodes[0],nodes[2],50,1,10),Road(2,nodes[1],nodes[2],50,1,10)]
    #drawMap(nodes,edges)
    def dk(start,end):
        return 1

    nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=1000)
    print(np.shape(edges))
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)
    ids = np.array([ind.u for ind in edges])

    for inode in nodes:
        indice = np.where(inode.id == ids)[0]
        if len(indice) == 0:
            continue
        inode.fill_edges(edges[indice])
        
    drawMap(nodes,edges)
    cars_u = np.random.randint(len(nodes),size=20)
    cars_v = np.random.randint(len(nodes),size=20)
    cars =[]
    for i in range(20):
        cars.append(Car(nodes[cars_u[i]],nodes[cars_v[i]]))
    drawCars(cars)
    plt.ion()
    
    plt.show()
