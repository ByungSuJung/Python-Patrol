import numpy as np 

class Car(object):
	def __init__(self, start_loc, end_loc):
		self.start = start_loc#Starting node
		self.end = end_loc#Destination
		self.current = start_loc#Current location
		self.in_transite = False#Is it on a road
		self.time_step_at_loc = 0#How many time steps it's been at a node or an edge
		self.total_time_steps = 0#How long it's been traveling for
		self.x_pos = 0#x position on grid
		self.ypos = 0#y position on grid

		self._set_coordinates()

	def _set_coordinates(self):
		#This function should convert the current
		#location into x and y locations on some grid
		#For the visualization portion
		return

meCar = Car(4, 5)

print(meCar.x_pos)