import osmnx as ox
import numpy as np

def retreiveMap(**kwargs):
    '''Retreive map from database or from file

    Args:
        place: keyword parameter, location of place tuple of ints or place name
        distance: keyword parameter, distance from center, default 1000
        fromfile: keyword parameter, bool, read from file or not
        filename: keyword parameter, tuple of file names (node file and edge file)
        savefile: keyword parameter, bool

    Returns:
        numpy array of nodes and edges
        nodes = id, x, y
        edges = id, u, v, length, speed, oneway(bool), lanes
    '''
    place = None
    distance = 1000
    from_file = False
    filename = None
    savefile = False
    if 'savefile' in kwargs:
        savefile = kwargs['savefile']
    if 'place' in kwargs:
        place = kwargs['place']
    if 'distance' in kwargs:
        distance = kwargs['distance']
    if 'fromfile' in kwargs:
        from_file = kwargs['fromfile']
    if 'filename' in kwargs:
        filename = kwargs['filename']
    #- filename is a tuple of nodes and edges
    if from_file:
        return _readFile(filename)
    graph = ox.graph_from_point(place,network_type='drive',distance=distance)
    nodes, edges = ox.graph_to_gdfs(graph)

    id_index = nodes.columns.get_loc('osmid')
    x_index = nodes.columns.get_loc('x')
    y_index = nodes.columns.get_loc('y')

    nodes_data = nodes.values[:,[id_index,x_index,y_index]]

    #-id, lanes are list when road is 2-way
    id_index = edges.columns.get_loc('osmid')
    lanes_index = edges.columns.get_loc('lanes')
    length_index = edges.columns.get_loc('length')
    #- maxspeed might be nan
    speed_index = edges.columns.get_loc('maxspeed')
    u_index = edges.columns.get_loc('u')
    v_index = edges.columns.get_loc('v')
    oneway_index = edges.columns.get_loc('oneway')

    edges_data = edges.values[:,[id_index,u_index,v_index,length_index,\
            speed_index,oneway_index,lanes_index]]
    if savefile:
        if filename is not None and len(filename) is not 2:
            if len(filename) is not 2:
                print('Value error in retreiveMap, should have 2 filenames!, saving as default ... ')
            np.save(filename[0],nodes_data)
            np.save(filename[1],edges_data)
        else:
            np.save('map/nodes.npy',nodes_data)
            np.save('map/edges.npy',edges_data)

    return nodes_data, edges_data

def _readFile(filename):
    fnode, fedge = filename
    return np.load(fnode),np.load(fedge)

if __name__=='__main__':
    n, e = retreiveMap(place=(47.608013,-122.335167))
    help(retreiveMap)
    print(n[0])
    print(e[0])
