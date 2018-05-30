import numpy as np
from intersection import Intersection as Node
from road import Road
import constants as c
def node_to_object(nodes):
    ''' converts numpy array nodes into list of node objects
    
    Args:
        nodes: numpy array nodes
    Returns:
        a list of Node object
    '''
    node_dic = {}
    for inode in nodes:
        id = str(inode[0])
        while id in node_dic:
            id = id + '9'
        if id in node_dic:
            continue
        node_dic[id] = Node(id,inode[1],inode[2])
    
    return node_dic
    
def edge_to_object(edges):
    ''' converts numpy array edges into list of edge objects
    Args:
        edges: numpy array edges
    Returns:
        a list of Edge object
    '''
    roads_dic = {}
    
    oneway_edges = edges[np.where(edges[:,5])[0],:]
    biway_edges = edges[np.where(edges[:,5]==False)[0],:]
    #- one way edge may contain multiple id coresponding to each lane
    #print('edges shape verification: util[43] - ',np.shape(edges),np.shape(oneway_edges),np.shape(biway_edges))
    for e in oneway_edges:
        id = e[0]
        length = e[3]
        speed = e[4]
        lanes = e[-1]
        if type(id) is list:
            id = id[0]
        
        if type(speed) is float:
            #- Speed is nan
            if np.isnan(speed):
                speed = c.MISSING_SPEED
        elif type(speed) is list:
            #- Speed is a list
            speed = max([int(i.split()[0]) for i in speed])
        else:
            #- Speed is in mph
            speed = int(speed.split()[0])
            
        if type(lanes) is float:
            #- lanes is nan
            if np.isnan(lanes):
                lanes = 1
        elif type(lanes) is list:
            #- lanes is list
            lanes = np.max([int(i) for i in lanes])
        id = str(id)
        while id in roads_dic:
            #print(roads_dic[id].u,roads_dic[id].v,roads_dic[id].id,'||||||',id,e[1],e[2])
            id = id + '99'
        if id in roads_dic:
            continue
        roads_dic[id] = Road(id,e[1],e[2],speed,int(lanes),length)
    for e in biway_edges:
        #- add 002 at the end of id for the opposite direction
        id = e[0]
        length = e[3]
        speed = e[4]
        lanes = e[-1]
        dif_lanes = False
        
        if type(id) is list:
            id = id[0]
            
        if type(speed) is float:
            #- Speed is nan
            if np.isnan(speed):
                speed = c.MISSING_SPEED
        elif type(speed) is list:
            #- Speed is a list
            speed = max([int(i.split()[0]) for i in speed])
        else:
            #- Speed is in mph
            speed = int(speed.split()[0])
            
        if type(lanes) is float:
            #- lanes is nan
            if np.isnan(lanes):
                lanes = 1
        elif type(lanes) is list:
            #- lanes is list
            lanes = [int(i) for i in lanes]
            dif_lanes = True
            
        #roads_dic[str(id)] = Road(str(id),e[1],e[2],speed,int(lanes),length)
        id = str(id)
        while id in roads_dic:
            #print(roads_dic[id].u,roads_dic[id].v,roads_dic[id].id,'||||||',id,e[1],e[2])
            id = id + '11'
        if id in roads_dic:
            continue
        if dif_lanes:
            roads_dic[id] = Road(id,e[1],e[2],speed,int(lanes[0]),length)
        else:
            roads_dic[id] = Road(id,e[1],e[2],speed,int(lanes),length)
            
        if dif_lanes:
            roads_dic[id + '002'] = Road(id,e[2],e[1],speed,int(lanes[1]),length)
        else:
            roads_dic[id + '002'] = Road(id,e[2],e[1],speed,int(lanes),length)
        return roads_dic