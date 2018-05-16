import numpy as np 

class Intersection(object):
	def __init__(self, city_name):
		self.id = city_name
		self.distance = sys.maxsize
		self.edges = []
		self.visted = False

	def add_road(self, road):
		self.edges.append(edge)