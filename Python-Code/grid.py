import sys
import numpy as np 

class car:
	def __init__(self, start_loc, end_loc):
		self.start = start_loc
		self.end = end_loc
		self.current = start_loc
		self.time = 0

class city:
	def __init__(self, city_name):
		self.id = city_name
		self.distance = sys.maxsize
		self.edges = []
		self.visted = False

	def add_edge(self, edge):
		self.edges.append(edge)

class edge:
	congestion = 0

	def __init__(self, cityA, cityB, length):
		self.cityA = cityA
		self.cityB = cityB
		self.length = length

mar = city(0)
sea = city(1)
bot = city(2)
bel = city(4)
red = city(5)

mar_sea = edge(mar, sea, 5)
mar_bot = edge(mar, bot, 3)
mar_bel = edge(mar, bel, 4)
sea_bel = edge(bel, sea, 5)
bel_bot = edge(bel, bot, 2)
bel_red = edge(bel, red, 3)

mar.add_edge(mar_sea)
mar.add_edge(mar_bot)
mar.add_edge(mar_bel)

print(mar.edges[0].cityB.id)