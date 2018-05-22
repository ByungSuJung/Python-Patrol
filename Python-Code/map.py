import osmnx as ox 
import networkx as nx
import geopandas as gpd 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Latitude and logitude coordinates of downtown Seattle 
place_point = (47.608013, -122.335167)
print("Making graph")
graph = ox.graph_from_point(place_point, network_type='drive',distance=100)
fig, ax = ox.plot_graph(graph)

#nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)
#node, edge = ox.graph_to_gdfs(graph, nodes=True, edges=True)
#node_data = node.values[:,[2,3]]
#print(node_data)
#print(node.columns)
#print(nodes.geometry)
#print(edges.columns)
#print(edges.maxspeed, edges.lanes, edges.length, edges.u, edges.v, edges.geometry)
edge = np.load("C:/Users/trece/Downloads/edge.npy")
print(np.shape(edge))
node = np.load("C:/Users/trece/Downloads/node.npy")
print(node)
x_vals = node[:, 1].astype(np.float64)
y_vals = node[:, 2].astype(np.float64)
print("Plotting")
plt.plot(x_vals, y_vals, 'o')
print("Showing")
plt.ioff()
plt.show()
plt.close()
print("Should close")