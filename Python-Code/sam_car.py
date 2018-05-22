from sam_edge import Road
class Car:
	def __init__(self,start,dest):
		self.start = start
		self.current_position = start
		self.dest = dest
		self.ts_on_current_position=0

	def run(self,algrithm):
		if type(self.current_position) == Road:
			if self.ts_on_current_position < 10:
				self.ts_on_current_position += 1
			else:
				self.ts_on_current_position = 0
				self.current_position = self.current_position.v
		else:
			self.current_position = algrithm(self.current_position,self.dest)
