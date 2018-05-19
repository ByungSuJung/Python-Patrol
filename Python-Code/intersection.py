import numpy as np
import matplotlib.pyplot as plt

class intesection(object):
	def __init__(self, name, x, y):
		self.id = name							#int - Unique identifier for this node
		self.x = x 								#int - X coordinate on the map
		self.y = y 								#int - Y coordinate on the map
		self.queue = []							#Queue - Queue of Cars at this location
		self.q_size = 0							#int - Current number of elements in the queue
		self.edge_list = [] 					#List - List of connected edges
		self.cap = len(self.edge_list)			#int - Allowed size of queue
		self.ts = 2								#int - Number of time steps to pass through node
		self.visted = False						#bool - Used for dijkstra's shortest path

	def add_node(self, road):
		self.edges.append(edge)

	def add(self, car):
		self.queue.append(car)					#Place the car onto the queue
		self.q_size += 1						#Properly track queue size
		car.ts_on_obj = 0						#Reset the time on object for the car

	def remove(self):
		self.queue.pop()						#Remove the front car from the queue
		self.q_size -= 1						#Properly track queue size

	def run(self):
		keep_moving = True						#Flag that determines if you should keep looping
		curr_car = 0							#Index of the current item you're looking at in the queue

		for car in self.queue:					#Go through each item in the queue if you can and move accordingly
			if(not keep_moving):				#If the one of the front cars couldn't go you need to break
				break

			if(car.ts_on_obj == self.ts):
				moved = car.modified_dijkstra()	#Returns True or False depending if the car was able to move or not

				if(moved):
					self.remove()				#Pop the car off the queue since it moved to an edge

			else:								#If it was not time for the car to move yet just
				car.ts_on_obj += 1				#increment how long it's been at the node for

			keep_moving = False
			print(car)

		def modified_dijkstra(self, car):
			decide = np.random.randint(0,2).astype(bool)

			if(decide):
				print("You've been give your next node")
				return True
			else:
				print("You can't move")
				return False

test = intesection("a", 1, 2)

node = np.load("node.npy")
edge = np.load("edge.npy")

#print(edge)
#print(node)

x_vals = node[:, 1].astype(np.float64)
y_vals = node[:, 2].astype(np.float64)

plt.plot(x_vals, y_vals, 'o')
#plt.show()