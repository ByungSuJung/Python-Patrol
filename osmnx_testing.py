import osmnx as ox
import networkx as nx 
import numpy as np

center_lat=47.608013
center_lon=-122.335167
center_pt = (center_lat, center_lon)
g = ox.graph_from_point(center_pt, network_type='drive', distance=150)

print("nodes")
#print(g.nodes(data=True))
print("edges")
print(g.edges(data=True))


