import osmnx as ox
import networkx as nx 
import numpy as np
import random as rn 
from intersection import Intersection
from road import Road 
from car import Car
center_lat=47.608013
center_long=-122.335167
dist=500
center_pt = (center_lat, center_long)
G = ox.graph_from_point(center_pt, network_type='drive', distance=dist)
print("works here")

for e in G.edges(data=True):
    e = e[2]
    if 'maxspeed' in e:
        if type(e['maxspeed']) is list:
            print(e)
    else:
        print("not a list")