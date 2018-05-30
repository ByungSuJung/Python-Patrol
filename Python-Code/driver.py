from map import Map 
#import visualize

m = Map()
def update():
    done_list = []
    for car in m.car_map:
        car.update()
        if car.done:
            m.car_map.remove(car) #done_list.append(car)
    
    for car in done_list: 
        m.car_map.remove(car)
        del car

    
"""
Start the clock
"""
print("finish constructing map")
ts = 0

# check this one 
while len(m.car_map) > 0:
    update()
    for car in m.car_map:
        if car.done:
            pass
        else:
            car.visited = False
    #visualize.drawMap(m.node_map, m.edge_map)
    ts+=1
    #if ts == 500: 
        #break

print("time", ts)

    






    
