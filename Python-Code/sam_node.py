class Node:
	def __init__(self,name,x,y):
		self.id = name
		self.x = x
		self.y = y
		
	def fill_edges(self,edges):
		self.edges = edges
