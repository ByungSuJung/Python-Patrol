import numpy as np
import copy
import sys

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
    def _weight(time,capacity):
        return capacity * 100 * (1-weight_on_length) + time * 100 * (weight_on_length)
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
    neighbor_history = []
    history = [last_run]
    tmp_run = []
    #counter=0
    while not used[str(end)]:
        #- sometimes error occured, this if statement just for avoiding errors
        #print(last_run)
        #print('counter',counter)
        #counter+=1
        if len(last_run) == 0:
            #print(history)
            print('start',start,'destination',end,end in nodes)
            #print(neighbor_history)
            for i in history:
                if end in i:
                    print('?????')
            for i in neighbor_history:
                if end in i:
                    print('!!!!!')
            #quit()
            return False
        #- run thru each nodes visited last cycle
        for cur in last_run:
            neighbor_edges = nodes[str(cur)].out_edges
            neighbor_edges = [str(i) for i in neighbor_edges]
            for ne in neighbor_edges:
                if not ne in edges:
                    print(ne,str(ne) in edges)
                    print(edges)
                    quit()
            neighbor_nodes = [str(edges[ne].v) for ne in neighbor_edges]
            neighbor_history.append(neighbor_nodes)
            #print('neighbor_nodes',neighbor_nodes)
            #print('neighbor_edges',neighbor_edges)
            for i in range(len(neighbor_nodes)):
                this_id = str(neighbor_nodes[i])
                
                    #- weight is set to be length
                    # --- weight = edges[neighbor_edges[i]].length
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
                    tmp_run.append(this_id)
            for nn in neighbor_nodes:
                used[nn] = True
        history.append(tmp_run)
        last_run = tmp_run
        tmp_run = []
        
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
