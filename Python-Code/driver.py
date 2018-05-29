from map import Map 
#import visualize

m = Map()
def update():
    for car in m.car_map:
        car.update()
"""
Start the clock
"""
ts = 0
while m.car_map:
    update()
    #visualize.drawMap(m.node_map, m.edge_map)
    ts+=1

    






    

