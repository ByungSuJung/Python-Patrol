import numpy as np

class Road(object):
	def __init__(self, start, end, length):
		self.start = start
		self.end = end
		self.length = length
		self.time_steps = length#This would be changed


	def _set_time_steps():
		#This method could calculate the amount of
		#time steps it costs to traverse the road