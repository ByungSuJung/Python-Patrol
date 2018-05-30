import matplotlib.pyplot as plt
import constants as c
from sam_car import Car
import numpy as np
import utility as util
import navigate as nv
from intersection import Intersection

car_data = None
nodes = None
edges = None
test_start = None
test_end = None

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
                    
    #plt.plot(test_end[0],test_end[1],color='red',linestyle='none',marker='o',markersize=10)


def drawCars(cars,draw=True):
    global car_data
    car_list = np.zeros((len(cars),2))
    it = 0
    for icar in cars:
        cur_p = icar.current_position
        if type(cur_p) is Intersection:
            car_list[it,0] = cur_p.x
            car_list[it,1] = cur_p.y
            #print(cur_p.id,cur_p.x,cur_p.y)
        else:
            #- car is on edge
            #car.ts_on_current_position
            portion = icar.ts_on_current_position / 10 #cur_steps
            car_list[it,0] = nodes[str(cur_p.u)].x + (nodes[str(cur_p.v)].x-nodes[str(cur_p.u)].x) * portion
            car_list[it,1] = nodes[str(cur_p.u)].y + (nodes[str(cur_p.v)].y-nodes[str(cur_p.u)].y) * portion
        it += 1
    if draw:
        car_data, = plt.plot(car_list[:,0],car_list[:,1],linestyle='none',\
            marker=c.CAR_PLOT_SHAPE,markersize=c.CAR_PLOT_SIZE,color='red')
    else:
        return car_list

def update(cars):
    global car_data
    car_list = drawCars(cars,draw=False)

    car_data.set_xdata(car_list[:,0])
    car_data.set_ydata(car_list[:,1])
    #- assum plt.draw() update only cars
    plt.draw()
    plt.pause(c.ANIMATION_SEG)
    

def _init_graph(nodes,edges,cars):
    drawMap(nodes,edges)
    drawCars(cars)

if __name__ == '__main__':
    '''Note
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !For now, ts on each road is set to be 10!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    
    #- CONSTANTS are in constants.py Feel free to change
    
        
    #nodes, edges = util.retreiveMap(place=(47.608013, -122.335167),distance=1000,savefile=True)
    
    #- If files do not exist, un-comment the line above and comment 3 lines below
    nodes_file_path = 'map/nodes.npy'
    edges_file_path = 'map/edges.npy'
    nodes, edges = util.retreiveMap(fromfile=True,filename=(nodes_file_path,edges_file_path))
    
    #- nodes and edges in dictionary form
    nodes = util.node_to_object(nodes)
    edges = util.edge_to_object(edges)
    
    #add edges to nodes
    for key, edge in edges.items():
        nodes[str(edge.u)].add_edge(str(edge.id))
        
    #- get seperate list of ids
    node_key = list(nodes.keys())
    edge_key = list(edges.keys())
    
    #test_end = (nodes[node_key[339]].x,nodes[node_key[339]].y)
    
    #- initialize navigator
    nv.init(nodes,edges,node_key,edge_key)
    
    #-some pairs of start and end dont work, do not why
    
    car_size = c.NUMBER_CARS
    #- pick random starts and ends
    cars_u = np.random.randint(len(nodes),size=car_size)
    cars_v = np.random.randint(len(nodes),size=car_size)
    cars =[]
    for i in range(car_size):
        cars.append(Car(nodes[node_key[cars_u[i]]],nodes[node_key[cars_v[i]]]))
    
    #- have map and cars ready on plot
    _init_graph(nodes,edges,cars)
    
    #- calculate shortest path for each car
    for car in cars:
        paths = nv.dk(car.start.id,car.dest.id)
        while type(paths) is bool:
            #- when pair of starts and destinations do not work, get new destination
            r_v = np.random.randint(len(nodes))
            car.dest = nodes[node_key[r_v]]
            paths = nv.dk(car.start.id,car.dest.id)
        #- add paths to car object
        car.set_path(nv.dk(str(car.start.id),str(car.dest.id)))
    
    while len(cars) > 0:
        for car in cars:
            if car.current_position.id == car.dest.id:
                cars.remove(car)
                #update(cars)
            else:
                car.move()
        update(cars)
    
    plt.ion()
    plt.show()
