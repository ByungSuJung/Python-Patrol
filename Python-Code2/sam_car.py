from road import Road
class Car:
	def __init__(self,start,dest):
		self.start = start
		self.current_position = start
		self.dest = dest
		self.ts_on_current_position=0
		self.paths = None

	def run(self,algrithm,nodes):
		if type(self.current_position) == Road:
			if self.ts_on_current_position < self.current_position.time_steps:
				self.ts_on_current_position += 1
			else:
				self.ts_on_current_position = 0
				self.current_position = nodes[str(self.current_position.v)]
		else:
			self.current_position = algrithm(self.current_position,self.dest,self)

	def set_path(self,paths):
		self.paths = paths
	def move(self):
		if type(self.current_position) == Road:
			if self.ts_on_current_position < 10:
				self.ts_on_current_position += 1
			else:
				self.ts_on_current_position = 0
				self.current_position = self.paths[0]
				self.paths.pop(0)
		else:
			self.current_position = self.paths[0]
			self.paths.pop(0)