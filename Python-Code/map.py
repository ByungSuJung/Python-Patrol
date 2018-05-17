import osmnx as ox 
import networkx as nx
import geopandas as gpd 
import matplotlib.pyplot as plt
import pandas as pd

#Latitude and logitude coordinates of downtown Seattle 
place_point = (47.608013, -122.335167)
graph = ox.graph_from_point(place_point, network_type='drive')
fig, ax = ox.plot_graph(graph)

nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)
print(nodes.columns)
print(nodes)
print(edges.columns)
print(edges)
