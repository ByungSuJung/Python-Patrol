import osmnx as ox
import networkx as nx 
import numpy as np

center_lat=47.608013
center_long=-122.335167
dist=150
center_pt = (center_lat, center_long)
graph = ox.graph_from_point(center_pt, network_type='drive', distance=dist)

print(len(graph.edges))
id = 0
for e in graph.edges(data=True):
    mspd = e[2]['maxspeed']
    max_spd = mspd.split(" ")[0]
    if int(max_spd):
        print(max_spd)
    id +=1