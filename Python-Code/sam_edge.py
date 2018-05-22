from sam_node import Node

class Road:
	def __init__(self,id,u,v,speed,lane,length):
		self.id = id
		self.u = u
		self.v = v
		self.speed = speed
		self.lane = lane
		self.length = length
		self.tk = 10