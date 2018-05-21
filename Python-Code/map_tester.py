import osmnx as ox
import numpy as np

place_point = (47.608013, -122.335167)
#- change distance to change map size. Not sure the unit
graph = ox.graph_from_point(place_point,network_type='drive',distance=1000)

nodes, edges = ox.graph_to_gdfs(graph)
print(nodes.columns)
print(nodes.columns.get_loc('x'))
print(edges.columns)
print(edges.values[0])
#check nodes, edges header by nodes.columns to get indices
'''
node_data = nodes.values
edge_data = edges.values
'''
#in this case, node x,y is at [3,4]
#print(node_data[:,[3,4]].astype(np.float64))
