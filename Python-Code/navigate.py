from road import Road
from intersection import Intersection
import numpy as np
import copy, sys

nodes = None
edges = None
node_keys = None
edge_keys = None

def init(n,e,nk,ek):
    global nodes, edges, node_keys, edge_keys
    nodes = n
    edges = e
    node_keys = nk
    edge_keys = ek

def dk(start,end,weight_on_length=1.0):
    weights = {}
    used = {}
    paths = {}
    
    for key,node in nodes.items():
        weights[str(node.id)] = 999999999999999999
        used[str(node.id)] = False
        paths[str(node.id)] = []
        
    #- initialize dictionary at starting point
    used[str(start)] = True
    weights[str(start)] = 0
    paths[str(start)] = [str(start)]
    
    last_run = [str(start)]
    
    #- tmp_run is nodes visited during this cycle
    tmp_run = []
    
    while not used[str(end)]:
        #- sometimes error occured, this if statement just for avoiding errors
        if len(last_run) == 0:
            return False
        #- run thru each nodes visited last cycle
        for cur in last_run:
            neighbor_edges = nodes[str(cur)].edge_list
            neighbor_nodes = [str(edges[ne].v) for ne in neighbor_edges]
            for i in range(len(neighbor_nodes)):
                this_id = str(neighbor_nodes[i])
                if not used[this_id]:
                    tmp_run.append(this_id)
                    #- weight is set to be length
                    weight = edges[neighbor_edges[i]].length
                    #- total weight is weight from last node + weight to next node
                    tot_weight = weights[cur] + weight
                    #- if tot_weight < in the dict, overwrite
                    if tot_weight < weights[this_id]:
                        weights[neighbor_nodes[i]] = tot_weight
                        #- paths = original + this node
                        paths[this_id] = copy.deepcopy(paths[cur])
                        paths[this_id].append(neighbor_nodes[i])
            for nn in neighbor_nodes:
                used[nn] = True
        last_run = tmp_run
        tmp_run = []
        
    return _expand_path(paths[end])

def _expand_path(paths):
    ''' expand paths from nodes to mix of nodes and edges
    
    Args:
        paths: list of nodes
    
    Returns:
        list of nodes and edges that car can follow
    '''
    result = [nodes[paths[0]]]
    for i in range(len(paths)-1):
        next_edges = nodes[paths[i]].edge_list
        for edge in next_edges:
            if str(edges[edge].v) == paths[i+1]:
                result.append(edges[edge])
                break
        result.append(nodes[paths[i+1]])
    #print(result)
    return result
