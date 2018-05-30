from road import Road
class Car:
	def __init__(self,start,dest):
		self.start = start
		self.current_position = start
		self.dest = dest
		self.ts_on_current_position=0
		self.paths = None
		start.add(self)

	def set_path(self,paths):
		self.paths = paths
	def move(self):
		if type(self.current_position) == Road:
			if self.ts_on_current_position < self.current_position.time_steps:
				self.ts_on_current_position += 1
			else:
				if self.paths[0].add(self):
					self.current_position.remove()
					self.current_position = self.paths[0]
					self.paths.pop(0)
				else:
					print('on hold',type(self.paths[0]))
					return False
		else:
			if self.paths[0].add(self):
				self.current_position.remove()
				self.current_position = self.paths[0]
				self.paths.pop(0)
		return True