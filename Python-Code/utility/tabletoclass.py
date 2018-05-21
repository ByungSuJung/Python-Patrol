import numpy as np
from ../node import Node
from ../road import Road
import ../constants as c
def node_to_object(nodes):
    ''' converts numpy array nodes into list of node objects
    
    Args:
        nodes: numpy array nodes

    Returns:
        a list of Node object
    '''
    return [Node(inode[0],inode[1],inode[2]) for inode in nodes]

def edge_to_object(edges):
    ''' converts numpy array edges into list of edge objects

    Args:
        edges: numpy array edges

    Returns:
        a list of Edge object
    '''
    oneway_edges = edges[np.where(edges[5])]
    biway_edges = edges[np.where(edges[5]==False)]
    roads = [Road(ie[0],ie[1],ie[2],ie[4],ie[6],_time_step(ie[3],ie[4]),ie[3]) for ie in oneway_edges]
    for ie in biway_edges:
        roads.append(Road(ie[0],ie[1],ie[2],ie[4],ie[6][0],_time_step(ie[3],ie[4]),ie[3]))
        roads.append(Road(ie[0],ie[2],ie[1],ie[4],ie[6][0],_time_step(ie[3],ie[4]),ie[3]))
    return roads

def _time_step(length,speed):
    if np.isnan(speed):
        return (int) 120 * length / c.MISSING_SPEED
    else:
        return (int) 120 * length / speed
