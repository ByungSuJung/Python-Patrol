from map import Map 
#import visualize

m = Map()
def update():
    for car in m.car_map:
        car.update()
        if car.current_position == car.destination:
            m.car_map.remove(car)
"""
Start the clock
"""
print("finish constructing map")
ts = 0

# check this one 
while len(m.car_map) > 0:
    update()
    for car in m.car_map:
        car.visited = False
    #visualize.drawMap(m.node_map, m.edge_map)
    ts+=1
    #if ts == 500: 
        #break

print("time", ts)

    






    
