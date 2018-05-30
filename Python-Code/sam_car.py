from road import Road
class Car:
	def __init__(self,start,dest):
		self.start = start
		self.current_position = start
		self.dest = dest
		self.ts_on_current_position=0
		self.paths = None
		#start.add()

	def set_path(self,paths):
		self.paths = paths
	def print_test(self):
		for i in self.paths:
			print(str(i))
	'''
	def move(self,callback):
		if type(self.current_position) == Road:
			if self.ts_on_current_position < self.current_position.time_steps:
				self.ts_on_current_position += 1
			else:
				#if self.paths[0].add(self):
				if callback(self.current_position.id,'E',self):
					self.ts_on_current_position = 0
					tmp = str(self.paths[0].id)
					#self.current_position.remove()
					self.current_position = self.paths[0]
					self.paths.pop(0)
					return tmp,'N'
				else:
					print('on hold',type(self.paths[0]),self.paths[0])
					return False, None
		else:
			#if self.paths[0].add(self):
			print('DBG1')
			if callback(self.current_position.id,'N',self):
				print('DBG2')
				self.ts_on_current_position = 0
				tmp = str(self.paths[0].id)
				#self.current_position.remove()
				self.current_position = self.paths[0]
				self.paths.pop(0)
				return tmp, 'E'
		return True, None
		'''