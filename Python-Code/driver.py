from map import Map 
#import visualize 
import matplotlib.pyplot as plt
import constants as c
import numpy as np
#import visualize

m = Map()
def update():
    done_list = []
    for car in m.car_map:
        car.update()
        if car.done:
            m.car_map.remove(car) #done_list.append(car)
    
    for car in done_list: 
        m.car_map.remove(car)
        del car

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


def drawCars(cars, node_map):
    car_list = np.zeros((len(cars), 2))

"""
Start the clock
"""
print("finish constructing map")
ts = 0
#visualize.drawMap(m.node_map, m.edge_map)
#visualize.drawCars(m.car_map, nodes=m.node_map)
#plt.show()

# check this one 
while len(m.car_map) > 0:
    update()
    visualize.update(m.car_map, nodes=m.node_map)
    for car in m.car_map:
        if car.done:
            pass
        else:
            car.visited = False
    ts+=1
    #if ts == 500: 
        #break

print("time", ts)
plt.ion()
plt.show()

    






    
