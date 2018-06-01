import numpy as np
import copy
import sys

nodes = None
edges = None
node_keys = None
edge_keys = None

def init(n,e,nk,ek):
    ''' Initialize global variables
    Args:
        n: dict, nodes
        e: dict, edges
        nk: list, nodes' ids
        ek: list, edges' ids
    '''
    global nodes, edges, node_keys, edge_keys
    nodes = n
    edges = e
    node_keys = nk
    edge_keys = ek

def dk(start,end,weight_on_length=1.0,parallel=False):
    ''' Initialize global variables
    Args:
        start: str or Node, starting node id
        end: str or Node, destination node id
        weight_on_length: float [0.0:1.0], weight ratio used for computing weight
        parallel: bool, if parallel, returns ids. if not parallel, returns objects
    Returns:
        tuple of ids if parallel. Otherwise, return list of nodes and edges
    '''
    def _weight(time,capacity):
        #- calculate weight on the edge
        return capacity * 100 * (1-weight_on_length) + time * 100 * (weight_on_length)
    weights = {}
    used = {}
    paths = {}
    
    for key,node in nodes.items():
        #- set weight on each node to a very large number
        weights[str(node.id)] = 999999999999999999
        #- set visited on each node to False
        used[str(node.id)] = False
        #- set path on each node to empty list
        paths[str(node.id)] = []
        
    #- initialize dictionary at starting point
    used[str(start)] = True
    weights[str(start)] = 0
    paths[str(start)] = [str(start)]
    
    last_run = [str(start)]
    #- tmp_run is nodes visited during this cycle
    tmp_run = []

    while not used[str(end)]:
        if len(last_run) == 0:
            #- route can not be determined
            return False

        #- run through each node visited last time
        for cur in last_run:
            #- neighbor_edges in str
            neighbor_edges = nodes[str(cur)].out_edges
            neighbor_edges = [str(i) for i in neighbor_edges]

            #- determine neighbor nodes
            neighbor_nodes = [str(edges[ne].v) for ne in neighbor_edges]

            for i in range(len(neighbor_nodes)):
                this_id = str(neighbor_nodes[i])
                #- calculate weight on this edge
                weight = _weight(edges[neighbor_edges[i]].time,edges[neighbor_edges[i]].q_size/edges[neighbor_edges[i]].capacity)
                #- total weight is weight from last node + weight to next node
                tot_weight = weights[cur] + weight
                #- if tot_weight < in the dict, overwrite
                if tot_weight < weights[this_id]:
                    weights[neighbor_nodes[i]] = tot_weight
                    #- paths = original + this node
                    paths[this_id] = copy.deepcopy(paths[cur])
                    paths[this_id].append(neighbor_nodes[i])

                if not used[this_id]:
                    #- if this_id is not visited, mark as visited this time
                    tmp_run.append(this_id)
            for nn in neighbor_nodes:
                used[nn] = True
        #- set last_run as this run, start next run
        last_run = tmp_run
        tmp_run = []
    #- return results for parallel optimized
    if parallel:
        fff = _expand_path(paths[str(end)])
        fff = [str(f) for f in fff]
        return tuple(fff)
    #- return normal result
    return _expand_path(paths[str(end)])

def _expand_path(paths):
    ''' expand paths from nodes to mix of nodes and edges
    
    Args:
        paths: list of nodes in string
    
    Returns:
        list of nodes and edges that car can follow
    '''
    result = [nodes[paths[0]]]
    for i in range(len(paths)-1):
        next_edges = nodes[paths[i]].edge_list
        for edge in next_edges:
            if str(edge.v) == paths[i+1]:
                result.append(edge)
                break
        result.append(nodes[paths[i+1]])
    return result
